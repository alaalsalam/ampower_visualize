import frappe

@frappe.whitelist()
def get_sales_order_links(doctype, docname):

	if not doctype or not docname:
		return []

	linked_docs = []
	sales_orders = get_sales_invoices_from_sales_order(docname)
	delivery_notes = get_delivery_notes_from_sales_order(docname)
	linked_docs.append(sales_orders[0])
	linked_docs.append(delivery_notes[0])
	return linked_docs

def get_sales_invoices_from_sales_order(sales_order_id):
    invoice_items = frappe.get_all(
        "Sales Invoice Item",
        filters={"sales_order": sales_order_id},
        fields=["parent"]
    )
    invoice_ids = [item["parent"] for item in invoice_items]
    if invoice_ids:
        sales_invoices = frappe.get_all(
            "Sales Invoice",
            filters={"name": ["in", invoice_ids]},
            fields=["name", "customer", "posting_date", "total", "status"]
        )
    else:
        sales_invoices = []
    return sales_invoices

def get_delivery_notes_from_sales_order(sales_order_id):
    delivery_note_items = frappe.get_all(
        "Delivery Note Item",
        filters={"against_sales_order": sales_order_id},
        fields=["parent"]
    )

    delivery_note_ids = [item["parent"] for item in delivery_note_items]

    if delivery_note_ids:
        delivery_notes = frappe.get_all(
            "Delivery Note",
            filters={"name": ["in", delivery_note_ids]},
            fields=["name", "customer", "posting_date", "total", "status"]
        )
    else:
        delivery_notes = []

    return delivery_notes
