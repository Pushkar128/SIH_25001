from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="krishna*128",
    database="newdb"
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        ContactNumber VARCHAR(15) NOT NULL,
        EmailID VARCHAR(255) NOT NULL UNIQUE,
        Password VARCHAR(255) NOT NULL,
        MainRole VARCHAR(50) NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        ReportID INT AUTO_INCREMENT PRIMARY KEY,
        City VARCHAR(255) NOT NULL,
        Cases INT NOT NULL,
        WaterPollution INT NOT NULL,
        Alerts TEXT,
        SubmittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        SubmittedBy INT,
        FOREIGN KEY (SubmittedBy) REFERENCES users(UserID)
    )
""")
conn.commit()

# IST timezone
ist = pytz.timezone('Asia/Kolkata')

# Register endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    contact_number = data.get('contactNumber')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([username, contact_number, email, password, role]):
        return jsonify({"status": "error", "message": "All fields are required."})

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (Username, ContactNumber, EmailID, Password, MainRole) VALUES (%s, %s, %s, %s, %s)",
                       (username, contact_number, email, hashed_password, role))
        conn.commit()
        return jsonify({"status": "success", "message": "Registration successful."})
    except mysql.connector.IntegrityError:
        return jsonify({"status": "error", "message": "Email already exists."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
# Add this new route to your db1.py file

@app.route("/get-village-results", methods=["POST"])
def get_village_results():
    try:
        # For now, we will send back some hardcoded sample data
        # Later, you would query your MySQL database here
        sample_reports = [
            {"VillageName": "Greenfield", "Result": "Safe"},
            {"VillageName": "Red Valley", "Result": "Unsafe"},
            {"VillageName": "Blue Creek", "Result": "Safe"}
        ]
        return jsonify({"status": "success", "reports": sample_reports})

    except Exception as e:
        print(f"❌ Error fetching village results: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"status": "error", "message": "Email and password are required."})

    try:
        cursor.execute("SELECT UserID, Password, MainRole FROM users WHERE EmailID = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
            return jsonify({"status": "success", "message": "Login successful.", "user": {"id": user[0], "role": user[2]}})
        else:
            return jsonify({"status": "error", "message": "Invalid email or password."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Submit report endpoint
@app.route('/submit-report', methods=['POST', 'GET'])
def submit_report():
    if request.method == 'POST':
        data = request.form
        city = data.get('city')
        cases = data.get('cases')
        water_pollution = data.get('water_pollution')
        alerts = data.get('alerts', '')
        user_id = request.form.get('user_id')  # From session or form

        if not all([city, cases, water_pollution]):
            return jsonify({"status": "error", "message": "City, cases, and water pollution are required."})

        try:
            cursor.execute("INSERT INTO reports (City, Cases, WaterPollution, Alerts, SubmittedBy) VALUES (%s, %s, %s, %s, %s)",
                           (city, cases, water_pollution, alerts, user_id))
            conn.commit()
            return jsonify({"status": "success", "message": "Report submitted successfully."})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    elif request.method == 'GET':
        city = request.args.get('city')
        if not city:
            return jsonify({"status": "error", "message": "City parameter required."})

        try:
            cursor.execute("SELECT Cases, WaterPollution, Alerts FROM reports WHERE City = %s ORDER BY SubmittedAt DESC LIMIT 1", (city,))
            data = cursor.fetchone()

            if data:
                return jsonify({
                    "status": "success",
                    "data": {
                        "cases": data[0],
                        "water_pollution": data[1],
                        "alerts": data[2].split(';') if data[2] else [],
                        "coordinates": get_city_coordinates(city)  # Placeholder function
                    }
                })
            else:
                return jsonify({"status": "success", "data": None})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

# Placeholder function for city coordinates
def get_city_coordinates(city):
    city_coords = {
        "Hyderabad": [17.3850, 78.4867],
        "Assam": [26.2006, 92.9376],  # Approx. Guwahati
        "Meghalaya": [25.4670, 91.3662],  # Approx. Shillong
        "Manipur": [24.8170, 93.9368],  # Approx. Imphal
        "Tripura": [23.9408, 91.9882]   # Approx. Agartala
    }
    return [city_coords.get(city, [0, 0])]  # Default to [0, 0] if city not found

if __name__ == '__main__':
    app.run(debug=True, port=5000)