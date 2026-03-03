# Copyright (c) 2026, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	def has_permission(self,user=None):
		if not user: user = frappe.session.user
		if "QF Manager" in frappe.get_roles(user):
			return True
		
		job_card=frappe.get_doc("Job Card", self.job_card)
		if job_card.payment_status!="Paid":
			return False
		return True