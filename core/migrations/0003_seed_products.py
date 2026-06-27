from django.db import migrations


PRODUCTS = [
    {
        'slug': 'pino-feeder-set',
        'name': 'Pino Feeder Set',
        'category': 'Feeding',
        'price': '$42',
        'tag': 'Best seller',
        'tone': 'sage',
        'image_url': 'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?auto=format&fit=crop&w=900&q=80',
        'note': 'A low, weighted bowl set for cats and small dogs. Matte finish, soft edges, easy-clean base.',
        'material': 'Food-grade silicone, matte PP, anti-slip base',
        'care': 'Hand wash or gentle dishwasher cycle',
        'fit': 'Cats, puppies, toy breeds, apartment homes',
        'sort_order': 10,
    },
    {
        'slug': 'cloud-cleanup-kit',
        'name': 'Cloud Cleanup Kit',
        'category': 'Grooming',
        'price': '$36',
        'tag': 'New drop',
        'tone': 'blue',
        'image_url': 'https://images.unsplash.com/photo-1598134493179-51332e56807f?auto=format&fit=crop&w=900&q=80',
        'note': 'A tidy grooming starter set for shedding season, paw cleanup, and quick sofa resets.',
        'material': 'Soft-touch brush, reusable pouch, gentle cleanup cloth',
        'care': 'Rinse brush head and air dry after use',
        'fit': 'Cats, short-hair dogs, small-space grooming',
        'sort_order': 20,
    },
    {
        'slug': 'city-walk-bottle',
        'name': 'City Walk Bottle',
        'category': 'Walking',
        'price': '$28',
        'tag': 'Travel ready',
        'tone': 'clay',
        'image_url': 'https://images.unsplash.com/photo-1601758125946-6ec2ef64daf8?auto=format&fit=crop&w=900&q=80',
        'note': 'A compact bottle and treat loop for short walks, coffee runs, and weekend park time.',
        'material': 'Tritan bottle, silicone seal, recycled nylon loop',
        'care': 'Separate lid before washing',
        'fit': 'Small dogs, city walks, car trips',
        'sort_order': 30,
    },
    {
        'slug': 'new-pet-home-box',
        'name': 'New Pet Home Box',
        'category': 'Gift Sets',
        'price': '$78',
        'tag': 'Giftable',
        'tone': 'pink',
        'image_url': 'https://images.unsplash.com/photo-1574158622682-e40e69881006?auto=format&fit=crop&w=900&q=80',
        'note': 'A balanced starter bundle with feeding, grooming, and small storage pieces in one soft palette.',
        'material': 'Mixed pet-safe daily essentials with gift packaging',
        'care': 'Care card included by item',
        'fit': 'New pet parents, housewarming gifts, cat and small-dog homes',
        'sort_order': 40,
    },
]


def seed_products(apps, schema_editor):
    Product = apps.get_model('core', 'Product')
    for product in PRODUCTS:
        product_data = product.copy()
        slug = product_data.pop('slug')
        Product.objects.update_or_create(slug=slug, defaults=product_data)


def unseed_products(apps, schema_editor):
    Product = apps.get_model('core', 'Product')
    Product.objects.filter(slug__in=[product['slug'] for product in PRODUCTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_newslettersubscriber_product_alter_contract_options_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
