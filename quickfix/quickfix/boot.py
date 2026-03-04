import frappe

def extend_bootinfo(bootinfo):
    settings=frappe.get_single("Quickfix Settings")
    bootinfo.shop_name=settings.shop_name
    bootinfo.manager_email=settings.manager_email