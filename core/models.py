from django.db import models
from django.utils import timezone


class Contract(models.Model):
    name = models.CharField('Name', max_length=80, blank=True, default='')
    email = models.EmailField('Email', blank=True, default='')
    phone = models.CharField('WhatsApp / Phone', max_length=40)
    country = models.CharField('Country', max_length=80, blank=True, default='')
    interested_products = models.TextField('Interested products', blank=True, default='')
    message = models.TextField('Message', blank=True, default='')
    source = models.CharField('Source', max_length=80, default='website')
    created_at = models.DateTimeField('Submitted at', default=timezone.now)

    # Legacy sourcing fields are kept so existing records and older API callers remain valid.
    contact_name = models.CharField('Legacy contact name', max_length=80, blank=True, default='')
    company_brand = models.CharField('Company / brand', max_length=120, blank=True, default='')
    project_type = models.CharField('Project type', max_length=80, blank=True, default='')
    estimated_quantity = models.CharField('Estimated quantity', max_length=80, blank=True, default='')
    delivery_city = models.CharField('Delivery city', max_length=80, blank=True, default='')
    budget_range = models.CharField('Budget range', max_length=80, blank=True, default='')
    requirement = models.TextField('Requirement', blank=True, default='')

    class Meta:
        db_table = 'contract'
        ordering = ('-created_at', '-id')
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        display_name = self.name or self.contact_name or 'Inquiry'
        display_context = self.country or self.company_brand or self.email
        return f'{display_name} - {display_context}'.strip(' -')


class Product(models.Model):
    slug = models.SlugField('Product slug', max_length=80, unique=True)
    name = models.CharField('Product name', max_length=120)
    category = models.CharField('Category', max_length=80)
    price = models.CharField('Display price', max_length=40)
    tag = models.CharField('Product tag', max_length=80, blank=True)
    tone = models.CharField('Color tone', max_length=40, blank=True)
    image_url = models.URLField('Image URL', max_length=500, blank=True)
    note = models.TextField('Short description')
    material = models.CharField('Material', max_length=240, blank=True)
    care = models.CharField('Care', max_length=240, blank=True)
    fit = models.CharField('Fit', max_length=240, blank=True)
    sort_order = models.PositiveIntegerField('Sort order', default=0)
    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        ordering = ('sort_order', 'id')
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField('Email', unique=True)
    source = models.CharField('Source', max_length=80, default='frontend')
    created_at = models.DateTimeField('Subscribed at', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Newsletter subscriber'
        verbose_name_plural = 'Newsletter subscribers'

    def __str__(self):
        return self.email


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_CONTACTED, 'Contacted'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
    )

    order_number = models.CharField('Order number', max_length=24, unique=True, blank=True)
    customer_name = models.CharField('Name', max_length=80)
    email = models.EmailField('Email')
    phone = models.CharField('WhatsApp / Phone', max_length=40)
    country = models.CharField('Country', max_length=80)
    address = models.TextField('Address')
    notes = models.TextField('Notes', blank=True, default='')
    total_price = models.DecimalField('Total price', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    email_sent = models.BooleanField('Email sent', default=False)
    created_at = models.DateTimeField('Submitted at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        ordering = ('-created_at', '-id')
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.order_number or "Order"} - {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    product_slug = models.SlugField('Product slug', max_length=80)
    product_name = models.CharField('Product name', max_length=120)
    unit_price = models.DecimalField('Unit price', max_digits=10, decimal_places=2)
    display_price = models.CharField('Display price', max_length=40)
    quantity = models.PositiveIntegerField('Quantity')
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = 'Order items'

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'
