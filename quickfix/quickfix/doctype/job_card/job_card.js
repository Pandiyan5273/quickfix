// Copyright (c) 2026, admin and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	setup(frm){
        frm.set_query("assigned_technician",function(){
            return {
                filters:{
                    status:"Active",
                    specialization:frm.doc.device_type
                }
            }
        })
    },
    refresh(frm){
              if (frm.doc.status === "Draft") {
            frm.dashboard.add_indicator(frm.doc.status, "gray");
        }
        if (frm.doc.status === "Pending Diagnosis") {
            frm.dashboard.add_indicator(frm.doc.status, "orange");
        }

        if (frm.doc.status === "Awaiting Customer Approval") {
            frm.dashboard.add_indicator(frm.doc.status, "yellow");
        }

        if (frm.doc.status === "In Repair") {
            frm.dashboard.add_indicator(frm.doc.status, "blue");
        }

        if (frm.doc.status === "Ready for Delivery") {
            frm.dashboard.add_indicator(frm.doc.status, "green");
        }

        if (frm.doc.status === "Delivered") {
            frm.dashboard.add_indicator(frm.doc.status, "green");
        }

        if (frm.doc.status === "Cancelled") {
            frm.dashboard.add_indicator(frm.doc.status, "red");
        }
        if(frm.doc.status==="Ready for Delivery" && frm.doc.docstatus===1){
            frm.add_custom_button("Mark as Delivered",function (){
                frappe.call({
                    method:"quickfix.api.mark_as_delivered",
                    args:{
                        job_card:frm.doc.name
                    },
                    callback:function(){
                        frm.reload_doc();
                    }
                })
            })
        }
    },
   assigned_technician: function(frm) {

    if (!frm.doc.assigned_technician) return;

    frappe.db.get_value(
        "Technician",
        frm.doc.assigned_technician,
        "specialization"
    ).then(r => {

        let spec = r.message.specialization;

        if (spec && frm.doc.device_type && spec !== frm.doc.device_type) {

            frappe.msgprint({
                title: __("Specialization Mismatch"),
                message: __("Selected technician specializes in {0}, but device type is {1}",
                    [spec, frm.doc.device_type]),
                indicator: "orange"
            });

        }

    });

},
    onload:function(frm){
        frappe.realtime.on("job_ready",function(data){
                frappe.show_alert({
                    message:"Job is ready for delivery",
                    indicator:"green"
                })
        })
    }
});
