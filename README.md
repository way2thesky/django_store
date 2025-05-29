# 📚 Online Bookstore — Graduation Project at Hillel IT School
![Bookstore overview gif](readster.gif)

## 🧰 Technology Stack

- **Back-end:** Django 3.2, Django REST Framework (DRF), Celery, Redis, RabbitMQ  
- **Front-end:** Bootstrap, Ajax  
- **Infrastructure:** Docker, Docker Compose, Nginx  
- **Database:** PostgreSQL  
- **Payment:** Braintree  
- **Email Service:** Mailhog  
- **Architecture:** Microservice-based (Store + Warehouse)

---

## 🛒 Store Features

- 🔄 **Celery** – periodically synchronizes book availability from the warehouse
- 🧺 **Shopping Cart:**
  - Items are stored in the session
  - Users can't add more items than available in stock
- 📦 **Order Placement and Tracking**
- 💳 **Payment via Braintree**
- 📤 **Order transmission to the warehouse API in JSON format**
- 🔍 **Book Search and Genre Filtering**
- 👤 **User Registration and Authentication**
- 📬 **Email Notifications via Mailhog:**
  - When an order is placed
  - When an order is completed
- 💾 **Caching Support**
- 🛠️ **Admin Panel:**
  - Managers can add books and manage orders
- 🔗 **Warehouse API:**
  - Used by the store service to create and retrieve order data

---

## 🚀 Getting Started

## 1. Clone the repository:

```bash
git clone https://github.com/way2thesky/django_store.git
```

2. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

## 3. Build and run the containers:

```bash
docker-compose build --no-cache
docker-compose up
```

## 4. Access the app in your browser:

- Store: http://localhost 
- Warehouse (API): http://localhost:8001
- Mailhog: http://localhost:8025
- pgAdmin: http://localhost:5050

## 5. You can create a Django superuser for both services:

```
bash docker exec -it shop bash
python manage.py createsuperuser
``` 
Repeat the same for the warehouse container.

## 6. Load Initial Data (Optional)

```bash If you have a file db_shop.json, load it into the shop:
docker cp db_shop.json shop:/code/
docker exec -it shop bash
python manage.py loaddata db_shop.json
```
## Notes

- Media files (book covers) should be placed in store/media/products/...

- Nginx is configured to serve /media/ and /static/ correctly
## 📊 UML Diagram

![Bookstore overview jpg](graph.png)