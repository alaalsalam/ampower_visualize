import frappe


@frappe.whitelist()
def get_sales_order_links(document_name):

	if not document_name:
		return []

	linked_docs = []

	delivery_notes = get_delivery_notes_from_sales_order(document_name)
	sales_invoices = get_sales_invoices_from_sales_order(document_name)
	material_requests = get_material_requests_from_sales_order(document_name)
	purchase_orders = get_purchase_orders_from_sales_order(document_name)

	linked_docs.append(delivery_notes)
	linked_docs.append(sales_invoices)
	linked_docs.append(material_requests)
	linked_docs.append(purchase_orders)

	return linked_docs


def get_delivery_notes_from_sales_order(sales_order):
	delivery_notes = {}

	delivery_note_items = frappe.db.get_all(
		"Delivery Note Item",
		filters={"against_sales_order": sales_order},
		fields=[
			"parent as delivery_note",
			"item_code",
			"qty as quantity",
			"parenttype",
		],
	)

	for item in delivery_note_items:
		delivery_note_id = item.pop("delivery_note")
		if delivery_note_id not in delivery_notes:
			delivery_notes[delivery_note_id] = []
		delivery_notes[delivery_note_id].append(item)

	return delivery_notes


def get_sales_invoices_from_sales_order(sales_order):
	sales_invoices = {}

	sales_invoice_items = frappe.db.get_all(
		"Sales Invoice Item",
		filters={"sales_order": sales_order},
		fields=[
			"parent as sales_invoice",
			"item_code",
			"qty as quantity",
			"parenttype",
		],
	)

	for item in sales_invoice_items:
		sales_invoice_id = item.pop("sales_invoice")
		if sales_invoice_id not in sales_invoices:
			sales_invoices[sales_invoice_id] = []
		sales_invoices[sales_invoice_id].append(item)

	return sales_invoices


def get_material_requests_from_sales_order(document_name):

	sales_order = frappe.get_doc("Sales Order", document_name)
	material_requests = {}

	for item in sales_order.items:
		material_request_items = frappe.get_all(
			"Material Request Item",
			filters={"sales_order_item": item.name},
			fields=["parent", "item_code", "qty", "parenttype"],
		)

		if material_request_items:
			for req_item in material_request_items:
				material_request = req_item.get("parent")

				if material_request not in material_requests:
					material_requests[material_request] = []

				material_requests[material_request].append(
					{
						"item_code": req_item.get("item_code"),
						"quantity": req_item.get("qty"),
						"parenttype": req_item.get("parenttype"),
					}
				)

	return material_requests


def get_purchase_orders_from_sales_order(sales_order):
	purchase_orders = {}

	purchase_order_items = frappe.db.get_all(
		"Purchase Order Item",
		filters={"sales_order": sales_order},
		fields=[
			"parent as sales_invoice",
			"item_code",
			"qty as quantity",
			"parenttype",
		],
	)

	for item in purchase_order_items:
		sales_invoice_id = item.pop("sales_invoice")
		if sales_invoice_id not in purchase_orders:
			purchase_orders[sales_invoice_id] = []
		purchase_orders[sales_invoice_id].append(item)

	return purchase_orders


@frappe.whitelist()
def get_material_request_links(document_name):
	if not document_name:
		return []

	linked_docs = []

	purchase_orders = get_purchase_orders_from_material_request(document_name)
	linked_docs.append(purchase_orders)
	return linked_docs


def get_purchase_orders_from_material_request(document_name):
	material_request = frappe.get_doc("Material Request", document_name)
	purchase_orders = {}

	for item in material_request.items:
		purchase_order_items = frappe.get_all(
			"Purchase Order Item",
			filters={"material_request_item": item.name},
			fields=["parent", "item_code", "qty", "parenttype"],
		)

		if purchase_order_items:
			for po_item in purchase_order_items:
				purchase_order = po_item.get("parent")

				if purchase_order not in purchase_orders:
					purchase_orders[purchase_order] = []

				purchase_orders[purchase_order].append(
					{
						"item_code": po_item.get("item_code"),
						"quantity": po_item.get("qty"),
						"parenttype": po_item.get("parenttype"),
					}
				)

	return purchase_orders


@frappe.whitelist()
def get_purchase_order_links(document_name):
	if not document_name:
		return []

	linked_docs = []

	purchase_receipts = get_purchase_receipts_from_purchase_order(document_name)
	purchase_invoices = get_purchase_invoices_from_purchase_order(document_name)

	linked_docs.append(purchase_receipts)
	linked_docs.append(purchase_invoices)

	return linked_docs


def get_purchase_receipts_from_purchase_order(document_name):
	purchase_receipts = {}

	purchase_receipt_items = frappe.db.get_all(
		"Purchase Receipt Item",
		filters={"purchase_order": document_name},
		fields=[
			"parent as purchase_receipt",
			"item_code",
			"qty as quantity",
			"parenttype",
		],
	)

	for item in purchase_receipt_items:
		purchase_receipt_id = item.pop("purchase_receipt")
		if purchase_receipt_id not in purchase_receipts:
			purchase_receipts[purchase_receipt_id] = []
		purchase_receipts[purchase_receipt_id].append(item)

	return purchase_receipts


def get_purchase_invoices_from_purchase_order(document_name):
	purchase_invoices = {}

	purchase_invoice_items = frappe.db.get_all(
		"Purchase Invoice Item",
		filters={"purchase_order": document_name},
		fields=[
			"parent as purchase_invoice",
			"item_code",
			"qty as quantity",
			"parenttype",
		],
	)

	for item in purchase_invoice_items:
		purchase_invoice_id = item.pop("purchase_invoice")
		if purchase_invoice_id not in purchase_invoices:
			purchase_invoices[purchase_invoice_id] = []
		purchase_invoices[purchase_invoice_id].append(item)

	return purchase_invoices
