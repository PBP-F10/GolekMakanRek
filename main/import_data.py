# GolekMakanRek/main/import_data.py

import os
import django
import csv
import sys
# Set up Django environment
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GolekMakanRek.settings')
django.setup()

from main.models import Food, Restaurant

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
    print(f'Successfully imported data from {file_path} into Restaurant model.')

def import_foods(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Get the restaurant associated with the food
            try:
                restaurant = Restaurant.objects.get(nama=row['merchant_name'])
            except Restaurant.DoesNotExist:
                print(f"Restaurant {row['merchant_name']} not found. Skipping food item.")
                continue

            # Importing Food data
            Food.objects.create(
                nama=row['product'],
                kategori=row['category'],
                harga=int(row['price']),
                diskon=int(row['discount_price']) if row['isDiscount'].lower() == 'true' else 0,
                deskripsi=row['description'],
                restoran=restaurant
            )
    print(f'Successfully imported data from {file_path} into Food model.')

if __name__ == '__main__':
    # Paths to the CSV files
    restaurant_file_path = './merchant_gofood_dataset.csv'  # Update with actual path
    food_file_path = './gofood_dataset.csv'  # Update with actual path

    # Import data
    import_restaurants(restaurant_file_path)
    import_foods(food_file_path)
