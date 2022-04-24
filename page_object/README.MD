### Запуск тестов

2. Поднять контейнеры
    ```
    $ make up
    ```
3. Запустить тесты
   ```
   $ pytest [PYTEST_OPTIONS] --browser=[BROWSER_NAME] --url=[URL_FOR_OPENCART] --driver_path=[PATH_TO_DRIVER]
   ```
   или
   ```
   $ make tests
   ```
4. Остановить контейнеры
   ```
   $ make down
   ```
5. Удалить все остановленные контейнеры
   ```
   $ docker system prune -a
   ```
6. Удалить все тома
   ```
   $ docker volume prune
   ```