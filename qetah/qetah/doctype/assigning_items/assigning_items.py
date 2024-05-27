# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class AssigningItems(Document):
	def validate(self):
		lst = []
		item = []
		for i in self.assigned_table:
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

		if(self.assigned_table):
			pass
		else:
			frappe.throw("Assigning Table is Mandorary")

		dd = frappe.get_doc("Sales Order",self.sales_order)
		dd.workflow_state = 'Measurement Assigned'
		dd.save()
	def on_trash(self):
		dd = frappe.get_doc("Sales Order",self.sales_order)
		dd.workflow_state = 'Approved'
		dd.save()

	def on_cancel(self):
		dd = frappe.get_doc("Sales Order",self.sales_order)
		dd.workflow_state = 'Approved'
		dd.save()


	def on_submit(self):
		sales_total=0
		assign_total=0
		for i in self.assigned_table:
			assign_total = assign_total + i.total_qty

		for i in self.sales_items:
			sales_total = sales_total + i.qty

		if(sales_total == assign_total):
			pass
		else:
			frappe.throw("Please allocate all the qty.")

		for i in self.assigned_table:
			user = i.user
			item = i.item_code
			qty = i.total_qty
			normal_qty = i.normal_qty
			urgent_qty = i.urgent_qty
			parent = i.parent
			sales_order = self.sales_order
			user_id = user
			notification_subject = f'{item} Assigned for you to Measurements - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}, Assigned by {self.allocated_person}'
			notification_message = 'Item Assigned.'
			notification = frappe.get_doc({
			"doctype": "Notification Log",
			"subject": notification_subject,
			"email_content": notification_message,
			"for_user":user,
			"document_type":"Assigning Items",
			"document_name":self.name,
			})
			notification.insert()





@frappe.whitelist()
def assign_measure(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.type = "Measurements"
	doclist = get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Assigning Items",
				"field_map": {
					"name": "sales_order",
				},
				"postprocess": update_item,
			},
			"Sales Order Item": {
				"doctype": "Sales Items",
				"field_map": {
					"parent": "ref",
					"custom_normal_qty":"normal_qty",
					"custom_urgent_qty":"urgent_qty"
				},
				"condition": lambda doc: doc.item_group == "Services",
			},
		},
		target_doc,
	)
	return doclist



@frappe.whitelist()
def create_measure(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Assigning Items",
		source_name,
		{
			"Assigning Items": {
				"doctype": "Measurements Details",
				"field_map": {
					"name": "assigning_items",
				},
			},
			"Sales Items": {
				"doctype": "Measurements Sales Items",
				"field_map": {
					"parent": "ref",
				},
			},
		},
		target_doc,
	)
	return doclist


