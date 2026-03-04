import frappe

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