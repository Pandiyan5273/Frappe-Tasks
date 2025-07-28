
frappe.ui.form.on('Task', {
    project: function(frm) {
        frm.clear_table("assigned_to"); 
        frm.refresh_field("assigned_to");
    },
    onload: function(frm) {
        set_user_query(frm);
    },
    refresh: function(frm) {
        set_user_query(frm);
    }
});

function set_user_query(frm) {
    frm.fields_dict['assigned_to'].grid.get_field('user').get_query = function(doc, cdt, cdn) {
        return {
            query: "pms.project_management_system.doctype.task.task.get_project_users",
            filters: {
                project: frm.doc.project
            }
        };
    };
}