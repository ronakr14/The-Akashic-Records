---
type: project
---

Multi Speciality Hospital

Entities:
1. Clinical:
	1. Patient
	2. Doctor
	3. Nurse
	4. Caregiver
	5. Lab Tecnician
	6. Pharmacist
2. Administrative
	1. Receptionist
	2. Admin
	3. Insurance
3. Supply Chain
	1. Inventory Manager
	2. Procurement Manager

Encounters:
1. Registration
	1. Patient Creation
	2. Caregiver Mapping
	3. Insurance Mapping
2. Appointment
	1. Scheduling
	2. Cancellation
	3. Rescheduling
	4. Queue Management
3. Consultation
	1. Doctor Notes
	2. Diagnosis
	3. Treatment Plan
4. Laboratory
	1. Test Orders
	2. Samples
	3. Result
5. Pharmacy
	1. Prescription
	2. Dispensing
	3. Refills
6. Emergenct
	1. Emergency Admission
	2. Triage
	3. Critical Alerts
7. ICU
	1. ICU Admissions
	2. Vitals Monitoring
	3. Bed Assignment
8. Inventory
	1. Medicine Stock
	2. Medical Equipment
	3. Consumables
9. Billing
	1. Charges
	2. Copay
	3. Invoices
	4. Payments
10. Insurance
	1. Claims
	2. Approvals
	3. Denials

Domains:
1. People
	1. Patient
	2. Doctor
	3. Nurse
	4. Caregiver
	5. Lab Technician
	6. Pharmacist
	7. Receptionist
	8. Administrator
	9. Insurance Representative
	10. Employer
	11. Emergency Contact
2. Clinical
	1. Encounter
	2. Consultation
	3. Diagnosis
	4. Condition
	5. Allergy
	6. Clinical note
	7. Treatment Plan
	8. Referral
	9. Procedure
	10. Prescription
	11. Lab Test
	12. Lab Result
	13. Admission
	14. Discharge
	15. Appointment
	16. Appointment Slot
	17. Queue Token
	18. Check-In
	19. Check-Out
3. Resource
	1. Hospital Building
	2. Department
	3. Ward
	4. Room
	5. Bed
	6. ICU Bed
	7. Ventilator
	8. Monitor
	9. Wheelchair
	10. Infusion Pump
	11. Ambulance
	12. Floor
	13. Unit
	14. Admission
	15. Transfer
	16. Discharge
	17. Bed Assignment
	18. Care Episode
	19. Patient Monitor
	20. Infusion Pump
	21. Operation Theatre
4. Inventory
	1. Medication
	2. Medical Equipment
	3. Consumables
	4. PPE
	5. Syringes
	6. Blood Units
5. Financial
	1. Invoice
	2. Payment
	3. Insurance Claim
	4. Copay
	5. Coverage
6. Workforce Management
	1. Shift
	2. Shift Assignment
	3. Duty Roster
	4. Leave Request
	5. Attendance Record
7. Emergency Department
	1. Emergency Visit
	2. Triage Assessment
	3. Emergency Severity
	4. Emergency Case
8. ICU
	1. ICU Admission
	2. ICU Stay
	3. ICU Observation
	4. Ventilator Assignment
	5. Critical Event
9. Lab Domain
	1. Lab Order
	2. Lab Test
	3. Sample
	4. Sample Collection
	5. Sample Processing
	6. Lab Result
	7. Lab Report
10. Pharmacy & Medication
	1. Medication
	2. Drug
	3. Prescription
	4. Prescription Item
	5. Dispense Record
	6. Medication Administration
	7. Medication Schedule
11. Vitals & Monitoring
	1. Vital Sign
	2. Observation
	3. Measurement - Heart Rate, Blood Pressure, SPO2, Temperature, Respiration Rate
	4. Alert
12. Inventory & Supply Chain
	1. Inventory Item
	2. Inventory Category
	3. Inventory Location
	4. Stock Transaction
	5. Stock Adjustment
	6. Stock Transfer
	7. Purchase Order
	8. Purchase Order Item
	9. Supplier
	10. Goods Receipt
	11. Batch
	12. Lot
	13. Expiry Record
13. Billing & Financials
	1. Invoice
	2. Invoice Line Item
	3. Charge
	4. Payment
	5. Payment Method
	6. Refund
	7. Copay
	8. Price Catalog
14. Insurance
	1. Insurance Policy
	2. Coverage Plan
	3. Claim
	4. Claim Line Item
	5. Preauthorization
	6. Claim Review
	7. Settlement
15. Audit & Workflow
	1. status
	2. substatus
	3. workflow state
	4. audit log
	5. status history
	6. task
16. Communication
	1. Notification
	2. Email
	3. SMS
	4. Reminder
17. Documents:
	1. Document
	2. Attachment
	3. Lab Report
	4. Prescription
	5. Discharge 
	6. Insurance
	7. Clinical Guideline
	8. Hospital SOP
	9. Drug Reference

| Role         | View Patient | Edit Patient | View Billing | View Lab        |
| ------------ | ------------ | ------------ | ------------ | --------------- |
| Receptionist | Yes          | Limited      | No           | No              |
| Doctor       | Yes          | Yes          | No           | Yes             |
| Nurse        | Yes          | Partial      | No           | Yes             |
| Pharmacist   | Limited      | No           | No           | Medication Only |
| Admin        | Yes          | Yes          | Yes          | Yes             |