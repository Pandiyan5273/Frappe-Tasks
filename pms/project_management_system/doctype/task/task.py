import frappe
from frappe.model.document import Document

class Task(Document):
    def on_submit(self):
        if self.status=="Open":
            self.notify_open_assignment()

    def on_update_after_submit(self):
        if self.status == "Open":
            self.notify_open_assignment()
        elif self.status == "Completed":
            self.notify_completion()

    def notify_completion(self):
        for row in self.assigned_to:
            user=row.user
            subject=f"Your task {self.title1} has been successfully completed"
            message=f"Your task {self.title1} has been successfully completed."
            frappe.sendmail(recipients=[user], subject=subject, message=message)

    def notify_open_assignment(self):
        for row in self.assigned_to:
            user=row.user
            subject=f"New Task is Assigned:{self.title1}"
            message=f"You have been assigned a new task: {self.title1}."
            frappe.sendmail(recipients=[user], subject=subject, message=message)

@frappe.whitelist() #task filter
def get_project_users(doctype, txt, searchfield, start, page_len, filters):
    project = filters.get("project")
    if not project:
        return []
    users = frappe.get_all(
        "Task Assignment",
        filters={"parenttype": "Project", "parent": project},
        fields=["user"]
    )
    return [(u.user,) for u in users if u.user and txt.lower() in u.user.lower()]


@frappe.whitelist() #for timesheet flter
def get_task_assigned_users(doctype, txt, searchfield, start, page_len, filters):
    task = filters.get("task")
    if not task:
        return []
    users = frappe.get_all(
        "Task Assignment",
        filters={"parent": task},
        fields=["user"]
    )
    return [(u.user,) for u in users if u.user and (not txt or txt.lower() in u.user.lower())]