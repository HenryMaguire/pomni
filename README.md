# Pomni app
The pomni web app written using the Flask framework for Python and javascript/JQuery for the dynamic parts of the timer/notetaking app.

# Quick setup
- In terminal:
`git clone https://github.com/HenryMaguire/pomni.git`

- With Python 3 installed:

`source venv/bin/activate`

`venv/bin/pip install -r requirements.txt`

- Set some environment variables

`FLASK_APP=pomni.py`

`export FLASK_ENV=development`

- Make sure all the database initialisation and migration has been done with

`flask db init`

`flask db upgrade`

- Run the application with `flask run`

- View the app by typing localhost:5000 in your browser of choice.

# Docker deployment

- Create the mysql docker container for the database

`docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=pomni -e MYSQL_USER=pomni -e MYSQL_PASSWORD=<choose-password> mysql/mysql-server:5.7`
- Build the Pomni app docker container

`docker build -t pomni:latest .`

- Run the Pomni docker container


`docker run --name pomni -d -p 8000:5000 --link mysql:dbserver -e DATABASE_URL=mysql+pymysql://pomni:<choose-password>@dbserver/pomni pomni:latest`
