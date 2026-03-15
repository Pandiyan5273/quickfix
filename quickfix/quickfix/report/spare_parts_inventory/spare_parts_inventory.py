# Copyright (c) 2026, admin and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters: dict | None = None):
	columns = get_columns()
	data = get_data()
	summary=get_summary(data)

	return columns, data,None,None, summary


def get_columns() -> list[dict]:
    return [
        {"label": "Part Name", "fieldname": "part_name", "fieldtype": "Data", "width": 200},
        {"label": "Part Code", "fieldname": "part_code", "fieldtype": "Data", "width": 150},
        {"label": "Device Type", "fieldname": "device_type", "fieldtype": "Link", "options": "Device Type", "width": 150},
        {"label": "Stock Qty", "fieldname": "stock_qty", "fieldtype": "Float", "width": 120},
        {"label": "Reorder Level", "fieldname": "reorder_level", "fieldtype": "Float", "width": 120},
        {"label": "Unit Cost", "fieldname": "unit_cost", "fieldtype": "Currency", "width": 120},
        {"label": "Selling Price", "fieldname": "selling_price", "fieldtype": "Currency", "width": 120},
        {"label": "Margin %", "fieldname": "margin", "fieldtype": "Percent", "width": 120},
        {"label": "Total Value", "fieldname": "total_value", "fieldtype": "Currency", "width": 150},
    ]


def get_data() -> list[list]:
	parts = frappe.get_list("Spare Part", fields=["part_name", "part_code", "compatible_device_type", "stock_qty", "reorder_level", "unit_cost", "selling_price"])
	data = []
	total_value = 0
	total_stock = 0

	for p in parts:
		unit_cost = round(p.get("unit_cost", 0), 2)
		selling_price = round(p.get("selling_price", 0), 2)
		stock_qty = p.get("stock_qty", 0)
		reorder_level = p.get("reorder_level", 0)
		margin = ((selling_price - unit_cost) / unit_cost) * 100 if unit_cost else 0
		part_value = round(stock_qty * unit_cost, 2)
		total_value += part_value
		total_stock += stock_qty

		data.append({
			"part_name": p.get("part_name"),
			"part_code": p.get("part_code"),
			"device_type": p.get("compatible_device_type"),
			"stock_qty": stock_qty,
			"reorder_level": reorder_level,
			"unit_cost": unit_cost,
			"selling_price": selling_price,
			"margin": round(margin, 2),
			"total_value": part_value,
		})

	# Add total row with all columns
	data.append({
		"part_name": "Total",
		"part_code": "",
		"device_type": "",
		"stock_qty": total_stock,
		"reorder_level": "",
		"unit_cost": "",
		"selling_price": "",
		"margin": "",
		"total_value": round(total_value, 2),
	})
	return data

def get_summary(data):
	total_parts = len(data)-1
	below_order=0
	total_value=0

	for d in data:
		if d.get("stock_qty") and d.get("reorder_level"):
			if d["stock_qty"]<= d["reorder_level"]:
				below_order+=1
		total_value+=d.get("total_value",0)

	return [
		{"label": "Total Parts", "value": total_parts, "indicator": "Blue"},
		{"label": "Below Reorder Level", "value": below_order, "indicator": "Red"},
		{"label": "Total Inventory Value", "value": total_value, "indicator": "Green"},
	]