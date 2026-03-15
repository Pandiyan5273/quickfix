// Copyright (c) 2026, admin and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {
	   formatter: function(value, row, column, data, default_formatter) {
		   value = default_formatter(value, row, column, data);
		   if (row && row["stock_qty"] !== undefined && row["reorder_level"] !== undefined && row["stock_qty"] <= row["reorder_level"] && row["part_name"] !== "Total") {
			   value = `<span style="background-color:#ffcccc">${value}</span>`;
		   }
		   return value;
	   }
};
