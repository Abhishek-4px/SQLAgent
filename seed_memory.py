FEW_SHOT_EXAMPLES = """
1. Q: "How many patients do we have?" -> SQL: SELECT COUNT(*) AS total_patients FROM patients;
2. Q: "List all doctors and their specializations" -> SQL: SELECT name, specialization FROM doctors;
3. Q: "Which doctor has the most appointments?" -> SQL: SELECT d.name, COUNT(a.id) FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.name ORDER BY COUNT(a.id) DESC LIMIT 1;
4. Q: "What is the total revenue?" -> SQL: SELECT SUM(total_amount) FROM invoices;
5. Q: "Which city has the most patients?" -> SQL: SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1;
6. Q: "Show unpaid invoices" -> SQL: SELECT * FROM invoices WHERE status IN ('Pending', 'Overdue');
7. Q: "List patients who visited more than 3 times" -> SQL: SELECT p.first_name, p.last_name, COUNT(a.id) FROM patients p JOIN appointments a ON p.id = a.patient_id GROUP BY p.id HAVING COUNT(a.id) > 3;
8. Q: "Revenue trend by month" -> SQL: SELECT strftime('%Y-%m', invoice_date) AS month, SUM(total_amount) FROM invoices GROUP BY month ORDER BY month;
9. Q: "What percentage of appointments are no-shows?" -> SQL: SELECT ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM appointments)), 2) FROM appointments WHERE status = 'No-Show';
10. Q: "Show patient registration trend by month" -> SQL: SELECT strftime('%Y-%m', registered_date) AS month, COUNT(*) FROM patients GROUP BY month ORDER BY month;
"""

def get_few_shot_examples():
    return FEW_SHOT_EXAMPLES

if __name__ == "__main__":
    print(f"Loaded {len(FEW_SHOT_EXAMPLES.split('Q:')) - 1} few-shot training pairs into memory.")