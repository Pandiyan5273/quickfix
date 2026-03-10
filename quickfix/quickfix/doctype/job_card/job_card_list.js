frappe.listview_settings["Job Card"]={
    add_fields:["status","final_amount","priority"],
    has_indicator_for_draft:true,
    get_indicator:function(doc){
        if(doc.status==="Draft"){
            return [__("Draft"),"gray","status,=,Draft"]
        }
        if(doc.status==="Cancelled"){
            return [__("Cancelled"),"red","status,=,Cancelled"]
        }
        if(doc.status==="Ready for Delivery"){
            return ["Ready For Delivery","green","status,=,Ready For Delivery"]
        }

    },
    formatters:{
     final_amount(value){
        if(!value) return "";
        return `<span style="font-weight:bold;color:black">₹ ${value}</span>`;
     }
    },
    button:{
        show: function (doc){
            return doc.status=="In Repair"
        },
        get_label:function (){
            return "Start Repair"
        },
        get_description:function(doc){
            return ("View {0}",[`${doc.status}`])
        },
        action:function(doc){
            frappe.db.set_value("Job Card",doc.name,"status","Ready for Delivery").then(()=>{
                frappe.msgprint("status changed to ready for delivery"+doc.name);
                cur_list.refresh();
            })
        }
    }

}
