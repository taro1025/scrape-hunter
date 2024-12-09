build:
	docker build -t selenium-script .

run:
	docker run --rm -v ./assets:/app/assets selenium-script
