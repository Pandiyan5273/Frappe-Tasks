# Copyright (c) 2025, admin and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns=[
		{"label": "User", "fieldname": "user", "fieldtype": "Link", "options": "User", "width": 200},
		{"label": "Total Hours", "fieldname": "total_hours", "fieldtype": "Float", "width": 120},
	]
	data = frappe.db.sql("""
		SELECT user, SUM(hours) as total_hours
		FROM `tabTimesheet Log`
		GROUP BY user
		ORDER BY total_hours DESC
	""", as_dict=True)
	return columns, data