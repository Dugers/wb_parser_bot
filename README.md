# What's the Wildberries parser bot?
The Wildberries parser bot is a wrapper for [parser library](https://github.com/Dugers/wb_parser_lib)

![Work example](https://i.ibb.co/BVRbgHNs/example.png)
# Introductions

## How run?
1. Clone the reposiotry
```sh
git clone https://github.com/Dugers/wb_parser_bot.git
```
2. Setup env variables at `example.env` or `.env` (`BOT__TOKEN` and etc)
### Docker
1. Build the image
```sh
docker build -t wb_parser_bot .
```
2. Run the container
```sh
docker run wb_parser_bot
```
You can setup env while run docker container
```sh
docker run -e BOT__TOKEN=12345 wb_parser_bot
```
### Poetry
Run bot in production mode:
```sh
poetry run prod
```
Or use dev mode
```sh
poetry run dev
```