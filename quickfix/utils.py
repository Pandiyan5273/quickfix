import frappe
import qrcode
import io
import base64
def send_urgent_alert(job_card, manager):
    subject = f"Urgent Job Card Requires Assignment: {job_card}"

    message = f"""
    An urgent Job Card has been created but no technician is assigned.

    Job Card: {job_card}

    Please assign a technician immediately.
    """

    frappe.sendmail(
        recipients=[manager],
        subject=subject,
        message=message
    )

def get_shop_name():
    return "QuickFix Repair Center"

def generate_qr(data):
    img=qrcode.make(data)
    buffer=io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()