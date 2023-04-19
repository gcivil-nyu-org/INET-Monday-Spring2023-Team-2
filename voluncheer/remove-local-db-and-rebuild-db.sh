rm db.sqlite3
./manage.py makemigrations
./manage.py migrate
#Load the data for categories.
./manage.py loaddata opportunityboard/fixtures/category_data.json
./manage.py loaddata profiles/fixtures/badge_data.json
#start docker daemon with "dockerd". If on macOS or windows, open docker desktop by clicking on it instead.
#Open redis server with docker container, but your docker daemon has to be running first.
docker run -p 6379:6379 -d redis:5
