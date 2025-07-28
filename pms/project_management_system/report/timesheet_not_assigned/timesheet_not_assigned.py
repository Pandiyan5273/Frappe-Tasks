import frappe

def execute(filters=None):
    columns = [
        {"label": "Project", "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 200},
        {"label": "User", "fieldname": "user", "fieldtype": "Link", "options": "User", "width": 200},
    ]

    # Get all user-project assignments from the child table
    assignments = frappe.db.sql("""
        SELECT ta.user, ta.parent AS project
        FROM `tabTask Assignment` ta
    """, as_dict=True)

    # Get all user-project pairs that have a timesheet log
    timesheet_pairs = frappe.db.sql("""
        SELECT DISTINCT tlog.user, t.project
        FROM `tabTimesheet Log` tlog
        JOIN `tabTimesheet` t ON tlog.parent = t.name
        WHERE t.project IS NOT NULL AND tlog.user IS NOT NULL
    """, as_dict=True)
    timesheet_set = {(row["user"], row["project"]) for row in timesheet_pairs}

    # Show only assignments where there is NO timesheet log
    data = [
        row for row in assignments
        if (row["user"], row["project"]) not in timesheet_set
    ]

    return columns, data