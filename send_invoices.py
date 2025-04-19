# send_invoices.py

import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from pypdf import PdfReader, PdfWriter
import smtplib
from email.message import EmailMessage
from openpyxl import load_workbook
from datetime import datetime

# ==== CONFIGURATION ====
DRY_RUN = False  # Set to False when you're ready to send real emails

BASE_PATH = Path(__file__).resolve().parent
INVOICE_FOLDER = BASE_PATH / "InvoicesToProcess"
FINAL_FOLDER = BASE_PATH / "FinalInvoices"
LOG_FILE = BASE_PATH / "invoice_log.xlsx"
CONTACTS_FILE = BASE_PATH / "client_contacts.csv"
ENV_PATH = BASE_PATH / ".env"

# ==== LOAD ENVIRONMENT ====
load_dotenv(dotenv_path=ENV_PATH)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# ==== LOAD CONTACTS ====
contacts_df = pd.read_csv(CONTACTS_FILE)
contacts_dict = dict(zip(contacts_df["ClientName"], contacts_df["Email"]))

# ==== LOG CREATION ====
if not LOG_FILE.exists():
    pd.DataFrame(columns=["Timestamp", "ClientName", "Filename", "EmailStatus"]).to_excel(LOG_FILE, index=False)

# ==== PROCESS FILES ====
for invoice_file in INVOICE_FOLDER.glob("*_Invoice.pdf"):
    base_name = invoice_file.stem.replace("_Invoice", "")
    summary_file = INVOICE_FOLDER / f"{base_name}_Summary.pdf"

    if not summary_file.exists():
        print(f"❌ Missing summary for: {base_name}")
        continue

    # Merge PDFs using PdfWriter
    writer = PdfWriter()

    for file_path in [invoice_file, summary_file]:
        reader = PdfReader(str(file_path))
        for page in reader.pages:
            writer.add_page(page)

    merged_filename = f"{base_name}_InvoicePacket.pdf"
    merged_path = FINAL_FOLDER / merged_filename
    with open(merged_path, "wb") as f_out:
        writer.write(f_out)


    # Prepare Email
    client_name = base_name.split("_")[0]
    month_label = base_name.split("_")[1] if "_" in base_name else "this period"
    client_email = contacts_dict.get(client_name)
    email_status = "No email found"

    if client_email:
        if DRY_RUN:
            print(f"[DRY RUN] Would send email to {client_email} with file: {merged_filename}")
            email_status = "Dry run – not sent"
        else:
            try:
                msg = EmailMessage()
                msg["Subject"] = f"Your Invoice – {month_label}"
                msg["From"] = EMAIL_USER
                msg["To"] = client_email
                msg.set_content(f"Hi {client_name},\n\nPlease find your invoice packet for {month_label} attached.\n\nThanks!\nJess Hayden Consulting")

                with open(merged_path, "rb") as f:
                    msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=merged_filename)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL_USER, EMAIL_PASS)
                    smtp.send_message(msg)

                print(f"✅ Email sent to {client_email}")
                email_status = "Sent"
            except Exception as e:
                print(f"❌ Error sending email to {client_email}: {e}")
                email_status = f"Failed: {e}"

    # Log result
    wb = load_workbook(LOG_FILE)
    ws = wb.active
    ws.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), client_name, merged_filename, email_status])
    wb.save(LOG_FILE)
