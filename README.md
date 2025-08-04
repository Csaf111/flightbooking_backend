Here's a complete, professional `README.md` file for your [Flight Booking Backend](https://github.com/Csaf111/flightbooking_backend) project:

---

```markdown
# ✈️ Flight Booking Backend API

This is the backend API for the **Flight Booking System**, developed using **Flask** and **MongoDB**. The system allows users to search for flights, book tickets, and manage their reservations securely with JWT-based authentication.

---

## 🔧 Technologies Used

- **Python** (Flask)
- **MongoDB** (NoSQL database)
- **PyJWT** for authentication
- **Flask-CORS** for frontend integration
- **Flask-PyMongo** for MongoDB connection

---

## 📁 Project Structure

```

flightbooking\_backend/
│
├── app.py                # Main application file
├── auth.py               # User registration & login
├── flights.py            # Flight CRUD operations
├── bookings.py           # Booking management (create, update, delete)
├── config.py             # App configuration & secrets
├── utils.py              # Utility functions (token handling, validation)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

````

---

## 🚀 Features

- ✅ User registration and login (with hashed passwords)
- 🔐 JWT authentication and token validation
- ✈️ CRUD operations for managing flights
- 🧾 Create, view, update, and delete bookings
- 📦 JSON-based API responses
- 🌍 Cross-origin support for Angular frontend

---

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/Csaf111/flightbooking_backend.git
cd flightbooking_backend
````

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

Backend will run at: `http://127.0.0.1:5001`

---

## 🧪 API Endpoints

| Endpoint         | Method | Description                 |
| ---------------- | ------ | --------------------------- |
| `/register`      | POST   | Register a new user         |
| `/login`         | POST   | Login and receive JWT token |
| `/flights`       | GET    | Retrieve all flights        |
| `/flights`       | POST   | Add a new flight            |
| `/bookings`      | POST   | Book a flight               |
| `/bookings/<id>` | PUT    | Update a booking            |
| `/bookings/<id>` | DELETE | Cancel a booking            |
| `/mybookings`    | GET    | View user-specific bookings |

**All protected endpoints require `Authorization: Bearer <token>` in headers.**

---

## 🛠 Environment Variables (optional)

You can store sensitive data like secret keys in a `.env` file:

```
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://localhost:27017/flightbooking
```

---

## 🤝 Frontend Integration

This backend integrates seamlessly with the [Angular frontend](https://github.com/Csaf111/flightbooking_frontend) to provide a complete flight booking experience.

---

## 📌 License

This project is open-source under the MIT License.

---

## 👨‍💻 Author

**Safwan Chowdhury**
📧(https://www.linkedin.com/in/safwan-chowdhury)


