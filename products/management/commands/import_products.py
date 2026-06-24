import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "Import products from CSV"

    def handle(self, *args, **kwargs):
        df = pd.read_csv('products_data.csv')

        for _, row in df.iterrows():
            Product.objects.get_or_create(
                product_id=row['id'],
                defaults={
                    'name': row['product_name'],
                    'category': row['category'],
                    'tags': row['tags'],
                    'description': row['product_description']
                    }
                )

        self.stdout.write(self.style.SUCCESS("Products imported successfully!"))