frappe.ui.form.on('*', {
    refresh: function(frm) {
        if(frappe.boot.quickfix_shop_name && frm.doc){
            console.log("Shop Name: " + frappe.boot.quickfix_shop_name);
            frm.page.set_title(frappe.boot.quickfix_shop_name);
        }
    }
});