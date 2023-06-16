build:
	docker build -t sql-live-coding .

run:
	docker run --rm -p 8501:8501 --env-file .env sql-live-coding

stop:
	docker stop $$(docker ps -q --filter ancestor=sql-live-coding)
