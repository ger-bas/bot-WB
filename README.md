# bot-WB
Telegram bot for working with the [Wildberries](https://www.wildberries.ru/)
platform.

### Technologies
- Python
- Aiogram
- psycopg2
- SQLAlchemy
- PostgreSQL
- Docker

### Description
The bot retrieves information about the product from the trading platform.

- Name:   ...
- Vendor code:   ...
- Price: ...
- Rating:   ...
- Quantity:   ...
- Relevance: ✅ or ❌

To do this, you need to send the product article.
Data about the product is saved in the database, the next time there is a
request for the same article, the information is taken from the database.
After one day, product data is updated when you contact the bot.

Functional:

“Subscriptions for notifications”, information about one unit of goods comes
to the user in five minutes, and the data is updated automatically after the
 expiration date. Single product subscription available.

"Get information from the database", sends the last five records from
the database.

Logging. Bot logs are written to the logs/ directory.
Configured to rotate log files by day. The logging period is ten days.

### Deployment
Run the following commands on the server (during execution, the nano editor
will open, edit the line BOT_TOKEN=... , you can leave the rest as is)
```
git clone https://github.com/aleksanderstartsev1984/bot-WB.git -b deploy
cd bot-WB/
chmod o+x runprogect.sh
sudo nano .env
sudo sh ./runprogect.sh
```
Docker will be installed and containers will start.

Or do it yourself:
- install docker and docker compose
- create a new directory
- copy the docker-compose.yml file from this repository into it
- create a .env file with the following content

```
BOT_TOKEN=your bot token
POSTGRES_LOGIN=postgres
POSTGRES_PASSWORD=password
```
- run the command
```
docer compose up -d
```

In any case, the bot will work, good luck to you.

### Author
[Alexander Startsev](https://github.com/aleksanderstartsev1984)
