import frappe

def validate_job_card(doc, method):

    if not doc.device_type:
        frappe.throw("Device Type must be selected.")