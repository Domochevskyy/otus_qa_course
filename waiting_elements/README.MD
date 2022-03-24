### Запуск тестов

1. Поднять контейнеры
    ```
    $ make up
    ```
2. Запустить тесты
   ```
   $ pytest [PYTEST_OPTIONS] --browser=[BROWSER_NAME] --url=[URL_FOR_OPENCART] --driver_path=[PATH_TO_DRIVER]
   ```
3. Остановить контейнеры
   ```
   $ make down
   ```
4. Удалить все остановленные контейнеры
   ```
   $ docker system prune -a
   ```
5. Удалить все тома
   ```
   $ docker volume prune
   ```