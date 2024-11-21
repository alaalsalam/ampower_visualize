import frappe


@frappe.whitelist()
def get_sales_order_links(sales_order_name="SAL-ORD-2021-00014"):
    try:
        sales_order_items = frappe.get_all(
            "Sales Order Item",
            fields=["item_code", "item_name", "qty"],
            filters={"parent": sales_order_name},
        )

        result = []

        for item in sales_order_items:
            item_data = {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "sales_order_qty": item.qty,
                "sales_invoices": [],
                "delivery_notes": [],
                "material_requests": [],
                "purchase_orders": [],
                "purchase_invoices": [],
                "purchase_receipts": [],
            }

            sales_invoice_items = frappe.get_all(
                "Sales Invoice Item",
                fields=["parent", "qty"],
                filters={
                    "sales_order": sales_order_name,
                    "item_code": item.item_code,
                },
            )
            for si_item in sales_invoice_items:
                si_status = frappe.db.get_value("Sales Invoice", si_item.parent, "status")
                if si_status != "Cancelled":
                    item_data["sales_invoices"].append({
                        "sales_invoice": si_item.parent,
                        "qty": si_item.qty
                    })

            delivery_note_items = frappe.get_all(
                "Delivery Note Item",
                fields=["parent", "qty"],
                filters={
                    "against_sales_order": sales_order_name,
                    "item_code": item.item_code,
                },
            )
            for dn_item in delivery_note_items:
                dn_status = frappe.db.get_value("Delivery Note", dn_item.parent, "status")
                if dn_status != "Cancelled":
                    item_data["delivery_notes"].append({
                        "delivery_note": dn_item.parent,
                        "qty": dn_item.qty
                    })

            material_request_items = frappe.get_all(
                "Material Request Item",
                fields=["parent", "qty"],
                filters={
                    "sales_order": sales_order_name,
                    "item_code": item.item_code,
                },
            )
            for mr_item in material_request_items:
                mr_status = frappe.db.get_value("Material Request", mr_item.parent, "status")
                if mr_status != "Cancelled":
                    item_data["material_requests"].append({
                        "material_request": mr_item.parent,
                        "qty": mr_item.qty
                    })

            purchase_order_items = frappe.get_all(
                "Purchase Order Item",
                fields=["parent", "qty"],
                filters={
                    "sales_order": sales_order_name,
                    "item_code": item.item_code,
                },
            )
            for po_item in purchase_order_items:
                po_status = frappe.db.get_value("Purchase Order", po_item.parent, "status")
                if po_status != "Cancelled":
                    item_data["purchase_orders"].append({
                        "purchase_order": po_item.parent,
                        "qty": po_item.qty
                    })

            purchase_invoice_items = frappe.get_all(
                "Purchase Invoice Item",
                fields=["parent", "qty"],
                filters={
                    "purchase_order": ["in", [po["purchase_order"] for po in item_data["purchase_orders"]]],
                    "item_code": item.item_code,
                },
            )
            for pi_item in purchase_invoice_items:
                pi_status = frappe.db.get_value("Purchase Invoice", pi_item.parent, "status")
                if pi_status != "Cancelled":
                    item_data["purchase_invoices"].append({
                        "purchase_invoice": pi_item.parent,
                        "qty": pi_item.qty
                    })

            purchase_receipt_items = frappe.get_all(
                "Purchase Receipt Item",
                fields=["parent", "qty"],
                filters={
                    "purchase_order": ["in", [po["purchase_order"] for po in item_data["purchase_orders"]]],
                    "item_code": item.item_code,
                },
            )
            for pr_item in purchase_receipt_items:
                pr_status = frappe.db.get_value("Purchase Receipt", pr_item.parent, "status")
                if pr_status != "Cancelled":
                    item_data["purchase_receipts"].append({
                        "purchase_receipt": pr_item.parent,
                        "qty": pr_item.qty
                    })

            result.append(item_data)

        return {"status": "success", "items": result}

    except Exception as e:
        frappe.log_error(message=str(e), title="Sales Order Traceability Error")
        return {"status": "error", "message": str(e)}
