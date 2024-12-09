web: gunicorn GolekMakanRek.wsgi 
release: python manage.py migrate && python manage.py loaddata data.json && python manage.py loaddata restaurant_data.json && python manage.py loaddata food_data.json