


frappe.ui.form.on('Timesheet Log', {
    task: function(frm, cdt, cdn) {
        frm.fields_dict['timesheet_logs'].grid.get_field('user').get_query = function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            if (!child.task) return {};
            return {
                query: "pms.project_management_system.doctype.task.task.get_task_assigned_users",
                filters: {
                    task: child.task
                }
            };
        };
        frappe.model.set_value(cdt, cdn, "user", "");
    }
});