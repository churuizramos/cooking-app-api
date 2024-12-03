# Python Backend
Requires Python3.12 to work.

Create a file `db_config.py` to store the values `db_host`, `db_user`, `db_password`, and `db_database` which are used in the app.py to connect to the MySQL server. Message me for the login.

Installing Python3.12 (For Debian)
```sh
sudo apt update
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget curl
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tar.xz
tar -xf Python-3.12.0.tar.xz
cd Python-3.12.0
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1
sudo update-alternatives --config python3
```
Cannot guarantee the viability of running all of this in one paste. Note to self...

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
pip install pymysql flask flask-cors
```

Run the app.py to start the API server
```sh
python app.py
```
