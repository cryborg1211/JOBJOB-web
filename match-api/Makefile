dev:
	uvicorn main:app --reload --port 8000

docker-build:
	docker build -t match-api:latest .

docker-run:
	docker run --rm -p 8000:8000 --env-file .env -v ${PWD}/artifacts:/app/artifacts match-api:latest


