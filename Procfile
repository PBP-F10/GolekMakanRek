web: gunicorn GolekMakanRek.wsgi 
release: python manage.py migrate && python manage.py loaddata data.json && python manage.py loaddata gofood_dataset.json && python manage.py loaddata merchant_gofood_dataset.json