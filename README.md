Online Bookstore built with Django and DRF
![Bookstore overview gif](readster.gif)

# Выпускной проект во время обучения в Hillel IT School 
## Technology Stack:
* Django, DRF, Ajax, Docker, Docker Compose, Nginx, PostgreSQL, Redis, Rabbitmq, Celery, Mailhog, Bootstrap, BRAINTREE, Microservice architecture


## Функции Магазина
* Celery - периодически синхронизирует наличие книг из склада в магазин
* Корзина (Пользователь не может добавить в корзину больше чем есть в наличие, Товар хранится в сессии)
* Оформление заказа
* Оплата
* Отправка заказа в API хранилища в формате json.
* Возможность отследить заказ
* Поиск
* Регистрация
* Фильтрация Книг по жанрам
* PostgreSQL 
* Есть кеширование

## Mailhog - получает почту за пользователя о том что заказ оформлен и о том что заказ выполнен.

## Функции Api - используется магазином что бы создать заказ
* Admin и Api. Менеджер иметь возможность через адмику добавлять книги (инстансы книг) и обрабатывать пришедшие заказы. 
* PostgreSQL 

## Использование

1. Клонируем репозиторий с гитхаба

    ```bash
    git clone git@github.com:way2thesky/quiz_app.git
    ```

2. Устанавливаем docker и docker-compose

3. Запускаем докер контейнеры и проект
    ```bash
       docker-compose build
      ```
    ```bash
       docker-compose up
      ```
## Приложение запущенно и доступно на порту 8000 Магазин / 8001 Склад


# Схема UML проекта </p>
![Bookstore overview jpg](graph.png)
