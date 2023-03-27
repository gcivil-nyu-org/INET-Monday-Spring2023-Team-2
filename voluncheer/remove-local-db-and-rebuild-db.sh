#AKA big red button
#BUT WE SHOULDN'T remove migration files now because that might impact our production database.
#find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
#find . -path "*/migrations/*.pyc"  -delete
#find . -path "*/migrations/*pycache*"  -delete
rm db.sqlite3
#This might be needed if django error occurs.
#pip uninstall -y Django
#pip install Django==3.2.8
./manage.py makemigrations
./manage.py migrate
#Load the data for categories.
./manage.py loaddata opportunityboard/fixtures/category_data.json
