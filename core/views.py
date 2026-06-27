import json
import logging
import re
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Contract, NewsletterSubscriber, Order, OrderItem, Product

logger = logging.getLogger(__name__)
CONSOLE_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


def frontend(request):
    frontend_index = settings.FRONTEND_DIST_DIR / 'index.html'
    if not frontend_index.exists() and settings.FRONTEND_SITE_URL:
        return redirect(settings.FRONTEND_SITE_URL)
    return render(request, 'index.html')


def parse_display_price(display_price):
    match = re.search(r'\d+(?:\.\d+)?', display_price or '')
    if not match:
        return Decimal('0.00')
    return Decimal(match.group(0)).quantize(Decimal('0.01'))


def serialize_product(product):
    return {
        'id': product.slug,
        'slug': product.slug,
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'numeric_price': str(parse_display_price(product.price)),
        'tag': product.tag,
        'tone': product.tone,
        'image': product.image_url,
        'note': product.note,
        'material': product.material,
        'care': product.care,
        'fit': product.fit,
    }


def read_json_body(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def clean_required(payload, field, label, max_length=None):
    value = str(payload.get(field, '')).strip()
    if not value:
        raise ValueError(f'Please fill in {label}.')
    if max_length and len(value) > max_length:
        raise ValueError(f'{label} is too long.')
    return value


def clean_email(payload, field='email'):
    email = str(payload.get(field, '')).strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        raise ValueError('Please enter a valid email.')
    return email


def build_contract_email(contract):
    subject_name = contract.name or contract.contact_name
    subject = f'New PawNest inquiry: {subject_name or "Website inquiry"}'
    message = '\n'.join(
        [
            'A new inquiry was submitted from the PawNest website.',
            '',
            f'Name: {contract.name or contract.contact_name}',
            f'Email: {contract.email or "-"}',
            f'WhatsApp / phone: {contract.phone}',
            f'Country: {contract.country or "-"}',
            f'Interested products: {contract.interested_products or "-"}',
            '',
            'Message:',
            contract.message or contract.requirement,
            '',
            'Legacy sourcing fields:',
            f'Company / brand: {contract.company_brand or "-"}',
            f'Project type: {contract.project_type or "-"}',
            f'Estimated quantity: {contract.estimated_quantity or "-"}',
            f'Delivery city: {contract.delivery_city or "-"}',
            f'Budget range: {contract.budget_range or "-"}',
            '',
            f'Admin record: /admin/core/contract/{contract.id}/change/',
        ]
    )
    return subject, message


def send_contract_notification(contract):
    recipient = getattr(settings, 'CONTRACT_NOTIFICATION_EMAIL', '')
    if not recipient:
        logger.warning('Contract notification skipped because CONTRACT_NOTIFICATION_EMAIL is empty.')
        return False
    if getattr(settings, 'EMAIL_BACKEND', '') == CONSOLE_EMAIL_BACKEND:
        logger.warning('Contract notification skipped because console email backend does not send real email.')
        return False

    subject, message = build_contract_email(contract)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )
    return True


def build_order_number():
    date_part = timezone.localdate().strftime('%Y%m%d')
    prefix = f'PN{date_part}'
    for sequence in range(Order.objects.filter(order_number__startswith=prefix).count() + 1, 10000):
        candidate = f'{prefix}{sequence:04d}'
        if not Order.objects.filter(order_number=candidate).exists():
            return candidate
    raise RuntimeError('No order number is available for today.')


def build_order_admin_email(order):
    subject = f'New PawNest order: {order.order_number}'
    item_lines = [
        f'- {item.product_name} x {item.quantity}: ${item.subtotal}'
        for item in order.items.all()
    ]
    message = '\n'.join(
        [
            'A new order was submitted from the PawNest website.',
            '',
            f'Order number: {order.order_number}',
            f'Name: {order.customer_name}',
            f'Email: {order.email}',
            f'WhatsApp / phone: {order.phone}',
            f'Country: {order.country}',
            f'Address: {order.address}',
            f'Total: ${order.total_price}',
            '',
            'Items:',
            *item_lines,
            '',
            'Notes:',
            order.notes or '-',
            '',
            f'Admin record: /admin/core/order/{order.id}/change/',
        ]
    )
    return subject, message


def build_order_customer_email(order):
    subject = f'We received your PawNest order {order.order_number}'
    message = '\n'.join(
        [
            f'Hi {order.customer_name},',
            '',
            f'We received your order {order.order_number}.',
            'Our team will contact you to confirm payment, shipping, and availability before fulfillment.',
            '',
            f'Order total: ${order.total_price}',
            '',
            'Thank you,',
            'PawNest',
        ]
    )
    return subject, message


def send_order_notifications(order):
    recipient = getattr(settings, 'ORDER_NOTIFICATION_EMAIL', '')
    if not recipient:
        logger.warning('Order notification skipped because ORDER_NOTIFICATION_EMAIL is empty.')
        return False

    subject, message = build_order_admin_email(order)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )

    if getattr(settings, 'SEND_CUSTOMER_ORDER_EMAIL', True):
        customer_subject, customer_message = build_order_customer_email(order)
        send_mail(
            subject=customer_subject,
            message=customer_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )

    return True


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return JsonResponse({'products': [serialize_product(product) for product in products]})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return JsonResponse({'product': serialize_product(product)})


