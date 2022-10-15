# Ссылка на репозиторий

https://github.com/bekishev04/Async_API_sprint_2

### Запуск проекта
1. Заполнить во всех проектах .env по примеру .env.example
2. Запустить docker-compose.yml для запуска проекта

### Запуск api
1. Перейти в директорию AsyncApi
2. Заполнить .env по примеру .env.example
3. Установить зависимости poetry install
4. Войти в виртуальное окружение poetry shell
5. Запустить проект командой poetry run uvicorn --host=0.0.0.0 main:app --reload

### Запуск etl
1. Перейти в директорию etl
2. Заполнить .env по примеру .env.example
3. Установить зависимости poetry install
4. Войти в виртуальное окружение poetry shell
5. Запустить проект командой python main.py


### Запуск тестов
1. docker-compose -f docker-compose.test.yml up --build
