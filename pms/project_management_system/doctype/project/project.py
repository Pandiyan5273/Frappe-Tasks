from frappe.model.document import Document
import frappe

class Project(Document):

    def validate(self):
        frappe.log_error("validate")
        if self.status == "Active":
            self.completion_percent = 50
        elif self.status == "Completed":
            self.completion_percent = 100
        else:
            self.completion_percent = 0
        
                
    def notify_assignment(self):
        for row in self.assigned_to:
            user=row.user
            subject=f"New project is assigned: {self.project_name}"
            message=f"You have been assigned a new project: {self.project_name}."
            frappe.sendmail(recipients=[user], subject=subject, message=message)

    def notify_completion(self):
        for row in self.assigned_to:
            user=row.user
            subject=f"Your project Name {self.project_name} has been successfully completed"
            message=f"Yo9ur project {self.project_name} has been successfully completed."
            frappe.sendmail(recipients=[user],subject=subject,message=message)
    
    def on_update_after_submit(self):
        if self.status=="Active":
            self.notify_assignment()
            frappe.db.set_value("Project", self.name, "completion_percent", 50)
        elif self.status=="Completed":
            self.notify_completion()
            frappe.db.set_value("Project", self.name, "completion_percent", 100)
        else:
            frappe.db.set_value("Project", self.name, "completion_percent", 0)    
        self.reload()

