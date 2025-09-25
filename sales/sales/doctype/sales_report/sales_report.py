import frappe
import json
from frappe.model.document import Document
from frappe.utils import flt

class SalesReport(Document):
    pass

@frappe.whitelist()
def update_sales_report(docname, updated_children_json):
    updated_items = json.loads(updated_children_json)
    updated_names = []

    for row in updated_items:
        row_name = row.get("name")
        if row_name and frappe.db.exists("saleschild", row_name):
            item = frappe.get_doc("saleschild", row_name)
            item.item = row.get("item")
            item.quantity = flt(row.get("quantity"))
            item.rate = flt(row.get("rate"))
            item.amount = flt(row.get("quantity")) * flt(row.get("rate"))
            item.save(ignore_permissions=True)
            updated_names.append(item.name)
        else:
            new_row = frappe.new_doc("saleschild")
            new_row.item = row.get("item")
            new_row.quantity = flt(row.get("quantity"))
            new_row.rate = flt(row.get("rate"))
            new_row.amount = flt(row.get("quantity")) * flt(row.get("rate"))
            new_row.parent = docname
            new_row.parenttype = "Sales Report"
            new_row.parentfield = "sales_report"
            new_row.insert(ignore_permissions=True)
            updated_names.append(new_row.name)
 
    existing_items = frappe.get_all(
        "saleschild",
        filters={"parent": docname},
        fields=["name"]
    )

    for row in existing_items:
        if row.name not in updated_names:
            frappe.delete_doc("saleschild", row.name, ignore_permissions=True)

    frappe.db.sql("""
        UPDATE `tabSales Report`
        SET total_amount = (SELECT SUM(amount) FROM `tabsaleschild` WHERE parent = %s)
        WHERE name = %s
    """, (docname, docname))

    frappe.db.commit()
    return "updated successfully"
