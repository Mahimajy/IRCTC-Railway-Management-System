

# IRCTC Railway Management System

This project is a simplified railway management system API that allows users to check train availability, book seats, and retrieve booking details. Admin users can manage train details such as adding new trains.

## Features
- User Registration and Login
- Role-based access control for Admin and User roles
- Admin operations:
  - Add new trains
- User operations:
  - Check train availability
  - Book a seat on a train
  - Retrieve booking details
- Handles race conditions during seat booking

## Tech Stack
- **Backend Framework**: Flask (Python)
- **Database**: SQLite (default; configurable to MySQL/PostgreSQL)
- **Authentication**: JWT for user authentication, API key for admin endpoints

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup
1. Clone the repository:
   ```bash
   git clone <https://github.com/Mahimajy/WorkIndia>
   cd irctc-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python app.py
   ```
   This will create an SQLite database `irctc.db` with the necessary tables.

## Running the Application
Run the Flask development server:
```bash
python app.py
```
The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### Authentication
- **Register User**: `POST /register`
  - Request Body:
    ```json
    {
        "username": "user1",
        "password": "password123",
        "role": "user"
    }
    ```
  - Response:
    ```json
    {
        "message": "User registered successfully!"
    }
    ```

- **Login User**: `POST /login`
  - Request Body:
    ```json
    {
        "username": "user1",
        "password": "password123"
    }
    ```
  - Response:
    ```json
    {
        "token": "<JWT_TOKEN>"
    }
    ```

### Admin Operations
- **Add Train**: `POST /admin/add_train`
  - Headers:
    - `x-api-key`: `<API_KEY>`
  - Request Body:
    ```json
    {
        "name": "Express Train",
        "source": "City A",
        "destination": "City B",
        "total_seats": 100
    }
    ```
  - Response:
    ```json
    {
        "message": "Train added successfully!"
    }
    ```

### User Operations
- **Check Train Availability**: `GET /check_availability`
  - Query Parameters:
    - `source`: Starting station
    - `destination`: Destination station
  - Response:
    ```json
    [
        {
            "id": 1,
            "name": "Express Train",
            "available_seats": 100
        }
    ]
    ```

- **Book a Seat**: `POST /book_seat`
  - Headers:
    - `x-access-token`: `<JWT_TOKEN>`
  - Request Body:
    ```json
    {
        "train_id": 1
    }
    ```
  - Response:
    ```json
    {
        "message": "Seat booked successfully!",
        "seat_number": 1
    }
    ```

- **Get Booking Details**: `GET /booking_details`
  - Headers:
    - `x-access-token`: `<JWT_TOKEN>`
  - Response:
    ```json
    [
        {
            "train_id": 1,
            "seat_number": 1,
            "timestamp": "2024-12-07T14:32:21.456789"
        }
    ]
    ```

## Security
- **JWT Authentication**: Secures user endpoints.
- **Admin API Key**: Protects sensitive admin operations.
- **Input Validation**: Ensures all inputs are sanitized to prevent SQL injection and other vulnerabilities.

## Notes
- Default database is SQLite for ease of setup. For production, switch to MySQL/PostgreSQL by updating `SQLALCHEMY_DATABASE_URI` in `app.config`.
- Ensure the `SECRET_KEY` and `x-api-key` are stored securely (e.g., in environment variables).

## License
This project is open-source and available under the MIT License.

