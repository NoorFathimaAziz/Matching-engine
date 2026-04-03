# Matching Engine: Django High-Performance Matching Engine

## 1. Use Case
Matching Engine is a production-grade **Trading Matching Engine**. Its primary purpose is to facilitate the exchange of assets between buyers and sellers. It acts as the "brain" of a financial exchange, ensuring that trades are executed fairly, quickly, and accurately based on market demand.

## Key Use Case:
- **High-Frequency Trading**: Handling thousands of orders per second.
- **Price Discovery**: Determining the market price based on the highest bid and lowest ask.
- **Order Fulfillment**: Automatically matching compatible orders to settle trades.

---

## 2. End-to-End Project Flow
1.  **Order Placement**: A user submits a Buy or Sell order via the REST API.
2.  **Validation**: The system checks if the price and quantity are valid.
3.  **Persistence**: The order is saved to the PostgreSQL database with a `PENDING` status.
4.  **Locking**: The system locks the "Order Book" for that specific asset to prevent race conditions.
5.  **Matching**: The engine compares the new order against existing orders using **Price-Time Priority**.
6.  **Execution**: If a match is found, a `Trade` record is created, and the order quantities are updated.
7.  **Completion**: The user receives a response confirming the order status and any executed trades.

---

## 3. Project Structure
This project follows **MNC-grade SOLID principles** and the **Service-Repository Pattern**:

- **`matching_engine/core/`**: **Domain Logic**. Contains the pure Python matching algorithm. It is completely independent of Django, making it highly portable and testable.
- **`matching_engine/services/`**: **Application Layer**. Orchestrates the flow between the API and the Core logic. It manages **ACID transactions**.
- **`matching_engine/repositories/`**: **Data Access Layer**. Handles all database queries and row-level locking (`select_for_update`).
- **`matching_engine/api/`**: **Interface Layer**. Contains DRF Views and Serializers for external communication.
- **`matching_engine/models/`**: **Data Layer**. Defines the PostgreSQL schema for Orders and Trades.
- **`matching_engine/middleware/`**: **System Layer**. Custom middleware for performance tracking and logging.

---

## 4. Tech Stack
- **Framework**: Django 5.0 + DRF
- **Database**: PostgreSQL
- **Concurrency**: Row-level locking (ACID compliant)
- **Architecture**: Service-Repository Pattern
- **Server**: Gunicorn (Production ready)

---

## 5. Local Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 
- `pip` and `virtualenv`

### 1. Clone & Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration
The project is pre-configured to use a ** PostgreSQL** database. You can find the connection string in `config/settings.py`. If you wish to use your own, update the `DATABASES` setting.

### 3. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
The server will be available at `http://127.0.0.1:8000/`.

---

## 6. API Documentation

### 1. Place a New Order
**Endpoint:** `POST /api/orders/`  
**Payload:**
```json
{
    "user_id": "user_123",
    "side": "BUY",
    "price": 150.50,
    "quantity": 10.0
}
```

### 2. View Order Book
**Endpoint:** `GET /api/orderbook/`  

### 3. View list of Orders
**Endpoint:** `GET /api/order/list`  


### 3. View list of Trades
**Endpoint:** `GET /api/trades/`  

---

## 7. Deployment Guide

