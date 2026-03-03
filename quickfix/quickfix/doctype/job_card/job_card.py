# Copyright (c) 2026, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def before_insert(self):
		setting= frappe.get_single_value("Quickfix Settings", "default_labour_charge")
		if not self.labour_charge:
			self.labour_charge=setting

	def permission_query_conditions(self, user):
		if not user: user = frappe.session.user
		if "QF Technician" in frappe.get_roles(user):
			return """(`tabJob Card`.assigned_technician = '{user}')""".format(user=user)