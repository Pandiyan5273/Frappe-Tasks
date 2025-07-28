# Copyright (c) 2025, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Payslip(Document):
    def on_submit(self):
        self.send_payslip_email()

    def send_payslip_email(self):
        if self.user:
            
            pdf = frappe.get_print(
                    doctype="Payslip",
                    name=self.name,
                    print_format="Payslip Receipt",  
                    as_pdf=True,
                    no_letterhead=0
                )
            subject = f"Payslip for {self.from_date} to {self.to_date}"
            message = f"""
                <h3>Payslip Receipt</h3>
                <p><b>User:</b> {self.user}</p>
                <p><b>Period:</b> {self.from_date} to {self.to_date}</p>
            """
            frappe.sendmail(
                recipients=[self.user],
                subject=subject,
                message=message,
                attachments=[{
                    "fname": f"Payslip_{self.user}_{self.from_date}_to_{self.to_date}.pdf",
                    "fcontent": pdf
                }]
            )

    def validate(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                frappe.throw("From Date must be before To Date.")
    
          

@frappe.whitelist()
def get_user_payslip_details(user, from_date, to_date):
    # Calculate working hours for this user in the date range   
    working_hours = frappe.db.sql("""
        SELECT SUM(hours) FROM `tabTimesheet Log` tlog
        WHERE tlog.user=%s AND tlog.from_time >= %s AND tlog.to_time <= %s
    """, (user, from_date, to_date))[0][0] or 0
    amount = 30 * (working_hours * 60)
    return {
        "working_hours": working_hours,
        "amount": amount
    }