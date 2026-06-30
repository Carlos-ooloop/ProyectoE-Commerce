# E-COMMERCE API ( FastAPI + Docker + MySQL )
A backend API for an e-commerce system built with FastAPI, modular architecture, MySQL, and containerized using Docker. It includes user management, product catalog, inventory control, orders, payments, and an audit logging system.
## TECH STACK:
·FastAPI
·SQLAlchemy ORM
·MySQL 8.0
·Pydantic
·Docker & Docker Compose
·Uvicorn
·Python 3.12+

## PROJECT ARCHITECTURE:
app/
│
├── models/        · SQLAlchemy models (User, Order, Payment, etc.)
├── schemas/       · Pydantic validation schemas
├── routers/       · API endpoints (CRUD routes)
├── services/      · Business logic (Orders, Payments)
├── db/            · Database configuration
├── utils/         · Auth, helpers
├── seed_script.py · Initial data seeding

## KEY FEATURES:
### USERS:
·User registration and authentication
·Role-based access (admin / user)

### Products & Categories:
·Full CRUD for products
·Predefined categories
·Inventory management

### Orders:
·Create orders with multiple items
·Automatic total calculation
·Order ↔ OrderItems relationship

### Payments:
·Simulated payment processing
·Extensible providers (fake, Stripe, PayPal ready)
·Payment states (pending, success, failed)

### Order State Machine:
·pending_payment
·paid
·cancelled
·shipped (extensible)

### Audit Logs (Stripe-like):
Event tracking for:
·Order creation
·Payments
·Status changes
·User actions

### Running with Docker:
1. Clone the repository
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
2. Create .env file
DATABASE_URL=mysql+pymysql://root:1234@db:3306/ecommerce
3. Start containers
docker compose up --build
4. Access the API
API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs


### Docker Services:
·API Service
·FastAPI application running on port 8000
·Database Service
·MySQL 8.0
·Persistent storage via Docker volumes


### System Design
Order Flow
User → Create Order → OrderItems → Payment → Update Order Status → Audit Log
Payment Flow
Create Payment
   ↓
Validate Order
   ↓
Fake Payment Provider (success/failure)
   ↓
Update Payment Status
   ↓
Update Order State
   ↓
Create Audit Log Event


### Advanced Features
·Order State Machine
·Decoupled payment service
·Audit logging system (Stripe-inspired)
·Layered / clean-ish architecture
·Fully containerized with Docker
·Ready for microservices evolution


### Seed Data

Includes a seed script that creates:

·Admin user
Default categories:
·Electronics
·Food
·Cleaning
·Home
·python seed_script.py

### Security
·Password hashing
·Role-based access control
·Authentication-ready structure (JWT extensible)
·Protected service layers

### Future Improvements
 ·Stripe integration
 ·Pytest test suite
 ·Pagination for endpoints
 ·Redis caching layer
 ·Advanced logging (ELK stack)
 ·Deployment (AWS / Render / Railway)
 ·CI/CD with GitHub Actions
### Author

This project was built as an advanced backend engineering practice focused on scalable architecture, clean design, and real-world system patterns












