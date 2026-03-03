import frappe

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