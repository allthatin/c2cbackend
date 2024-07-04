
from products.models import Products
from django.core.management.base import BaseCommand
from django.db import transaction
import csv

class Command(BaseCommand):
    help = "Insert AMD Ryzen products"
    def handle(self, *args, **options):
        product_list = []
        with open('./products/management/commands/amds.csv', 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['\ufeff"이름"']
                if "Ryzen™" in name:
                    if "(" in name:
                        name = name.split("Ryzen™ ",1)[1].split("(",1)[0].split(" ", -1)[1]
                    else:
                        try:
                            name = name.split("Ryzen™ ",1)[1].split(" ", -1)[1]
                        except:
                            name = name.split("Ryzen™ ",1)[1]
                else:
                    name = name
                product = Products()
                product.manufacturer = "AMD"
                product.model = name
                product.name = row['\ufeff"이름"'].split(product.model, 1)[0]
                product.cores = int(row['CPU 코어 수'] if row['CPU 코어 수'] != "" else 0)
                product.threads = int(row['스레드 수'] if row['스레드 수'] != "" else 0)
                product.turbo_boost_clock_rate_ghz = float(row['최대 부스트 클럭'].replace("최대 ","").replace("GHz", "").replace("MHz", "") if row['최대 부스트 클럭'] != "" else 0)
                product.base_clock_rate_ghz = float(row['기본 클럭'].replace("GHz", ""))
                product.gpu_model = row['그래픽 모델']
                product_list.append(product)

        with transaction.atomic():
            Products.objects.bulk_create(product_list, ignore_conflicts=True)

        print("AMD Ryzen products inserted successfully!")