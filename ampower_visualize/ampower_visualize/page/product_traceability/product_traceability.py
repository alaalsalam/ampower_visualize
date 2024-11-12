import frappe

@frappe.whitelist()
def get_sales_order_links(docname="SAL-ORD-2024-00011"):

	if not docname:
		return []

	linked_docs = []

	material_requests = get_material_requests_from_sales_order(docname)
	delivery_notes = get_delivery_notes_from_sales_order(docname)
	sales_invoices = get_sales_invoices_from_sales_order(docname)

	linked_docs.append(material_requests)
	linked_docs.append(delivery_notes)
	linked_docs.append(sales_invoices)

	return linked_docs

def get_material_requests_from_sales_order(sales_order_name):
	
	sales_order = frappe.get_doc("Sales Order", sales_order_name)
	material_requests = {}
	
	for item in sales_order.items:
		material_request_items = frappe.get_all(
			"Material Request Item",
			filters={"sales_order_item": item.name},
			fields=["parent", "item_code", "qty", "parenttype"]
		)

		if material_request_items:
			for req_item in material_request_items:
				material_request = req_item.get("parent")

				if material_request not in material_requests:
					material_requests[material_request] = []

				material_requests[material_request].append({
					"item_code": req_item.get("item_code"),
					"quantity": req_item.get("qty"),
					"parenttype": req_item.get("parenttype")
				})

	return material_requests

def get_delivery_notes_from_sales_order(sales_order):
    delivery_notes = {}

    delivery_note_items = frappe.db.get_all(
        "Delivery Note Item",
        filters={"against_sales_order": sales_order},
        fields=["parent as delivery_note", "item_code", "qty as quantity", "parenttype"]
    )

    for item in delivery_note_items:
        delivery_note_id = item.pop("delivery_note")
        if delivery_note_id not in delivery_notes:
            delivery_notes[delivery_note_id] = []
        delivery_notes[delivery_note_id].append(item)

    return delivery_notes

@frappe.whitelist()
def get_sales_invoices_from_sales_order(sales_order):
    sales_invoices = {}

    sales_invoice_items = frappe.db.get_all(
        "Sales Invoice Item",
        filters={"sales_order": sales_order},
        fields=["parent as sales_invoice", "item_code", "qty as quantity", "parenttype"]
    )

    for item in sales_invoice_items:
        sales_invoice_id = item.pop("sales_invoice")
        if sales_invoice_id not in sales_invoices:
            sales_invoices[sales_invoice_id] = []
        sales_invoices[sales_invoice_id].append(item)

    return sales_invoices
