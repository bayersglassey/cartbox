
from .models import Category, Product


CATS_AND_PRODS = [
    {
        'title': "Fruit",
        'products': [
            # From http://www.bobbywires.com/plu-1.php
            {'sku': '4011', 'title': "Banana Yellow"},
            {'sku': '4101', 'title': "Apple Braeburn"},
            {'sku': '4104', 'title': "Apple Cortland"},
            {'sku': '4107', 'title': "Apple Crab"},
            {'sku': '3010', 'title': "Apple Cripps"},
            {'sku': '3621', 'title': "Mango Francis"},
            {'sku': '4311', 'title': "Mango Green"},
            {'sku': '4051', 'title': "Mango Red"},
        ],
    },
    {
        'title': "Veg",
        'products': [
            # From http://www.bobbywires.com/plu-1.php
            {'sku': '4560', 'title': "Carrots Baby"},
            {'sku': '4562', 'title': "Carrots Loose"},
            {'sku': '4070', 'title': "Celery Bunch"},
            {'sku': '4575', 'title': "Celery Hearts"},
            {'sku': '4552', 'title': "Cabbage Napa"},
            {'sku': '4069', 'title': "Cabbage Green"},
            {'sku': '4554', 'title': "Cabbage Red"},
        ],
    },
    {
        'title': "Meat",
        'products': [
            # From http://gleibermans.com/Meat.pdf
            {'sku': '200029', 'title': "Beef Patties"},
            {'sku': '210027', 'title': "Beef Ribs"},
            {'sku': '210022', 'title': "Beef Stew"},
            {'sku': '210001', 'title': "Ground Beef"},
            {'sku': '210002', 'title': "Ground Beef Lean"},
            {'sku': '210007', 'title': "Ground Veal"},
            {'sku': '200015', 'title': "Marrow Bones"},
            {'sku': '200632', 'title': "Veal Roast"},
            {'sku': '220009', 'title': "Veal Brisket"},
            {'sku': '210014', 'title': "Rib Roast Bone In"},
            {'sku': '210017', 'title': "Top of Rib"},
            {'sku': '200006', 'title': "Whole Brisket"},
        ],
    },
]

def updated_or_created(created, thing):
    msg = "Created" if created else "Updated"
    print("{} {}: {}".format(
        msg, thing._meta.verbose_name, thing))

def update_or_create_cats_and_prods():
    cats = []
    prods = []
    for cat_data in CATS_AND_PRODS:
        title = cat_data['title']
        prod_datas = cat_data['products']
        cat, created = Category.objects.update_or_create(
            title=title)
        updated_or_created(created, cat)
        cats.append(cat)
        for prod_data in prod_datas:
            sku = prod_data['sku']
            title = prod_data['title']
            prod, created = Product.objects.update_or_create(
                sku=sku, defaults=dict(
                    category=cat, title=title))
            updated_or_created(created, prod)
            prods.append(prod)
    return cats, prods


