# 📬 Invoice Processing Automation

This project automates the process of merging freelance invoices and work summaries into a single PDF per client, saving the result in a final folder, logging each action, and emailing the file to the client.

Perfect for freelancers, consultants, and small businesses who want to spend less time on admin and more time getting paid.

---

## 📁 Folder Structure

    InvoiceAutomation/
    ├── InvoicesToProcess/       # Place invoice and summary PDFs here
    ├── FinalInvoices/           # Output folder for merged PDF packets
    ├── invoice_log.xlsx         # Log file of email activity 
    ├── client_contacts.csv      # Client name and email address mapping
    ├── .env                     # Stores your email credentials securely
    ├── send_invoices.py         # Main script
    ├── README.md                # This file

---

## 🔧 Setup Instructions

### 1. Install dependencies

Run this in your terminal:

```bash
pip install pypdf pandas openpyxl python-dotenv
```

---

### 2. Create `.env` file

This file stores your Gmail credentials securely. Create a file called `.env` and add:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

> **Note:** Use a Gmail App Password (not your regular password) if you have 2-step verification enabled.

---

### 3. Fill out `client_contacts.csv`

Example format:

```
ClientName,Email
PineconeLLC,your_email1@gmail.com
SideHustleCo,your_email2@gmail.com
PivotAnalytics,your_email3@gmail.com
```

---

### 4. Add PDFs to `InvoicesToProcess/`

Name your files using this format:

```
ClientName_MonthYear_Invoice.pdf
ClientName_MonthYear_Summary.pdf
```

Example:

```
PineconeLLC_April2025_Invoice.pdf
PineconeLLC_April2025_Summary.pdf
```

---

### 5. Run the script

```bash
python send_invoices.py
```

- If `DRY_RUN = True`, the script will simulate sending and log the action.
- Set `DRY_RUN = False` when you're ready to send real emails.

---

### ✅ Output

- Merged PDF saved to `/FinalInvoices/`
- Email sent to the client (if not in dry run mode)
- Action logged in `invoice_log.xlsx`

