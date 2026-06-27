from django.contrib import admin

from .models import Contract, NewsletterSubscriber, Order, OrderItem, Product

admin.site.site_header = 'PawNest 后台管理'
admin.site.site_title = 'PawNest 后台'
admin.site.index_title = '运营管理'


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    actions = None
    list_display_links = ('display_name',)
    list_display = (
        'display_name',
        'email',
        'phone',
        'country',
        'interested_products',
        'source',
        'created_at',
    )
    fields = (
        'name',
        'email',
        'phone',
        'country',
        'interested_products',
        'message',
        'source',
        'created_at',
        'contact_name',
        'company_brand',
        'project_type',
        'estimated_quantity',
        'delivery_city',
        'budget_range',
        'requirement',
    )
    readonly_fields = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'country', 'interested_products', 'message')
    list_filter = ('country', 'source', 'created_at')
    ordering = ('-created_at', '-id')
    list_per_page = 20

    @admin.display(description='姓名')
    def display_name(self, obj):
        return obj.name or obj.contact_name or '询盘'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('name', 'category', 'price', 'tag', 'sort_order', 'is_active', 'updated_at')
    list_editable = ('sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category', 'tag', 'note')
    list_filter = ('category', 'is_active')
    ordering = ('sort_order', 'id')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_slug', 'product_name', 'unit_price', 'display_price', 'quantity', 'subtotal')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = None
    inlines = (OrderItemInline,)
    list_display = ('order_number', 'customer_name', 'email', 'country', 'total_price', 'status', 'email_sent', 'created_at')
    list_display_links = ('order_number',)
    list_editable = ('status',)
    fields = (
        'order_number',
        'status',
        'customer_name',
        'email',
        'phone',
        'country',
        'address',
        'notes',
        'total_price',
        'email_sent',
        'created_at',
        'updated_at',
    )
    readonly_fields = ('order_number', 'total_price', 'email_sent', 'created_at', 'updated_at')
    search_fields = ('order_number', 'customer_name', 'email', 'phone', 'country', 'address')
    list_filter = ('status', 'country', 'email_sent', 'created_at')
    ordering = ('-created_at', '-id')
    list_per_page = 20


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('email', 'source', 'created_at')
    search_fields = ('email',)
    list_filter = ('source', 'created_at')
    ordering = ('-created_at',)
