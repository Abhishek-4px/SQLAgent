import sqlite3
import random
from datetime import datetime, timedelta

FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
               "Ananya", "Diya", "Saanvi", "Isha", "Aanya", "Priya", "Meera", "Riya", "Kavya", "Nisha"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Reddy", "Nair", "Joshi", "Rao"]
SPECIALTIES = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]
DEPARTMENTS = ["Skin Dept", "Heart Dept", "Bone Dept", "Primary Care", "Child Dept"]
CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
GENDERS = ["M", "F"]

def _maybe_none(value):
    return None if random.random() < 0.10 else value

def _random_date(days_back=365):
    return (datetime.now() - timedelta(days=random.randint(0, days_back))).strftime("%Y-%m-%d")

def _random_datetime(days_back=365):
    dt = datetime.now() - timedelta(days=random.randint(0, days_back), hours=random.randint(8, 18))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def _generate_dummy_data(cursor):
    # Patients (200)
    for _ in range(200):
        cursor.execute(
            "INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (random.choice(FIRST_NAMES), random.choice(LAST_NAMES), _maybe_none(f"{random.choice(FIRST_NAMES).lower()}@mail.com"),
             _maybe_none(f"+91{random.randint(7000000000, 9999999999)}"), _random_date(days_back=365*60), random.choice(GENDERS),
             random.choice(CITIES), _random_date(days_back=365))
        )

    # Doctors (15)
    for i in range(15):
        cursor.execute(
            "INSERT INTO doctors (name, specialization, department, phone) VALUES (?, ?, ?, ?)",
            (f"Dr. {random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}", SPECIALTIES[i % 5], DEPARTMENTS[i % 5],
             _maybe_none(f"+91{random.randint(7000000000, 9999999999)}"))
        )

    # Appointments (500)
    patient_ids = list(range(1, 201))
    doctor_ids = list(range(1, 16))
    for _ in range(500):
        cursor.execute(
            "INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes) VALUES (?, ?, ?, ?, ?)",
            (random.choice(patient_ids), random.choice(doctor_ids), _random_datetime(),
             random.choice(["Scheduled", "Completed", "Cancelled", "No-Show"]), _maybe_none("Routine checkup"))
        )

    # Treatments (350)
    completed_appt_ids = [row[0] for row in cursor.execute("SELECT id FROM appointments WHERE status='Completed'").fetchall()]
    if not completed_appt_ids: completed_appt_ids = [1] # Fallback
    for _ in range(350):
        cursor.execute(
            "INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes) VALUES (?, ?, ?, ?)",
            (random.choice(completed_appt_ids), random.choice(["Blood Test", "X-Ray", "MRI", "ECG", "Consultation"]),
             round(random.uniform(50.0, 5000.0), 2), random.randint(15, 120))
        )

    # Invoices (300)
    for _ in range(300):
        total = round(random.uniform(100.0, 10000.0), 2)
        paid_fraction = random.choice([0.0, 0.5, 1.0])
        paid = round(total * paid_fraction, 2)
        status = "Paid" if paid_fraction == 1.0 else (random.choice(["Pending", "Overdue"]) if paid_fraction == 0 else "Pending")
        cursor.execute(
            "INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status) VALUES (?, ?, ?, ?, ?)",
            (random.choice(patient_ids), _random_date(), total, paid, status)
        )

def setup_database():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT, phone TEXT, date_of_birth DATE, gender TEXT, city TEXT, registered_date DATE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, specialization TEXT, department TEXT, phone TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, appointment_date DATETIME, status TEXT, notes TEXT, FOREIGN KEY(patient_id) REFERENCES patients(id), FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS treatments (id INTEGER PRIMARY KEY AUTOINCREMENT, appointment_id INTEGER, treatment_name TEXT, cost REAL, duration_minutes INTEGER, FOREIGN KEY(appointment_id) REFERENCES appointments(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, invoice_date DATE, total_amount REAL, paid_amount REAL, status TEXT, FOREIGN KEY(patient_id) REFERENCES patients(id))''')

    _generate_dummy_data(cursor)
    conn.commit()
    conn.close()
    print("Created 200 patients, 15 doctors, 500 appointments, 350 treatments, 300 invoices.")

if __name__ == "__main__":
    setup_database()