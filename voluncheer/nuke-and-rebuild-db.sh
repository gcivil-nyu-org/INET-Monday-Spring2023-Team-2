#nuke the existing databse and remigrate everything
#AKA big red button
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/migrations/*pycache*"  -delete
rm db.sqlite3
#pip uninstall -y Django
#pip install Django==3.2.8
git checkout origin/develop -- db.sqlite3
mv db.sqlite3 dbTemp.sqlite3
./manage.py makemigrations
./manage.py migrate
#Dump data
sqlite3 dbTemp.sqlite3 ".dump opportunityboard_category" |sqlite3 db.sqlite3
sqlite3 dbTemp.sqlite3 ".dump opportunityboard_opportunity" |sqlite3 db.sqlite3
sqlite3 dbTemp.sqlite3 ".dump opportunityboard_subcategory" |sqlite3 db.sqlite3
sqlite3 dbTemp.sqlite3 ".dump opportunityboard_subsubcategory" |sqlite3 db.sqlite3
rm dbTemp.sqlite3