@frappe.whitelist()
def create_cutting(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Measurements Details",
		source_name,
		{
			"Measurements Details": {
				"doctype": "Cutting",
				"field_map": {
					"name": "measurement_details",
				},
			},
			"Measurements Sales Items": {
				"doctype": "Cutting Sales Items",
				"field_map": {
					"parent": "ref",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def create_stitching(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Cutting",
		source_name,
		{
			"Cutting": {
				"doctype": "Stitching",
				"field_map": {
					"name": "cutting",
				},
			},
			"Cutting Sales Items": {
				"doctype": "Stitching Sales Items",
				"field_map": {
					"parent": "ref",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def create_embroidery(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Stitching",
		source_name,
		{
			"Stitching": {
				"doctype": "Embroidery",
				"field_map": {
					"name": "stitching",
				},
			},
			"Stitching Sales Items": {
				"doctype": "Embroidery Sales Items",
				"field_map": {
					"parent": "ref",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def create_ironing(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Embroidery",
		source_name,
		{
			"Embroidery": {
				"doctype": "Ironing",
				"field_map": {
					"name": "embroidery",
				},
			},
			"Embroidery Sales Items": {
				"doctype": "Ironing Sales Items",
				"field_map": {
					"parent": "ref",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def create_packing(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Ironing",
		source_name,
		{
			"Ironing": {
				"doctype": "Packing",
				"field_map": {
					"name": "ironing",
				},
			},
			"Ironing Sales Items": {
				"doctype": "Packing Sales Items",
				"field_map": {
					"parent": "ref",
				},
			},
		},
		target_doc,
	)
	return doclist


@frappe.whitelist()
def open_measurements(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Assigning Notification",
		source_name,
		{
			"Assigning Notification": {
				"doctype": "Measurements Details",
				"field_map": {
					"name": "assigning_allow",
				},
			},
			"Assigned Table": {
				"doctype": "Customer Measurement Table",
				"field_map": {
					"parent": "assigning_allow",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def open_cutting(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Assigning Notification",
		source_name,
		{
			"Assigning Notification": {
				"doctype": "Cutting",
				"field_map": {
					"name": "assigning_allow",
				},
			},
			"Assigned Table": {
				"doctype": "Cutting Details",
				"field_map": {
					"parent": "assigning_allow",
				},
			},
		},
		target_doc,
	)
	return doclist


@frappe.whitelist()
def open_stitching(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Assigning Notification",
		source_name,
		{
			"Assigning Notification": {
				"doctype": "Stitching",
				"field_map": {
					"name": "assigning_allow",
				},
			},
			"Assigned Table": {
				"doctype": "Stitching Table",
				"field_map": {
					"parent": "assigning_allow",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def open_embroidery(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Assigning Notification",
		source_name,
		{
			"Assigning Notification": {
				"doctype": "Embroidery",
				"field_map": {
					"name": "assigning_allow",
				},
			},
			"Assigned Table": {
				"doctype": "Embroidery Table",
				"field_map": {
					"parent": "assigning_allow",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def open_ironing(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Assigning Notification",
		source_name,
		{
			"Assigning Notification": {
				"doctype": "Ironing",
				"field_map": {
					"name": "assigning_allow",
				},
			},
			"Assigned Table": {
				"doctype": "Ironing Table",
				"field_map": {
					"parent": "assigning_allow",
				},
			},
		},
		target_doc,
	)
	return doclist


@frappe.whitelist()
def open_packing(source_name, target_doc=None):
	doclist = get_mapped_doc(
		"Assigning Notification",
		source_name,
		{
			"Assigning Notification": {
				"doctype": "Packing",
				"field_map": {
					"name": "assigning_allow",
				},
			},
			"Assigned Table": {
				"doctype": "Packing Table",
				"field_map": {
					"parent": "assigning_allow",
				},
			},
		},
		target_doc,
	)
	return doclist

@frappe.whitelist()
def send_notification(child_table_data):
	child_table_data = frappe.parse_json(child_table_data)
	for row in child_table_data:
		if row.get('notification') == "sent":
			pass
		else:
			user = row.get('user')
			item = row.get('item_code')
			qty = row.get('total_qty')
			normal_qty = row.get('normal_qty')
			urgent_qty = row.get('urgent_qty')
			parent = row.get('parent')
			sales_order = frappe.db.get_value("Assigning Items", row.get('parent'), "sales_order")
			assigning_type = frappe.db.get_value("Assigning Items", row.get('parent'), "type")
			if(assigning_type == 'Measurements'):
				user_id = user
				notification_subject = f'{item} Assigned for you to Measurements - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}'
				notification_message = 'Item Assigned.'
				dd = frappe.new_doc("Assigning Notification")
				dd.username = user
				dd.sales_order = sales_order
				dd.assigning_for = "Measurements"
				dd.append("user_table", {
					"user": user,
					"item_code": item,
					"normal_qty": normal_qty,
					"urgent_qty": urgent_qty,
					"total_qty": qty,
					"sales_order": sales_order
				})
				dd.insert()


				notification = frappe.get_doc({
				"doctype": "Notification Log",
				"subject": notification_subject,
				"email_content": notification_message,
				"for_user":user,
				"document_type":"Assigning Notification",
				"document_name":dd.name,
				})
				notification.insert()
			elif(assigning_type == 'Cutting'):
				user_id = user
				notification_subject = f'{item} Assigned for you to Cutting - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}'
				notification_message = 'Item Assigned.'
				dd = frappe.new_doc("Assigning Notification")
				dd.username = user
				dd.sales_order = sales_order
				dd.assigning_for = "Cutting"
				dd.append("user_table", {
					"user": user,
					"item_code": item,
					"normal_qty": normal_qty,
					"urgent_qty": urgent_qty,
					"total_qty": qty,
					"sales_order": sales_order
				})
				dd.insert()


				notification = frappe.get_doc({
				"doctype": "Notification Log",
				"subject": notification_subject,
				"email_content": notification_message,
				"for_user":user,
				"document_type":"Assigning Notification",
				"document_name":dd.name,
				})
				notification.insert()

			elif(assigning_type == 'Stitching'):
				user_id = user
				notification_subject = f'{item} Assigned for you to Stitching - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}'
				notification_message = 'Item Assigned.'
				dd = frappe.new_doc("Assigning Notification")
				dd.username = user
				dd.sales_order = sales_order
				dd.assigning_for = "Stitching"
				dd.append("user_table", {
					"user": user,
					"item_code": item,
					"normal_qty": normal_qty,
					"urgent_qty": urgent_qty,
					"total_qty": qty,
					"sales_order": sales_order
				})
				dd.insert()


				notification = frappe.get_doc({
				"doctype": "Notification Log",
				"subject": notification_subject,
				"email_content": notification_message,
				"for_user":user,
				"document_type":"Assigning Notification",
				"document_name":dd.name,
				})
				notification.insert()

			elif(assigning_type == 'Embroidery'):
				user_id = user
				notification_subject = f'{item} Assigned for you to Embroidery - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}'
				notification_message = 'Item Assigned.'
				dd = frappe.new_doc("Assigning Notification")
				dd.username = user
				dd.sales_order = sales_order
				dd.assigning_for = "Embroidery"
				dd.append("user_table", {
					"user": user,
					"item_code": item,
					"normal_qty": normal_qty,
					"urgent_qty": urgent_qty,
					"total_qty": qty,
					"sales_order": sales_order
				})
				dd.insert()


				notification = frappe.get_doc({
				"doctype": "Notification Log",
				"subject": notification_subject,
				"email_content": notification_message,
				"for_user":user,
				"document_type":"Assigning Notification",
				"document_name":dd.name,
				})
				notification.insert()

			elif(assigning_type == 'Ironing'):
				user_id = user
				notification_subject = f'{item} Assigned for you to Ironing - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}'
				notification_message = 'Item Assigned.'
				dd = frappe.new_doc("Assigning Notification")
				dd.username = user
				dd.sales_order = sales_order
				dd.assigning_for = "Ironing"
				dd.append("user_table", {
					"user": user,
					"item_code": item,
					"normal_qty": normal_qty,
					"urgent_qty": urgent_qty,
					"total_qty": qty,
					"sales_order": sales_order
				})
				dd.insert()


				notification = frappe.get_doc({
				"doctype": "Notification Log",
				"subject": notification_subject,
				"email_content": notification_message,
				"for_user":user,
				"document_type":"Assigning Notification",
				"document_name":dd.name,
				})
				notification.insert()

			elif(assigning_type == 'Packing'):
				user_id = user
				notification_subject = f'{item} Assigned for you to Packing - Normal Qty - {normal_qty} - Urgent Qty - {urgent_qty}'
				notification_message = 'Item Assigned.'
				dd = frappe.new_doc("Assigning Notification")
				dd.username = user
				dd.sales_order = sales_order
				dd.assigning_for = "Packing"
				dd.append("user_table", {
					"user": user,
					"item_code": item,
					"normal_qty": normal_qty,
					"urgent_qty": urgent_qty,
					"total_qty": qty,
					"sales_order": sales_order
				})
				dd.insert()


				notification = frappe.get_doc({
				"doctype": "Notification Log",
				"subject": notification_subject,
				"email_content": notification_message,
				"for_user":user,
				"document_type":"Assigning Notification",
				"document_name":dd.name,
				})
				notification.insert()
			
	return 'success'


@frappe.whitelist()
def measure_notify(ref_name):
	user = frappe.session.user
	ref_name = ref_name
	notification_subject = f'{user} Completed the Measurement, Kindly check the document - {ref_name}'
	notification_message = 'Measurement Completed.'
	notification = frappe.get_doc({
	"doctype": "Notification Log",
	"subject": notification_subject,
	"email_content": notification_message,
	"for_user":"Administrator",
	"document_type":"Measurements Details",
	"document_name":ref_name,
	})
	notification.insert()
			
	return 'success'

@frappe.whitelist()
def cutting_notify(ref_name):
	user = frappe.session.user
	ref_name = ref_name
	notification_subject = f'{user} Completed the Cutting, Kindly check the document - {ref_name}'
	notification_message = 'Cutting Completed.'
	notification = frappe.get_doc({
	"doctype": "Notification Log",
	"subject": notification_subject,
	"email_content": notification_message,
	"for_user":"Administrator",
	"document_type":"Cutting",
	"document_name":ref_name,
	})
	notification.insert()
			
	return 'success'

@frappe.whitelist()
def stitching_notify(ref_name):
	user = frappe.session.user
	ref_name = ref_name
	notification_subject = f'{user} Completed the Stitching, Kindly check the document - {ref_name}'
	notification_message = 'Stitching Completed.'
	notification = frappe.get_doc({
	"doctype": "Notification Log",
	"subject": notification_subject,
	"email_content": notification_message,
	"for_user":"Administrator",
	"document_type":"Stitching",
	"document_name":ref_name,
	})
	notification.insert()
			
	return 'success'

@frappe.whitelist()
def embroidery_notify(ref_name):
	user = frappe.session.user
	ref_name = ref_name
	notification_subject = f'{user} Completed the Embroidery, Kindly check the document - {ref_name}'
	notification_message = 'Embroidery Completed.'
	notification = frappe.get_doc({
	"doctype": "Notification Log",
	"subject": notification_subject,
	"email_content": notification_message,
	"for_user":"Administrator",
	"document_type":"Embroidery",
	"document_name":ref_name,
	})
	notification.insert()
			
	return 'success'

@frappe.whitelist()
def ironing_notify(ref_name):
	user = frappe.session.user
	ref_name = ref_name
	notification_subject = f'{user} Completed the Ironing, Kindly check the document - {ref_name}'
	notification_message = 'Ironing Completed.'
	notification = frappe.get_doc({
	"doctype": "Notification Log",
	"subject": notification_subject,
	"email_content": notification_message,
	"for_user":"Administrator",
	"document_type":"Ironing",
	"document_name":ref_name,
	})
	notification.insert()
	return 'success'

@frappe.whitelist()
def packing_notify(ref_name):
	user = frappe.session.user
	ref_name = ref_name
	notification_subject = f'{user} Completed the Packing, Kindly check the document - {ref_name}'
	notification_message = 'Packing Completed.'
	notification = frappe.get_doc({
	"doctype": "Notification Log",
	"subject": notification_subject,
	"email_content": notification_message,
	"for_user":"Administrator",
	"document_type":"Packing",
	"document_name":ref_name,
	})
	notification.insert()
	return 'success'

@frappe.whitelist()
def get_measurements(sales_order):
	ar=[]
	for i in frappe.db.sql("SELECT cmt.item_code,cmt.total_qty,md.name as mref FROM `tabCustomer Measurement Table` AS cmt INNER JOIN `tabMeasurements Details` as md ON md.name=cmt.parent WHERE md.docstatus!=2 and md.sales_order='"+str(sales_order)+"' and cmt.status='Accept'",as_dict=1):
		ar.append({
			"item_code":i.item_code,
			"total_qty":i.total_qty,
			"ref":i.mref
		})
	return ar


@frappe.whitelist()
def get_cutting(sales_order):
	ar=[]
	for i in frappe.db.sql("SELECT cmt.item_code,cmt.total_qty,md.name as mref FROM `tabCutting Details` AS cmt INNER JOIN `tabCutting` as md ON md.name=cmt.parent WHERE md.docstatus!=2 and md.sales_order='"+str(sales_order)+"' and cmt.status='Accept'",as_dict=1):
		ar.append({
			"item_code":i.item_code,
			"total_qty":i.total_qty,
			"ref":i.mref
		})
	return ar

@frappe.whitelist()
def get_stitching(sales_order):
	ar=[]
	for i in frappe.db.sql("SELECT cmt.item_code,cmt.total_qty,md.name as mref FROM `tabStitching Table` AS cmt INNER JOIN `tabStitching` as md ON md.name=cmt.parent WHERE md.docstatus!=2 and md.sales_order='"+str(sales_order)+"' and cmt.status='Accept'",as_dict=1):
		ar.append({
			"item_code":i.item_code,
			"total_qty":i.total_qty,
			"ref":i.mref
		})
	return ar

@frappe.whitelist()
def get_embroidery(sales_order):
	ar=[]
	for i in frappe.db.sql("SELECT cmt.item_code,cmt.total_qty,md.name as mref FROM `tabEmbroidery Table` AS cmt INNER JOIN `tabEmbroidery` as md ON md.name=cmt.parent WHERE md.docstatus!=2 and md.sales_order='"+str(sales_order)+"' and cmt.status='Accept'",as_dict=1):
		ar.append({
			"item_code":i.item_code,
			"total_qty":i.total_qty,
			"ref":i.mref
		})
	return ar

@frappe.whitelist()
def get_ironing(sales_order):
	ar=[]
	for i in frappe.db.sql("SELECT cmt.item_code,cmt.total_qty,md.name as mref FROM `tabIroning Table` AS cmt INNER JOIN `tabIroning` as md ON md.name=cmt.parent WHERE md.docstatus!=2 and md.sales_order='"+str(sales_order)+"' and cmt.status='Accept'",as_dict=1):
		ar.append({
			"item_code":i.item_code,
			"total_qty":i.total_qty,
			"ref":i.mref
		})
	return ar
