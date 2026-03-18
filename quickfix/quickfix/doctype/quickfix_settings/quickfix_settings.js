// Copyright (c) 2026, admin and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quickfix Settings", {
	refresh(frm) {
        frm.add_custom_button("Generate Monthly Revenue Report", function() {
            frappe.call({
                method: "quickfix.api.enqueue_monthly_revenue_report"
            });
        });
    }   
	});
