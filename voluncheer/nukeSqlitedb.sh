#nuke the existing databse and remigrate everything
#AKA big red button
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
pip3 uninstall -y Django
pip3 install Django==3.2.8
./manage.py makemigrations
./manage.py migrate