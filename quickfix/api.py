import frappe
from quickfix.quickfix.report.technician_performance import technician_performance
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def share_job_card(job_card_name,user_email):
    frappe.share.add("Job Card", job_card_name, user_email, read=1, write=0, share=0, everyone=0)
    return f"Job Card {job_card_name} shared with {user_email}"


@frappe.whitelist()
def manager_func():
    frappe.only_for("QF Manager")
    return "This function can only be accessed by users with the Manager role."

@frappe.whitelist(allow_guest=True)
def get_job_carsds_unsafe():
    return frappe.get_all("Job Card", fields='*')

@frappe.whitelist()
def get_job_cards_safe():
    user=frappe.session.user
    roles=frappe.get_roles(user)

    jc=frappe.get_list("Job Card", fields='*')

    if "QF Manager" not in roles:
        for j in jc:
            j.pop('customer_phone', None)
            j.pop('customer_email', None)

    return jc

@frappe.whitelist()
def rename_technician( old_name, new_name):
    frappe.rename_doc("Spare Part", old_name, new_name, merge=True)
    return f"technician renamed from {old_name} to {new_name}"

@frappe.whitelist()
def custom_get_count(doctype, filters=None, debug=False, cache=False):
 frappe.get_doc({"doctype":"Audit Log","doctype_name":doctype,"action":"count_queried","user":frappe.session.user}).insert(ignore_permissions=True)
 from frappe.client import get_count
 return get_count(doctype, filters, debug, cache)

@frappe.whitelist()
def mark_as_delivered(job_card,customer_email):
    frappe.db.set_value("Job Card",job_card,"status","Delivered")
    frappe.enqueue("quickfix.api.send_delivered_email", queue="short", job_card=job_card, customer_email=customer_email)
    return "marked as delivered"

def send_delivered_email(job_card,customer_email):
    frappe.sendmail(
        recipients=[customer_email],
        subject="Your device is delivered",
        message=f"Dear Customer, Your device for Job Card {job_card} has been delivered. Thank you for choosing Quickfix!"
    )
@frappe.whitelist()
def reject_job(job_card,reason):
    frappe.db.set_value("Job Card",job_card,"status","Draft")
    doc=frappe.get_doc("Job Card",job_card)
    doc.cancel()

@frappe.whitelist()
def transfer_technician(job_card,technician):
    doc=frappe.get_doc("Job Card",job_card)
    doc.db_set("assigned_technician",technician)
    return "status:success"

@frappe.whitelist()
def enqueue_monthly_revenue_report():
    from frappe.utils import get_first_day, get_last_day, nowdate
    frappe.enqueue(
        "quickfix.api.generate_monthly_revenue_report",
        queue="long",
        timeout=600,
        start_date=get_first_day(nowdate()),
        end_date=get_last_day(nowdate())
    )
    return "Monthly revenue report generation enqueued on 'long' queue with 600s timeout."


@frappe.whitelist()
def generate_monthly_revenue_report(start_date=None, end_date=None):
    manager_email = frappe.db.get_value("Quickfix Settings", None, "manager_email")
    if not manager_email:
        return "Manager email not set in Quickfix Setting."

    filters = {}
    if start_date:
        filters["from_date"] = start_date
    if end_date:
        filters["to_date"] = end_date
    columns, data, _, chart, summary = technician_performance.execute(filters)


    html = f"<h2>Technician Performance Report ({start_date} to {end_date})</h2>"
    html += "<table border='1'><tr>"
    for col in columns:
        html += f"<th>{col['label']}</th>"
    html += "</tr>"
    for row in data:
        html += "<tr>"
        for col in columns:
            html += f"<td>{row.get(col['fieldname'], '')}</td>"
        html += "</tr>"
    html += "</table>"

    html += "<h3>Summary</h3><ul>"
    for item in summary:
        html += f"<li>{item['label']}: {item['value']}</li>"
    html += "</ul>"

    pdf = get_pdf(html)
    frappe.sendmail(
        recipients=[manager_email],
        subject=f"Technician Performance Report ({start_date} to {end_date})",
        message="Attached is the performance report for all technicians.",
        attachments=[{"fname": "Technician_Performance_Report.pdf", "fcontent": pdf}]
    )
    return f"Report sent to {manager_email}"

from frappe.utils import today
@frappe.whitelist()
def check_low_stock():
    last_run=frappe.db.get_value('Audit Log',{"action":"low_stock_check","timestamp":["like",today()+ "%"]},"name")
    if last_run:
        frappe.log_error("this function is already called")
        return
    low_stock_item=frappe.get_all("Spare part",{"stock_quantity":["<",5]},fields=["name","stock_quantity"])
    for item in low_stock_item:
        frappe.log_error(f"Low stock alert: {item['name']} has only {item['stock_quantity']} left in stock.")
    frappe.get_doc({"doctype":"Audit Log","action":"low_stock_check","timestamp":today()}).insert(ignore_permissions=True)
    frappe.db.commit()
