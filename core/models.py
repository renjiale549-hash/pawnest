from django.db import models
from django.utils import timezone


class Contract(models.Model):
    name = models.CharField('姓名', max_length=80, blank=True, default='')
    email = models.EmailField('邮箱', blank=True, default='')
    phone = models.CharField('WhatsApp / 电话', max_length=40)
    country = models.CharField('国家', max_length=80, blank=True, default='')
    interested_products = models.TextField('感兴趣商品', blank=True, default='')
    message = models.TextField('留言', blank=True, default='')
    source = models.CharField('来源', max_length=80, default='website')
    created_at = models.DateTimeField('提交时间', default=timezone.now)

    # Legacy sourcing fields are kept so existing records and older API callers remain valid.
    contact_name = models.CharField('旧版联系人姓名', max_length=80, blank=True, default='')
    company_brand = models.CharField('公司 / 品牌', max_length=120, blank=True, default='')
    project_type = models.CharField('项目类型', max_length=80, blank=True, default='')
    estimated_quantity = models.CharField('预计数量', max_length=80, blank=True, default='')
    delivery_city = models.CharField('收货城市', max_length=80, blank=True, default='')
    budget_range = models.CharField('预算范围', max_length=80, blank=True, default='')
    requirement = models.TextField('需求说明', blank=True, default='')

    class Meta:
        db_table = 'contract'
        ordering = ('-created_at', '-id')
        verbose_name = '询盘'
        verbose_name_plural = '询盘'

    def __str__(self):
        display_name = self.name or self.contact_name or '询盘'
        display_context = self.country or self.company_brand or self.email
        return f'{display_name} - {display_context}'.strip(' -')


class Product(models.Model):
    slug = models.SlugField('商品别名', max_length=80, unique=True)
    name = models.CharField('商品名称', max_length=120)
    category = models.CharField('分类', max_length=80)
    price = models.CharField('展示价格', max_length=40)
    tag = models.CharField('商品标签', max_length=80, blank=True)
    tone = models.CharField('色调', max_length=40, blank=True)
    image_url = models.URLField('图片地址', max_length=500, blank=True)
    note = models.TextField('简短描述')
    material = models.CharField('材质', max_length=240, blank=True)
    care = models.CharField('护理说明', max_length=240, blank=True)
    fit = models.CharField('适用范围', max_length=240, blank=True)
    sort_order = models.PositiveIntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ('sort_order', 'id')
        verbose_name = '商品'
        verbose_name_plural = '商品'

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField('邮箱', unique=True)
    source = models.CharField('来源', max_length=80, default='frontend')
    created_at = models.DateTimeField('订阅时间', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = '邮件订阅'
        verbose_name_plural = '邮件订阅'

    def __str__(self):
        return self.email


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_NEW, '新订单'),
        (STATUS_CONTACTED, '已联系'),
        (STATUS_CONFIRMED, '已确认'),
        (STATUS_CANCELLED, '已取消'),
    )

    order_number = models.CharField('订单编号', max_length=24, unique=True, blank=True)
    customer_name = models.CharField('姓名', max_length=80)
    email = models.EmailField('邮箱')
    phone = models.CharField('WhatsApp / 电话', max_length=40)
    country = models.CharField('国家', max_length=80)
    address = models.TextField('地址')
    notes = models.TextField('备注', blank=True, default='')
    total_price = models.DecimalField('总价', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    email_sent = models.BooleanField('邮件已发送', default=False)
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ('-created_at', '-id')
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return f'{self.order_number or "订单"} - {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    product_slug = models.SlugField('商品别名', max_length=80)
    product_name = models.CharField('商品名称', max_length=120)
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2)
    display_price = models.CharField('展示价格', max_length=40)
    quantity = models.PositiveIntegerField('数量')
    subtotal = models.DecimalField('小计', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'
