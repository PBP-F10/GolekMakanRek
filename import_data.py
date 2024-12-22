import os
import django
import csv
import sys
import logging

# Set up Django environment
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GolekMakanRek.settings')
django.setup()

from main.models import Food, Restaurant

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_restaurants(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Importing Restaurant data
            restaurant, created = Restaurant.objects.get_or_create(
                nama=row['merchant_name'],
                defaults={
                    'kategori': row['category'],
                    'deskripsi': row['merchant_description']
                }
            )
            if created:
                logger.info(f"Created restaurant: {restaurant.nama}")
            else:
                logger.info(f"Restaurant already exists: {restaurant.nama}")
    logger.info(f'Successfully imported data from {file_path} into Restaurant model.')

def import_foods(file_path):
    food_items = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Get the restaurant associated with the food
            try:
                restaurant = Restaurant.objects.get(nama=row['merchant_name'])
            except Restaurant.DoesNotExist:
                logger.warning(f"Restaurant {row['merchant_name']} not found. Skipping food item: {row['product']}.")
                continue
            
            # Prepare Food data
            food_item = Food(
                nama=row['product'],
                kategori=row['category'],
                harga=int(row['price']),
                diskon=int(row['discount_price']) if row['isDiscount'].lower() == 'true' else 0,
                deskripsi=row['description'],
                restoran=restaurant
            )
            food_items.append(food_item)

    # Bulk create Food items
    Food.objects.bulk_create(food_items)
    logger.info(f'Successfully imported {len(food_items)} food items from {file_path} into Food model.')

if __name__ == '__main__':
    # Paths to the CSV files
    restaurant_file_path = './merchant_gofood_dataset.csv'  # Update with actual path
    food_file_path = './gofood_dataset.csv'  # Update with actual path

    # Import data
    import_restaurants(restaurant_file_path)
    import_foods(food_file_path)
