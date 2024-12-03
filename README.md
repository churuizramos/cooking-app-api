# Python Backend
Requires Python3.12 to work.

Create a file `db_config.py` to store the values `db_host`, `db_user`, `db_password`, and `db_database` which are used in the app.py to connect to the MySQL server. Message me for the login.

Create a venv locally
```sh
python3.12 -m venv venv
```

Run the venv
```sh
source venv/bin/activate
```

Install dependencies
```sh
pip install pymysql flask
```

Run the app.py to start the API server
```sh
python app.py
```