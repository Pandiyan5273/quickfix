import frappe

def test_override_called():
    count=frappe.call("frappe.client.get_count", "User")
    logs=frappe.get_all("Audit Log", filters={"action":"count_queried"}, order_by="timestamp desc", limit=1)
    assert logs, "No audit log created"

