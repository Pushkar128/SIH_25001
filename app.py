import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client
import mysql.connector
from mysql.connector import Error
import datetime

# --- Load Environment Variables ---
load_dotenv()
# Twilio Credentials
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
OFFICIAL_PHONE_NUMBER = os.environ.get("OFFICIAL_PHONE_NUMBER")
# Database Credentials
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME", "new_db")


# --- Initialize Services ---

# Initialize the Twilio client if credentials are available
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✅ Twilio client initialized.")
else:
    client = None
    print("⚠️ Twilio credentials not found. SMS alerts will be disabled.")

# Database connection function
def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL database: {e}")
        return None

# --- Flask App Initialization ---
app = Flask(__name__, template_folder="templates")
CORS(app)


# --- Load Machine Learning Model Files ---
try:
    model = joblib.load("water_quality_model.pkl")
    model_features = joblib.load("model_features.pkl")
    scaler = joblib.load("scaler.pkl")
    imputer = joblib.load("imputer.pkl")
    print("✅ Model & preprocessing files loaded successfully.")
except FileNotFoundError:
    print("❌ Critical Error: Model files not found. Please ensure .pkl files are in the root directory.")
    exit()


# --- HTML Page Serving Routes ---
@app.route("/")
def index():
    """Serves the main homepage or a default page."""
    return render_template("Homepage1.html") 

@app.route("/asha")
def asha_page():
    """Serves the ASHA worker's reporting page."""
    return render_template("asha.html")

@app.route("/doctor")
def doctor_page():
    """Serves the doctor's reporting page."""
    return render_template("doctor.html")

@app.route("/citizen")
def citizen_page():
    """Serves the citizen's portal page."""
    return render_template("citizen.html")


# --- API Endpoint for Report Submission ---
@app.route("/submit-report", methods=["POST"])
def submit_report():
    data = request.json
    response = {}
    quality_category = None

    # 1. Predict Water Quality using the ML Model
    try:
        # Create a full data record with all features expected by the model
        full_data_record = {feature: None for feature in model_features}
        for key, value in data.items():
            # Map frontend field names to model feature names
            mapped_key = {
                'phLevel': 'ph',
                'bacterialLevel': 'coliform_bacteria',
                'turbidityNtu': 'turbidity'
            }.get(key, key)
            
            if mapped_key in model_features and value:
                full_data_record[mapped_key] = float(value)

        df = pd.DataFrame([full_data_record])
        df = df[model_features] # Ensure correct column order

        df_imputed = imputer.transform(df)
        df_scaled = scaler.transform(df_imputed)
        prediction_code = model.predict(df_scaled)[0]
        
        quality_category = "Safe" if prediction_code == 1 else "Unsafe"
        response["quality_category"] = quality_category

        # 2. Send SMS Alert if water is unsafe
        if quality_category == "Unsafe" and client and OFFICIAL_PHONE_NUMBER:
            try:
                message_body = (f"URGENT: Unsafe water quality reported in {data.get('villageName', 'N/A')}. "
                              f"Details - pH: {data.get('phLevel')}, Bacteria: {data.get('bacterialLevel')}, Turbidity: {data.get('turbidityNtu')}. "
                              f"Please investigate.")
                client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE_NUMBER,
                    to=OFFICIAL_PHONE_NUMBER
                )
                response["sms_status"] = "Alert Sent Successfully"
            except Exception as e:
                response["sms_status"] = f"Failed to send alert: {e}"

    except Exception as e:
        response["water_error"] = f"Error during prediction: {str(e)}"

    # 3. Store the complete report in the database
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO water_reports (
                    VillageName, WaterSourceID, ReportDate, BacterialLevel, 
                    pHLevel, TurbidityNTU, SymptomsObserved, Remarks, Result
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data.get('villageName'), data.get('waterSourceId'),
                data.get('reportDate'), data.get('bacterialLevel'),
                data.get('phLevel'), data.get('turbidityNtu'),
                data.get('symptomsObserved'), data.get('remarks'),
                quality_category
            )
            cursor.execute(query, values)
            connection.commit()
            response["db_status"] = "Report stored successfully"
        except Error as e:
            response["db_status"] = f"Failed to store report: {e}"
        finally:
            cursor.close()
            connection.close()
    else:
        response["db_status"] = "Database connection failed"

    return jsonify(response)


# --- API Endpoint for Fetching Village Results ---
@app.route("/get-village-results", methods=["POST"])
def get_village_results():
    data = request.json
    city = data.get('city')
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT VillageName, Result FROM water_reports WHERE LOWER(VillageName) LIKE %s ORDER BY ReportDate DESC"
        cursor.execute(query, (f"%{city.lower()}%",))
        reports = cursor.fetchall()
        return jsonify({"status": "success", "reports": reports})
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)