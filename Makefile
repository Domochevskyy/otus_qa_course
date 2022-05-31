CHROME_DRIVER_PATH ?=
FIREFOX_DRIVER_PATH ?=
TEST_DIR ?=


up:
	OPENCART_PORT=8081	\
	PHPADMIN_PORT=8888	\
	LOCAL_IP=`hostname -I | grep -o "^[0-9.]*"`	\
	docker-compose up  -d

tests:
	docker build --tag tests .
	docker run --name my_first_container_from_dockerfile \
			   --network selenoid \
			   --privileged	\
			   tests pytest
	docker cp my_first_container_from_dockerfile:/app/allure-results .
	docker rm my_first_container_from_dockerfile
allure:
	allure generate --clean && allure open
down:
	OPENCART_PORT=8081	\
	PHPADMIN_PORT=8888	\
	LOCAL_IP=`hostname -I | grep -o "^[0-9.]*"`	\
	docker-compose down
