// Copyright (c) 2025, admin and contributors
// For license information, please see license.txt

function update_total_amount(frm) {
    let total = 0;
    (frm.doc.sales_report || []).forEach(row => {
        total += flt(row.amount || 0);
    });
    frm.set_value('total_amount', total);
}

frappe.ui.form.on('saleschild', { 
    quantity(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.quantity && row.rate) {
            frappe.model.set_value(cdt, cdn, 'amount', flt(row.quantity) * flt(row.rate));
        }
        update_total_amount(frm);
    },
    rate(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.quantity && row.rate) {
            frappe.model.set_value(cdt, cdn, 'amount', flt(row.quantity) * flt(row.rate));
        }
        update_total_amount(frm);
    },
    item(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.quantity = 0;
        row.amount = 0;
        frm.refresh_field('sales_report'); // fixed fieldname
        update_total_amount(frm);
    },
    amount(frm, cdt, cdn) {
        update_total_amount(frm);
    }
});

frappe.ui.form.on('Sales Report', {
    refresh(frm) {
        frm.add_custom_button("Edit Sales Report", function() {
            if (!frm.doc.sales_report || frm.doc.sales_report.length === 0) {
                frappe.msgprint("No Sales Report rows to edit.");
                return;
            }

            let table_data = frm.doc.sales_report.map(row => ({
                name: row.name,
                item: row.item,
                quantity: row.quantity,
                rate: row.rate,
                amount: row.amount
            }));

            let d = new frappe.ui.Dialog({
                title: 'Edit Sales Report Table',
                size: 'large',
                fields: [
                    {
                        fieldtype: 'Table',
                        fieldname: 'sales_report_table',
                        label: 'Sales Report',
                        cannot_add_rows: false,
                        in_place_edit: true,
                        data: table_data,
                        fields: [
                            {
                                fieldtype: 'Link',
                                fieldname: 'item',
                                label: 'Item',
                                options: 'Item', // Fixed
                                reqd: 1,
                                in_list_view: true,
                                onchange: async function () {
                                    const grid = d.fields_dict.sales_report_table.grid;
                                    const data = grid.get_data(); 
                                    for (let row of data) {
                                        if (row.item) {
                                            try {
                                                const item_doc = await frappe.db.get_doc('Item', row.item);
                                                row.rate = item_doc.price || 0;
                                                row.amount = flt(row.quantity || 0) * flt(row.rate);
                                            } catch (err) {
                                                console.error(`Failed to fetch item ${row.item}:`, err);
                                                row.rate = 0;
                                                row.amount = 0;
                                            }
                                        }
                                    }
                                    grid.refresh(); 
                                }
                            },
                            {
                                fieldtype: 'Int',
                                fieldname: 'quantity',
                                label: 'Quantity',
                                reqd: 1,
                                in_list_view: true
                            },
                            {
                                fieldtype: 'Int',
                                fieldname: 'rate',
                                label: 'Rate',
                                reqd: 1,
                                in_list_view: true
                            },
                            {
                                fieldtype: 'Int',
                                fieldname: 'amount',
                                label: 'Amount',
                                read_only: 1,
                                in_list_view: true
                            }
                        ]
                    }
                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    d.hide();

                    let updated_data = values.sales_report_table || [];

                    updated_data.forEach(row => {
                        row.amount = flt(row.quantity || 0) * flt(row.rate || 0);
                    });

                    frappe.call({
                        method: "sales.sales.doctype.sales_report.sales_report.update_sales_report",
                        args: {
                            docname: frm.doc.name,
                            updated_children_json: JSON.stringify(updated_data)
                        },
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.msgprint("Sales Report Updated Successfully");
                                frm.reload_doc();
                            }
                        }
                    });
                }
            });

            d.show();
        });
    },
    sales_report_add(frm) {
        update_total_amount(frm);
    },
    sales_report_remove(frm) {
        update_total_amount(frm);
    },
    sales_report_on_form_rendered(frm) {
        update_total_amount(frm);
    }
});
