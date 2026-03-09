# Copyright (c) 2026, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		setting= frappe.get_single_value("Quickfix Settings", "default_labour_charge")
		if not self.labour_charge:
			self.labour_charge=setting

		if self.customer_phone:
			if not(self.customer_phone.isdigit() and len(self.customer_phone)==10):
				frappe.throw("Customer phone number must be 10 digits.")
		if self.status in ["In Repair","Ready for Delivery","Delivered"] :
			if not self.assigned_technician:
				frappe.throw("Assigned technician is required once repait starts.")
		
		parts_tot=0
		for row in self.parts_used:
			row.total_price=row.quantity*row.unit_price
			parts_tot+=row.total_price
		self.parts_total=parts_tot

		self.final_amount=self.parts_total+self.labour_charge
		if self.priority=='Normal':
			frappe.throw("Priority cannot be Low for a Job Card.")
	def permission_query_conditions(self, user):
		if not user: user = frappe.session.user
		if "QF Technician" in frappe.get_roles(user):
			return """(`tabJob Card`.assigned_technician = '{user}')""".format(user=user)
		

	def before_submit(self):
		if self.status!="Ready for Delivery":
			frappe.throw("Job Card can only be submitted when status is 'Ready for Delivery'.")

		for row in self.parts_used:
			stock_qty=frappe.get_value("Spare Part", row.part, "stock_qty")
			if stock_qty is None:
				frappe.throw(f"Spare Part {row.part} does not exist.")
			if stock_qty < row.quantity:
				frappe.throw(f"Insufficient stock for Spare Part {row.part}.")

	def on_submit(self):
		for row in self.parts_used:
			current_stock=frappe.get_value("Spare Part", row.part, "stock_qty")
			new_stock=current_stock - row.quantity
			frappe.db.set_value("Spare Part", row.part, "stock_qty", new_stock, update_modified=False)

		invoice=frappe.get_doc({
				"doctype": "Service Invoice",
				"job_card": self.name,
				"invoice_date": self.creation,
				"labour_charge": self.labour_charge,
			})
		invoice.insert(ignore_permissions=True)

		frappe.publish_realtime("job_ready", {"job_card": self.name}, user=self.owner)
		frappe.sendmail(
				recipients=[self.customer_email],
				subject=f"Your Device is Ready ",
				message=f"Dear {self.customer_name},<br><br>Your device with Job Card {self.name} is ready for delivery with amount {self.final_amount}. Please contact us to arrange pickup.<br><br>Thank you for choosing our service!<br><br>Best regards,<br>QuickFix Team"
			)

	def on_cancel(self):
		self.status="Cancelled"

		for row in self.parts_used:
			current_stock=frappe.get_value("Spare Part", row.part, "stock_qty")
			frappe.db.set_value("Spare Part", row.part, "stock_qty", current_stock + row.quantity, update_modified=False)
			inv_name=frappe.get_value("Service Invoice", {"job_card": self.name}, "name")
			if inv_name:
				invoice=frappe.get_doc("Service Invoice", inv_name)
				if invoice.docstatus==1:
					invoice.cancel()
	
	def on_trash(self):
		if self.status not in ["Cancelled", "Draft"]:
			frappe.throw("Only Job Cards in Draft or Cancelled status can be deleted.")

	# def on_update(self):
	# 	self.save()