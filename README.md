This project uses LibraryWiki as a submodule so need to use "git clone --recursive ..." to get it.

then run first:
pip3 install -r LibraryWiki/requirements.txt
pip3 install -r requirements.txt


Frontend development instructions:
    
    cd frontend
    pip install -r requirements-dev.txt
    python manage.py migrate
    python manage.py import_alto_data
    python manage.py runserver

