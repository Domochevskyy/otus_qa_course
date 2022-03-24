CHROME_DRIVER_PATH ?=
FIREFOX_DRIVER_PATH ?=
TEST_DIR ?=


up:
	OPENCART_PORT=8081	\
	PHPADMIN_PORT=8888	\
	LOCAL_IP=`hostname -I | grep -o "^[0-9.]*"`	\
	docker-compose up  -d

down:
	OPENCART_PORT=8081	\
	PHPADMIN_PORT=8888	\
	LOCAL_IP=`hostname -I | grep -o "^[0-9.]*"`	\
	docker-compose down