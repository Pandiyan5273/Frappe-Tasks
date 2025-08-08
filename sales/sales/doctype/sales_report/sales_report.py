# Copyright (c) 2025, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

import json
class SalesReport(Document):
	pass


import frappe
import json
from frappe.utils import flt


@frappe.whitelist()
def update_sales_report(docname, updated_children_json):
	updated_items = json.loads(updated_children_json)
	updated_names=[]
	for  row in updated_items:
		row_name= row.get("name")
		if row_name and frappe.db.exists("saleschild", row_name):
			item=updated_items[row_name]
			item.item= row.get("item")
			item.quantity= row.get("quantity")
			item.rate= row.get("rate")  
			item.amount= row.get("quantity") * row.get("rate")
			item.save()
			updated_names.append(item.name)
		else:
			new_row= frappe.new_doc("saleschild")
			new_row.item= row.get("item")
			new_row.quantity= row.get("quantity")
			new_row.rate= row.get("rate")
			new_row.amount= row.get("quantity") * row.get("rate")
			new_row.parent= docname
			new_row.parenttype= "Sales Report"
			new_row.parentfield= "sales_report"
			new_row.insert()
			updated_names.append(new_row.name)
			
	existing_items = frappe.get_all(
        "saleschild",
        filters={"parent": docname},
        fields=["name"]
    )
	for row in existing_items:
		if row.name not in updated_names:
			frappe.delete_doc("saleschild", row.name,ignore_permissions=
					 True)  
	frappe.db.sql("""
        UPDATE `tabSales Report`
        SET total_amount = (SELECT SUM(amount) FROM `tabsaleschild` WHERE parent = %s)
        WHERE name = %s
    """, (docname, docname))
	return "updated successfully"