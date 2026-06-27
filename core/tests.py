import json
from unittest.mock import Mock, patch

from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django.test import Client, TestCase, override_settings

from .models import Contract, NewsletterSubscriber, Order, OrderItem, Product


class FailingEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        raise RuntimeError('SMTP unavailable')


@override_settings(ALLOWED_HOSTS=['testserver'])
class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_product_list_returns_active_products(self):
        Product.objects.create(
            slug='hidden-product',
            name='Hidden Product',
            category='Draft',
            price='$0',
            note='Draft item.',
            is_active=False,
        )

        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        product_ids = [product['id'] for product in payload['products']]
        self.assertIn('pino-feeder-set', product_ids)
        self.assertNotIn('hidden-product', product_ids)
        self.assertIn('numeric_price', payload['products'][0])

    def test_newsletter_subscribe_creates_subscriber(self):
        response = self.client.post(
            '/api/newsletter/',
            data=json.dumps({'email': 'buyer@example.com'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(NewsletterSubscriber.objects.filter(email='buyer@example.com').exists())

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CONTRACT_NOTIFICATION_EMAIL='renjiale549@gmail.com',
        DEFAULT_FROM_EMAIL='PawNest <test@example.com>',
    )
    def test_contract_submission_creates_new_inquiry_and_sends_email(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'interested_products': 'Pino Feeder Set',
                    'message': 'Need a feeding set sample.',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contract.objects.count(), 1)
        inquiry = Contract.objects.get()
        self.assertEqual(inquiry.email, 'mia@example.com')
        self.assertEqual(inquiry.contact_name, 'Mia')
        self.assertTrue(response.json()['email_sent'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['renjiale549@gmail.com'])
        self.assertIn('Mia', mail.outbox[0].subject)
        self.assertIn('Need a feeding set sample.', mail.outbox[0].body)
        self.assertNotIn('Legacy sourcing fields', mail.outbox[0].body)

    def test_contract_submission_rejects_invalid_email(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'name': 'Mia',
                    'email': 'not-an-email',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'interested_products': 'Pino Feeder Set',
                    'message': 'Need a feeding set sample.',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Contract.objects.count(), 0)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CONTRACT_NOTIFICATION_EMAIL='renjiale549@gmail.com',
        DEFAULT_FROM_EMAIL='PawNest <test@example.com>',
    )
    def test_legacy_contract_submission_still_works(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'contact_name': 'Mia',
                    'phone': '+1 555 000 0000',
                    'company_brand': 'PawNest QA',
                    'project_type': 'Private label',
                    'estimated_quantity': '500 pcs',
                    'delivery_city': 'Los Angeles',
                    'budget_range': '$1,000 - $3,000',
                    'requirement': 'Need a feeding set sample.',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contract.objects.count(), 1)
        self.assertTrue(response.json()['email_sent'])
        self.assertIn('Legacy sourcing fields', mail.outbox[0].body)

    @override_settings(
        EMAIL_BACKEND='core.tests.FailingEmailBackend',
        CONTRACT_NOTIFICATION_EMAIL='renjiale549@gmail.com',
    )
    def test_contract_submission_is_saved_when_email_fails(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'interested_products': 'Pino Feeder Set',
                    'message': 'Need a feeding set sample.',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contract.objects.count(), 1)
        self.assertFalse(response.json()['email_sent'])

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend',
        CONTRACT_NOTIFICATION_EMAIL='renjiale549@gmail.com',
    )
    def test_contract_submission_console_backend_is_not_marked_sent(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'interested_products': 'Pino Feeder Set',
                    'message': 'Need a feeding set sample.',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contract.objects.count(), 1)
        self.assertFalse(response.json()['email_sent'])

    @override_settings(
        EMAIL_DELIVERY_PROVIDER='resend',
        RESEND_API_KEY='re_test_key',
        RESEND_FROM_EMAIL='PawNest <onboarding@resend.dev>',
        CONTRACT_NOTIFICATION_EMAIL='renjiale549@gmail.com',
    )
    @patch('core.views.urllib.request.urlopen')
    def test_contract_submission_sends_email_with_resend(self, mock_urlopen):
        response_context = Mock()
        response_context.status = 200
        mock_urlopen.return_value.__enter__.return_value = response_context

        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'interested_products': 'Pino Feeder Set',
                    'message': 'Need a feeding set sample.',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['email_sent'])
        self.assertEqual(mock_urlopen.call_count, 1)
        request = mock_urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(request.headers['Authorization'], 'Bearer re_test_key')
        body = json.loads(request.data.decode('utf-8'))
        self.assertEqual(body['to'], ['renjiale549@gmail.com'])
        self.assertEqual(body['from'], 'PawNest <onboarding@resend.dev>')
        self.assertIn('Mia', body['subject'])
        self.assertIn('Need a feeding set sample.', body['text'])

    @override_settings(
        EMAIL_DELIVERY_PROVIDER='resend',
        RESEND_API_KEY='',
        CONTRACT_NOTIFICATION_EMAIL='renjiale549@gmail.com',
    )
    def test_contract_submission_resend_without_api_key_is_not_marked_sent(self):
        response = self.client.post(
            '/api/contracts/',
            data=json.dumps(
                {
                    'name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'interested_products': 'Pino Feeder Set',
                    'message': 'Need a feeding set sample.',
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.json()['email_sent'])

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        ORDER_NOTIFICATION_EMAIL='orders@example.com',
        SEND_CUSTOMER_ORDER_EMAIL=True,
        DEFAULT_FROM_EMAIL='PawNest <test@example.com>',
    )
    def test_order_submission_creates_order_items_and_sends_email(self):
        response = self.client.post(
            '/api/orders/',
            data=json.dumps(
                {
                    'customer_name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'address': '123 Pet Home St, Los Angeles, CA',
                    'notes': 'Please contact me by WhatsApp.',
                    'items': [{'product_slug': 'pino-feeder-set', 'quantity': 2}],
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertTrue(payload['order_number'].startswith('PN'))
        self.assertTrue(payload['email_sent'])
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.total_price, 84)
        self.assertEqual(order.items.get().product_name, 'Pino Feeder Set')
        self.assertEqual(order.items.get().quantity, 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, ['orders@example.com'])
        self.assertEqual(mail.outbox[1].to, ['mia@example.com'])

    def test_order_submission_rejects_empty_cart(self):
        response = self.client.post(
            '/api/orders/',
            data=json.dumps(
                {
                    'customer_name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'address': '123 Pet Home St',
                    'items': [],
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_submission_rejects_invalid_product(self):
        response = self.client.post(
            '/api/orders/',
            data=json.dumps(
                {
                    'customer_name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'address': '123 Pet Home St',
                    'items': [{'product_slug': 'missing-product', 'quantity': 1}],
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_submission_rejects_invalid_quantity(self):
        response = self.client.post(
            '/api/orders/',
            data=json.dumps(
                {
                    'customer_name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'address': '123 Pet Home St',
                    'items': [{'product_slug': 'pino-feeder-set', 'quantity': 0}],
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    @override_settings(
        EMAIL_BACKEND='core.tests.FailingEmailBackend',
        ORDER_NOTIFICATION_EMAIL='orders@example.com',
    )
    def test_order_submission_is_saved_when_email_fails(self):
        response = self.client.post(
            '/api/orders/',
            data=json.dumps(
                {
                    'customer_name': 'Mia',
                    'email': 'mia@example.com',
                    'phone': '+1 555 000 0000',
                    'country': 'United States',
                    'address': '123 Pet Home St',
                    'items': [{'product_slug': 'pino-feeder-set', 'quantity': 1}],
                }
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertFalse(response.json()['email_sent'])
