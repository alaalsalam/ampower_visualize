import frappe

@frappe.whitelist()
def get_sales_order_links(document_name="SAL-ORD-2024-00016"):
    sales_order = frappe.get_doc('Sales Order', document_name)

    result = {
        'items': []
    }

    for so_item in sales_order.items:
        item_links = {
            'item_code': so_item.item_code,
            'item_name': so_item.item_name,
            'sales_order_qty': so_item.qty,
            'sales_invoices': [],
            'delivery_notes': [],
            'material_requests': [],
            'purchase_orders': []
        }

        sales_invoices = get_sales_invoices_for_so_item(so_item)
        item_links['sales_invoices'] = sales_invoices

        delivery_notes = get_delivery_notes_for_so_item(so_item)
        item_links['delivery_notes'] = delivery_notes

        material_requests = get_material_requests_for_so_item(so_item)
        for mr in material_requests:
            mr['purchase_orders'] = get_purchase_orders_for_mr(mr['material_request'])
        item_links['material_requests'] = material_requests

        purchase_orders = get_purchase_orders_for_so_item(so_item)
        item_links['purchase_orders'] = purchase_orders

        result['items'].append(item_links)

    return result

def get_sales_invoices_for_so_item(so_item):
    sales_invoices = []

    sinv_items = frappe.get_all('Sales Invoice Item', 
        filters={
            'sales_order': so_item.parent,
            'item_code': so_item.item_code
        },
        fields=['parent', 'qty']
    )

    for sinv_item in sinv_items:
        sales_invoices.append({
            'sales_invoice': sinv_item['parent'],
            'qty': sinv_item['qty']
        })

    return sales_invoices

def get_delivery_notes_for_so_item(so_item):
    delivery_notes = []

    dn_items = frappe.get_all('Delivery Note Item', 
        filters={
            'against_sales_order': so_item.parent,
            'item_code': so_item.item_code
        },
        fields=['parent', 'qty']
    )

    for dn_item in dn_items:
        delivery_notes.append({
            'delivery_note': dn_item['parent'],
            'qty': dn_item['qty']
        })

    return delivery_notes

def get_material_requests_for_so_item(so_item):
    material_requests = []

    mr_items = frappe.get_all('Material Request Item', 
        filters={
            'sales_order_item': so_item.name,
            'item_code': so_item.item_code
        },
        fields=['parent', 'qty']
    )

    for mr_item in mr_items:
        material_requests.append({
            'material_request': mr_item['parent'],
            'qty': mr_item['qty']
        })

    return material_requests

def get_purchase_orders_for_mr(material_request_name):
    purchase_orders = []

    po_items = frappe.get_all('Purchase Order Item', 
        filters={'material_request': material_request_name},
        fields=['parent', 'qty']
    )

    for po_item in po_items:
        purchase_invoices = get_purchase_invoices_for_po(po_item['parent'])
        purchase_receipts = get_purchase_receipts_for_po(po_item['parent'])
        purchase_orders.append({
            'purchase_order': po_item['parent'],
            'qty': po_item['qty'],
            'purchase_invoices': purchase_invoices,
            'purchase_receipts': purchase_receipts
        })

    return purchase_orders

def get_purchase_orders_for_so_item(so_item):
    purchase_orders = []

    po_items = frappe.get_all('Purchase Order Item', 
        filters={
            'sales_order_item': so_item.name,
            'item_code': so_item.item_code
        },
        fields=['parent', 'qty']
    )

    for po_item in po_items:
        purchase_invoices = get_purchase_invoices_for_po(po_item['parent'])
        purchase_receipts = get_purchase_receipts_for_po(po_item['parent'])
        purchase_orders.append({
            'purchase_order': po_item['parent'],
            'qty': po_item['qty'],
            'purchase_invoices': purchase_invoices,
            'purchase_receipts': purchase_receipts
        })

    return purchase_orders

def get_purchase_invoices_for_po(purchase_order_name):
    purchase_invoices = []

    pi_items = frappe.get_all('Purchase Invoice Item', 
        filters={'purchase_order': purchase_order_name},
        fields=['parent', 'qty']
    )

    for pi_item in pi_items:
        purchase_invoices.append({
            'purchase_invoice': pi_item['parent'],
            'qty': pi_item['qty']
        })

    return purchase_invoices

def get_purchase_receipts_for_po(purchase_order_name):
    purchase_receipts = []

    pr_items = frappe.get_all('Purchase Receipt Item', 
        filters={'purchase_order': purchase_order_name},
        fields=['parent', 'qty']
    )

    for pr_item in pr_items:
        purchase_receipts.append({
            'purchase_receipt': pr_item['parent'],
            'qty': pr_item['qty']
        })

    return purchase_receipts
