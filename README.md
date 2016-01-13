Frontend development instructions:
    
    cd frontend
    pip install -r requirements-dev.txt
    python manage.py migrate
    python manage.py import_alto_data
    python manage.py runserver
