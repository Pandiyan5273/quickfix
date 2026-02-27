# Copyright (c) 2026, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):
	def autoname(self):
		self.name=self.part_code.upper()+"-"+make_autoname("PART-.YYYY.-.####")

	def validate(self):
		if self.selling_price < self.unit_cost:
			frappe.throw("Selling Price must be greater than Unit Cost")
