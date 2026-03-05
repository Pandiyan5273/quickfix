import frappe

def after_install():
    device_type=["Laptop","Desktop","Mobile"]
    for d in device_type:
        if not frappe.db.exists("Device Type",d):
            doc=frappe.get_doc({
                "doctype":"Device Type",
                "device_type":d
            })
            doc.insert(ignore_permissions=True)
    
    if not frappe.db.exists("Quickfix Settings","Quickfix Settings"):
        doc=frappe.get_doc({
            "doctype":"Quickfix Settings",
            "shop_name":"Quickfix",
            "manager_email":"manager@quickfix.com",
            "low_stock_threshold":10
        })
        doc.insert(ignore_permissions=True)
    frappe.msgprint("Quickfix App Installed Successfully")
    frappe.make_property_setter("Job Card","remarks","bold",1,"Check")

def before_uninstall():
    submitted_cards=frappe.db.exists("Job Card",{"docstatus":1})
    if submitted_cards:
        frappe.throw("Cannot uninstall Quickfix App because there are submitted Job Cards. Please cancel or delete all Job Cards before uninstalling.")