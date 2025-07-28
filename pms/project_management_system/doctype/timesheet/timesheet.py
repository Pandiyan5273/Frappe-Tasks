import frappe
from frappe.model.document import Document
from datetime import datetime

class Timesheet(Document):
    def validate(self):
        for entry in self.timesheet_logs:
            if entry.from_time and entry.to_time:# validation of timing
                from_time = datetime.strptime(entry.from_time, "%Y-%m-%d %H:%M:%S")
                to_time = datetime.strptime(entry.to_time, "%Y-%m-%d %H:%M:%S")
                if from_time >= to_time:
                    frappe.throw(f"From Time must be less than To Time for Task {entry.task}.")
                time_diff = (to_time - from_time).total_seconds() / 3600 #calculating time
                entry.hours = round(time_diff, 2)
                if entry.hours > 2: # Assuming 2 hours is the maximum allowed
                    frappe.throw(f"Time difference for Task {entry.task} cannot exceed 2 hours (got {entry.hours} hours).")

    def on_submit(self):
        for entry in self.timesheet_logs: #task page change the status to Working
            if entry.task:
                frappe.db.set_value("Task", entry.task, "status", "Working")