# NL2SQL Test Results
**LLM Provider**: Groq (llama-3.1-8b-instant)
**Total Passed**: 17 / 20
**Total Failed**: 3 / 20

## Summary of Failures
- **Q6 & Q19**: Failed due to incorrect JOIN conditions. The LLM hallucinated relationship keys instead of strictly following the provided schema paths.
- **Q9**: Failed due to missing SELECT columns. The query calculated the average correctly but forgot to output the grouping category name in the SELECT statement.

## Detailed Test Results

| # | Question | Generated SQL | Status | Notes |
|---|----------|---------------|--------|-------|
| 1 | How many patients do we have? | `SELECT COUNT(*) AS total_patients FROM patients;` | ✅ Pass | Returned exactly 200. |
| 2 | List all doctors and their specializations | `SELECT name, specialization FROM doctors;` | ✅ Pass | Returned 15 rows cleanly. |
| 3 | Show me appointments for last month | `SELECT * FROM appointments WHERE appointment_date >= date('now', '-1 month')` | ✅ Pass | Correctly used SQLite date filtering. |
| 4 | Which doctor has the most appointments? | `SELECT d.name, COUNT(a.id) ... GROUP BY d.name ORDER BY COUNT(a.id) DESC LIMIT 1` | ✅ Pass | Correct JOIN and GROUP BY logic. |
| 5 | What is the total revenue? | `SELECT SUM(total_amount) FROM invoices` | ✅ Pass | Simple and correct aggregation. |
| 6 | Show revenue by doctor | `... JOIN invoices i ON a.id = i.patient_id ...` | ❌ Fail | Wrong JOIN condition: Joined a.id to i.patient_id. It should be a.patient_id = i.patient_id. |
| 7 | How many cancelled appointments last quarter? | `... WHERE status = 'Cancelled' AND appointment_date >= DATE('now', '-3 months')` | ✅ Pass | Correct string matching and date logic. |
| 8 | Top 5 patients by spending | `... JOIN invoices i ON p.id = i.patient_id GROUP BY p.id ORDER BY total_spending DESC LIMIT 5` | ✅ Pass | Perfect query. Generated chart successfully. |
| 9 | Average treatment cost by specialization | `SELECT AVG(t.cost) ... GROUP BY d.specialization` | ❌ Fail | Missing SELECT column: Forgot to SELECT d.specialization. Output shows averages but lacks category names. |
| 10 | Show monthly appointment count for past 6 months | `SELECT strftime('%Y-%m', appointment_date) AS month, COUNT(*) ...` | ✅ Pass | Perfect use of strftime for time-series grouping. |
| 11 | Which city has the most patients? | `SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1` | ✅ Pass | Correct aggregation and sorting. |
| 12 | List patients who visited more than 3 times | `... GROUP BY p.id HAVING COUNT(a.id) > 3` | ✅ Pass | Correct use of the HAVING clause. |
| 13 | Show unpaid invoices | `SELECT * FROM invoices WHERE status IN ('Pending', 'Overdue')` | ✅ Pass | Correctly mapped "unpaid" business logic to DB schema statuses. |
| 14 | What percentage of appointments are no-shows? | `SELECT ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM appointments)), 2) ...` | ✅ Pass | Flawless subquery math for percentages. |
| 15 | Show the busiest day of the week | `SELECT strftime('%w', appointment_date) AS day_of_week ... LIMIT 1` | ✅ Pass | Correct SQLite date formatting (returned '5' for Friday). |
| 16 | Revenue trend by month | `SELECT strftime('%Y-%m', invoice_date) AS month, SUM(total_amount) ... GROUP BY month` | ✅ Pass | Perfect time-series grouping. Generated chart. |
| 17 | Average appointment duration by doctor | `SELECT d.name, AVG(t.duration_minutes) ... GROUP BY d.name` | ✅ Pass | Correct multi-table JOIN and AVG aggregation. |
| 18 | List patients with overdue invoices | `... JOIN invoices i ON p.id = i.patient_id WHERE i.status = 'Overdue'` | ✅ Pass | Correct filtering and JOIN. |
| 19 | Compare revenue between departments | `... JOIN appointments a ON i.patient_id = a.patient_id ... GROUP BY d.department` | ❌ Fail | Logical Fan-out Error: Joining on just patient_id creates a Cartesian product, artificially inflating revenue numbers. |
| 20 | Show patient registration trend by month | `SELECT strftime('%Y-%m', registered_date) AS month, COUNT(*) ... GROUP BY month` | ✅ Pass | Perfect time-series query. |
