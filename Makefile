build:
	docker build -t chat-bot .

start:
	docker run -d -p 8080:8080 chat-bot

stop:
	docker stop $(shell docker ps -q --filter ancestor=chat-bot)
