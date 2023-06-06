install:
	pip install -r requirements.txt
save:
	pip freeze > requirements.txt
create_db:
	docker run -d --name redis-stack-server -p 6380:6379 redis/redis-stack-server:latest
run:
	flask run