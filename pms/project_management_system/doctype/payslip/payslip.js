frappe.ui.form.on('Payslip', {
    user: function(frm) {
        fetch_user_payslip_details(frm);
    },
    from_date: function(frm) {
        fetch_user_payslip_details(frm);
    },
    to_date: function(frm) {
        fetch_user_payslip_details(frm);
    }
});

function fetch_user_payslip_details(frm) {
    if (frm.doc.user && frm.doc.from_date && frm.doc.to_date) {
        frappe.call({
            method: "pms.project_management_system.doctype.payslip.payslip.get_user_payslip_details",
            args: {
                user: frm.doc.user,
                from_date: frm.doc.from_date,
                to_date: frm.doc.to_date
            },
            callback: function(r) {
                if (r.message) {
                    frm.clear_table("payslip_details");
                    let row = frm.add_child("payslip_details");
                    row.user = frm.doc.user;
                    row.working_hours = r.message.working_hours;
                    row.amount = r.message.amount;
                    frm.refresh_field("payslip_details");
                }
            }
        });
    }
}