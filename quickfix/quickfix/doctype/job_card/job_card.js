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
                        job_card:frm.doc.name,
                        customer_email:frm.doc.customer_email
                    },
                    callback:function(){
                        frm.reload_doc();
                    }
                })
            })
        }
        if(frm.doc.docstatus==1){
        frm.add_custom_button("Reject Job",function(){
            let d=new frappe.ui.Dialog({
                title:"Reject Job",
                fields:[
                    {
                        label:"Rejection Reason",
                        fieldname:"rejection_reason",
                        fieldtype:"Small Text",
                        reqd:1
                    }
                ],
                primary_action_label:"Reject",
                primary_action(values){
                    frappe.call({
                        method:"quickfix.api.reject_job",
                        args:{
                            job_card:frm.doc.name,
                            reason:values.rejection_reason
                        },
                        callback:function(r){
                            frappe.msgprint({
                                title:__("Rejection"),
                                message:__("Job Rejected successfully"),
                        })
                        frm.reload_doc();
                        }
                    })
                    d.hide();
                }
            });
            d.show();
        })
        frm.add_custom_button("Transfer Technician",()=>{
            frappe.prompt(
                [
                    {
                        label:"New Technician",
                        fieldname:"technician",
                        fieldtype:"Link",
                        options:"Technician",
                        reqd:1,
                        placeholder:"select technician"
                    }
                ],
                function(values){
                    frappe.confirm("Are you sure you want to transfer this job?",()=>{
                        frappe.call({
                            method:"quickfix.api.transfer_technician",
                            args:{
                                job_card:frm.doc.name,
                                technician:values.technician
                            },
                            callback:function(){
                                frm.set_value("assigned_technician",values.technician);
                                frm.trigger("assigned_technician");
                                frappe.msgprint("technician transferred successfully..")
                            }
                        })
                    })
                },
                "Transfer Technician", // title of the popup
                "Transfer" //primary button
            )
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

// frappe.ui.form.on('Job Card', {
//     refresh: function(frm) {
//         if (!frappe.user.has_role("Manager")) {
//             frm.set_df_property("customer_phone", "hidden", 1);
//         } else {
//             frm.set_df_property("customer_phone", "hidden", 0);
//         }

//     }
// });