# Copyright (c) 2025, admin and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Project", "fieldname": "name", "fieldtype": "Link", "options": "Project", "width": 200},
        {"label": "Project Name", "fieldname": "project_name", "fieldtype": "Data", "width": 200},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Completion %", "fieldname": "completion_percent", "fieldtype": "Percent", "width": 120},
    ]
    data = frappe.get_all(
        "Project",
        filters={"status": "Completed"},
        fields=["name", "project_name", "status", "completion_percent"]
    )
    return columns, data