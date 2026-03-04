import frappe

def log_login(login_manager):
    audit=frappe.get_doc({
        "doctype":"Audit Log",
        "user":frappe.session.user,
        "action":"Login",
        "timestamp":frappe.utils.now()
    })
    audit.insert(ignore_permissions=True)

def log_logout(login_manager):
    audit=frappe.get_doc({
        "doctype":"Audit Log",
        "user":frappe.session.user,
        "action":"Logout",
        "timestamp":frappe.utils.now()
    })
    audit.insert(ignore_permissions=True)

def extend_bootinfo(bootinfo):
    settings = frappe.get_single("Quickfix Settings")
    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email

def get_shop_name():
    settings = frappe.get_single("Quickfix Settings")
    return settings.shop_name

def format_job(value):
    return f"Job-{value}"