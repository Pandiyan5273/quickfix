import frappe
from quickfix.monkey_patch import apply_all
import frappe.utils as fu

class TestGetUrl:
    def test_prefix_applied(self):
        frappe.conf.custom_url_prefix = "https://cdn.example.com"
        apply_all()
        url = fu.get_url("/files/test.png")
        print("url",url)
        assert url.startswith("https://cdn.example.com")

    def test_original_behavior_without_prefix(self):
        frappe.conf.custom_url_prefix = ""
        apply_all()
        url = fu.get_url("/files/test.png")
        assert "cdn.example.com" not in url