@csrf_exempt
@require_http_methods(['POST'])
def create_contract(request):
    payload = read_json_body(request)
    if payload is None:
        return JsonResponse({'message': 'Invalid request data.'}, status=400)

    try:
        if any(key in payload for key in ('name', 'email', 'country', 'interested_products', 'message')):
            name = clean_required(payload, 'name', 'name', 80)
            email = clean_email(payload)
            phone = clean_required(payload, 'phone', 'WhatsApp / phone', 40)
            country = clean_required(payload, 'country', 'country', 80)
            interested_products = clean_required(payload, 'interested_products', 'interested products')
            message = clean_required(payload, 'message', 'message')
            cleaned = {
                'name': name,
                'email': email,
                'phone': phone,
                'country': country,
                'interested_products': interested_products,
                'message': message,
                'source': str(payload.get('source', 'website-contact')).strip()[:80] or 'website-contact',
                'contact_name': name,
                'company_brand': str(payload.get('company_brand', '')).strip(),
                'project_type': 'Website inquiry',
                'requirement': message,
            }
        else:
            legacy_fields = {
                'contact_name': 'contact name',
                'phone': 'phone',
                'company_brand': 'company / brand',
                'project_type': 'project type',
                'estimated_quantity': 'estimated quantity',
                'delivery_city': 'delivery city',
                'budget_range': 'budget range',
                'requirement': 'requirement',
            }
            cleaned = {
                field: clean_required(payload, field, label)
                for field, label in legacy_fields.items()
            }
            cleaned.update(
                {
                    'name': cleaned['contact_name'],
                    'country': cleaned['delivery_city'],
                    'interested_products': cleaned['project_type'],
                    'message': cleaned['requirement'],
                    'source': 'legacy-contract-form',
                }
            )
    except ValueError as error:
        return JsonResponse({'message': str(error)}, status=400)

    contract = Contract.objects.create(**cleaned)
    email_sent = False
    try:
        email_sent = send_contract_notification(contract)
    except Exception:
        logger.exception('Failed to send contract notification email for contract id %s.', contract.id)

    return JsonResponse(
        {
            'message': 'Submitted successfully.',
            'id': contract.id,
            'email_sent': email_sent,
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(['POST'])
@transaction.atomic
def create_order(request):
    payload = read_json_body(request)
    if payload is None:
        return JsonResponse({'message': 'Invalid request data.'}, status=400)

    try:
        customer_name = clean_required(payload, 'customer_name', 'name', 80)
        email = clean_email(payload)
        phone = clean_required(payload, 'phone', 'WhatsApp / phone', 40)
        country = clean_required(payload, 'country', 'country', 80)
        address = clean_required(payload, 'address', 'address')
        notes = str(payload.get('notes', '')).strip()

        raw_items = payload.get('items')
        if not isinstance(raw_items, list) or not raw_items:
            raise ValueError('Your cart is empty.')

        order_items = []
        total_price = Decimal('0.00')
        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                raise ValueError('Invalid cart item.')
            product_slug = str(raw_item.get('product_slug', '')).strip()
            try:
                quantity = int(raw_item.get('quantity', 0))
            except (TypeError, ValueError):
                raise ValueError('Invalid item quantity.')
            if quantity < 1 or quantity > 99:
                raise ValueError('Item quantity must be between 1 and 99.')

            product = Product.objects.filter(slug=product_slug, is_active=True).first()
            if product is None:
                raise ValueError(f'Product is unavailable: {product_slug or "unknown"}.')

            unit_price = parse_display_price(product.price)
            subtotal = (unit_price * quantity).quantize(Decimal('0.01'))
            total_price += subtotal
            order_items.append((product, quantity, unit_price, subtotal))
    except ValueError as error:
        return JsonResponse({'message': str(error)}, status=400)

    order = Order.objects.create(
        order_number=build_order_number(),
        customer_name=customer_name,
        email=email,
        phone=phone,
        country=country,
        address=address,
        notes=notes,
        total_price=total_price.quantize(Decimal('0.01')),
    )
    for product, quantity, unit_price, subtotal in order_items:
        OrderItem.objects.create(
            order=order,
            product=product,
            product_slug=product.slug,
            product_name=product.name,
            unit_price=unit_price,
            display_price=product.price,
            quantity=quantity,
            subtotal=subtotal,
        )

    email_sent = False
    try:
        email_sent = send_order_notifications(order)
    except Exception:
        logger.exception('Failed to send order notification email for order id %s.', order.id)

    if email_sent != order.email_sent:
        order.email_sent = email_sent
        order.save(update_fields=['email_sent'])

    return JsonResponse(
        {
            'message': 'Order submitted successfully.',
            'order_number': order.order_number,
            'id': order.id,
            'email_sent': email_sent,
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(['POST'])
def subscribe_newsletter(request):
    payload = read_json_body(request)
    if payload is None:
        return JsonResponse({'message': 'Invalid request data.'}, status=400)

    email = str(payload.get('email', '')).strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'message': 'Please enter a valid email.'}, status=400)

    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={'source': str(payload.get('source', 'frontend')).strip()[:80] or 'frontend'},
    )
    return JsonResponse(
        {
            'message': 'Subscribed successfully.' if created else 'This email is already subscribed.',
            'id': subscriber.id,
            'created': created,
        },
        status=201 if created else 200,
    )
