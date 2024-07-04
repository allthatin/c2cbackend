
from products.models import Products, Manufacturer
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

class Command(BaseCommand):
    help = "Insert products_manufacturer"
    def handle(self, *args, **options):
        qs = Products.objects.all()
        for product in qs:
            # search manufacturer field in product with Manufacturer model name using vector search
            vector = SearchVector('name')
            query = SearchQuery(product.manufacturer)
            queryset = Manufacturer.objects.all().annotate(rank=SearchRank(vector, query)).order_by('-rank')
            queryset = queryset.filter(rank__gt=0)
            if queryset.exists():
                manufacturer = queryset.first()
                product.manufacturer = manufacturer
                product.save()
            else:
                print(f"Manufacturer {product.manufacturer} not found")