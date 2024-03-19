# bot-WB
Telegram bot for working with the Wildberries platform.

### Technologies
- Python
- Aiogram
- psycopg2
- SQLAlchemy
- PostgreSQL

### Deployment
While in the root folder of the project, run the command
```
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

In the "data_base" directory create a ".env" file with user data:
```
PS_LOGIN=postgres
PS_PASSWORD=password
```

Installing postgres:
```
sudo apt install postgresql postgresql-contrib python3.10-dev libpq-dev
```

If you have problems connecting to the database, edit the configuration file:
```
sudo nano /etc/postgresql/14/main/pg_hba.conf
```
data:
```
# "local" is for Unix domain socket connections only
local   all             all                                     trust
```

Define a password for the postgres user:
```
sudo -u postgres psql -U postgres -d postgres -c "ALTER USER postgres PASSWORD 'password'"
```
