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
...

### Author
[Alexander Startsev](https://github.com/aleksanderstartsev1984)
