# Copyright (c) 2023, Tailor Shop and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Ironing(Document):
	def validate(self):
		lst = []
		item = []
		for i in self.ironing_table:
			item_code = i.item_code
			total_qty = i.total_qty
			if item_code not in lst:
				lst.append(item_code)
				item.append({"item_code": item_code, "total_qty": total_qty})
			else:
				index = lst.index(item_code)
				item[index]["total_qty"] += total_qty

		lst1=[]
		item1=[]
		for i in self.sales_items:
			item_code = i.item_code
			qty = i.qty
			if item_code not in lst1:
				lst1.append(item_code)
				item1.append({"item_code": item_code, "qty": qty})
			else:
				index = lst1.index(item_code)
				item1[index]["qty"] += qty


		for m in item1:
			for n in item:
				if(m['item_code'] == n['item_code']):
					if(m['qty']<n['total_qty']):
						frappe.throw('Qty is Greater')
					else:
						pass

		if(self.ironing_table):
			pass
		else:
			frappe.throw("Ironing Table is Mandorary")
		dd = frappe.get_doc("Sales Order",self.sales_order)
		dd.workflow_state = 'Assign For Ironing'
		dd.save()

	def on_trash(self):
		dd = frappe.get_doc("Sales Order",self.sales_order)
		dd.workflow_state = 'Embroidery Completed'
		dd.save()

	def on_cancel(self):
		dd = frappe.get_doc("Sales Order",self.sales_order)
		dd.workflow_state = 'Embroidery Completed'
		dd.save()
	def on_submit(self):
		dd = frappe.get_doc("Sales Order",self.sales_order)
		dd.workflow_state = 'Ironing Completed'
		dd.save()
		sales_total=0
		assign_total=0
		for i in self.ironing_table:
			assign_total = assign_total + i.total_qty

		for i in self.sales_items:
			sales_total = sales_total + i.qty

		if(sales_total == assign_total):
			pass
		else:
			frappe.throw("Please allocate all the qty.")

		for i in self.ironing_table:
			user = i.user
			item = i.item_code
			qty = i.total_qty
			normal_qty = i.normal_qty
			urgent_qty = i.urgent_qty
			parent = i.parent
			sales_order = self.sales_order
			user_id = user
			notification_subject = f'{item} Ironing is Completed - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}, Completed by {user}'
			notification_message = 'Item Assigned.'
			notification = frappe.get_doc({
			"doctype": "Notification Log",
			"subject": notification_subject,
			"email_content": notification_message,
			"for_user":self.allocated_person,
			"document_type":"Ironing",
			"document_name":self.name,
			})
			notification.insert()
	# def on_submit(self):
	# 	for i in self.ironing_table:
	# 		user = i.user
	# 		item = i.item_code
	# 		qty = i.total_qty
	# 		status = i.status
	# 		normal_qty = i.normal_qty
	# 		urgent_qty = i.urgent_qty
	# 		total_qty = i.total_qty
	# 		if(i.status == 'Accept'):
	# 			notification_subject = f'Item Code - {item} - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty} - Total Qty - {total_qty} is Accepted for Ironing'
	# 			notification_message = 'Ironing Status.'
	# 			notification = frappe.get_doc({
	# 			"doctype": "Notification Log",
	# 			"subject": notification_subject,
	# 			"email_content": notification_message,
	# 			"for_user":user,
	# 			"document_type":"Ironing",
	# 			"document_name":self.name,
	# 			})
	# 			notification.insert()
	# 		elif(i.status == 'Reject'):
	# 			notification_subject = f'Item Code - {item} - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty} - Total Qty - {total_qty} is Rejected, Please redo the process'
	# 			notification_message = 'Ironing Status.'
	# 			notification = frappe.get_doc({
	# 			"doctype": "Notification Log",
	# 			"subject": notification_subject,
	# 			"email_content": notification_message,
	# 			"for_user":user,
	# 			"document_type":"Assigning Notification",
	# 			"document_name":self.assigning_allow,
	# 			})
	# 			notification.insert()

