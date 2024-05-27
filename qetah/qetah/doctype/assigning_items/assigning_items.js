// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assigning Items', {
	refresh: function(frm) {
		if(frm.doc.allocated_person)
		{

		}
		else
		{
			frm.set_value("allocated_person",frappe.session.user);
			frm.refresh_field("allocated_person");
		}
		if(frm.doc.docstatus == 1)
		{
			frm.add_custom_button(__('Cutting'), () => {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.create_cutting",
					frm: cur_frm
				})
			});
		}
		if(frm.doc.docstatus == 0)
		{
			// frm.add_custom_button(__('Send notification'), () => {
			// frm.set_value("sent","")
   //          var child_table_data = frm.doc.assigned_table;
   //          frappe.call({
   //              method: 'tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.send_notification',
   //              args: {
   //                  'child_table_data': child_table_data
   //              },
   //              callback: function(r) {
   //              	$.each(frm.doc.assigned_table, function (index, source_row) {
			// 			source_row.notification="sent"
			// 		});
			// 		frm.refresh_fields("assigned_table");
   //  				frm.set_value("sent","sent")
   //  				frm.refresh_fields("sent")
   //  				frm.save();
   //              }
   //          });
   //      	});

   //      	frm.add_custom_button(__('Measurements'),
			// function() {
			// 	if(frm.doc.sales_order)
			// 	{
			// 		frappe.call({
	  //               method: 'tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.get_measurements',
	  //               args: {
	  //                   'sales_order': frm.doc.sales_order
	  //               },
	  //               callback: function(r) {
	  //               	frm.set_value("type","Cutting");
	  //               	frm.refresh_field("type");
	  //               	frm.clear_table("sales_items");
	  //               	for(var i=0;i<r.message.length;i++)
			// 			{     
			// 			var child = frm.add_child("sales_items");
			// 			frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
			// 			frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].total_qty);
			// 			frappe.model.set_value(child.doctype, child.name, "ref", r.message[i].ref);
			// 			frm.refresh_field("sales_items");
			// 			}
	  //               }
	  //           	});
			// 	}
			// 	else
			// 	{
			// 		frappe.throw("Please choose the sales order")
			// 	}

			// }, __("Get Items From"));


			// frm.add_custom_button(__('Cutting'),
			// function() {
			// 	if(frm.doc.sales_order)
			// 	{
			// 		frappe.call({
	  //               method: 'tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.get_cutting',
	  //               args: {
	  //                   'sales_order': frm.doc.sales_order
	  //               },
	  //               callback: function(r) {
	  //               	frm.set_value("type","Stitching");
	  //               	frm.refresh_field("type");
	  //               	frm.clear_table("sales_items");
	  //               	for(var i=0;i<r.message.length;i++)
			// 			{     
			// 			var child = frm.add_child("sales_items");
			// 			frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
			// 			frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].total_qty);
			// 			frappe.model.set_value(child.doctype, child.name, "ref", r.message[i].ref);
			// 			frm.refresh_field("sales_items");
			// 			}
	  //               }
	  //           	});
			// 	}
			// 	else
			// 	{
			// 		frappe.throw("Please choose the sales order")
			// 	}

			// }, __("Get Items From"));

			// frm.add_custom_button(__('Stitching'),
			// function() {
			// 	if(frm.doc.sales_order)
			// 	{
			// 		frappe.call({
	  //               method: 'tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.get_stitching',
	  //               args: {
	  //                   'sales_order': frm.doc.sales_order
	  //               },
	  //               callback: function(r) {
	  //               	frm.set_value("type","Embroidery");
	  //               	frm.refresh_field("type");
	  //               	frm.clear_table("sales_items");
	  //               	for(var i=0;i<r.message.length;i++)
			// 			{     
			// 			var child = frm.add_child("sales_items");
			// 			frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
			// 			frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].total_qty);
			// 			frappe.model.set_value(child.doctype, child.name, "ref", r.message[i].ref);
			// 			frm.refresh_field("sales_items");
			// 			}
	  //               }
	  //           	});
			// 	}
			// 	else
			// 	{
			// 		frappe.throw("Please choose the sales order")
			// 	}

			// }, __("Get Items From"));


			// frm.add_custom_button(__('Embroidery'),
			// function() {
			// 	if(frm.doc.sales_order)
			// 	{
			// 		frappe.call({
	  //               method: 'tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.get_embroidery',
	  //               args: {
	  //                   'sales_order': frm.doc.sales_order
	  //               },
	  //               callback: function(r) {
	  //               	frm.set_value("type","Ironing");
	  //               	frm.refresh_field("type");
	  //               	frm.clear_table("sales_items");
	  //               	for(var i=0;i<r.message.length;i++)
			// 			{     
			// 			var child = frm.add_child("sales_items");
			// 			frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
			// 			frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].total_qty);
			// 			frappe.model.set_value(child.doctype, child.name, "ref", r.message[i].ref);
			// 			frm.refresh_field("sales_items");
			// 			}
	  //               }
	  //           	});
			// 	}
			// 	else
			// 	{
			// 		frappe.throw("Please choose the sales order")
			// 	}

			// }, __("Get Items From"));


			// frm.add_custom_button(__('Ironing'),
			// function() {
			// 	if(frm.doc.sales_order)
			// 	{
			// 		frappe.call({
	  //               method: 'tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.get_ironing',
	  //               args: {
	  //                   'sales_order': frm.doc.sales_order
	  //               },
	  //               callback: function(r) {
	  //               	frm.set_value("type","Packing");
	  //               	frm.refresh_field("type");
	  //               	frm.clear_table("sales_items");
	  //               	for(var i=0;i<r.message.length;i++)
			// 			{     
			// 			var child = frm.add_child("sales_items");
			// 			frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
			// 			frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].total_qty);
			// 			frappe.model.set_value(child.doctype, child.name, "ref", r.message[i].ref);
			// 			frm.refresh_field("sales_items");
			// 			}
	  //               }
	  //           	});
			// 	}
			// 	else
			// 	{
			// 		frappe.throw("Please choose the sales order")
			// 	}

			// }, __("Get Items From"));



		}

		frm.fields_dict['sales_items'].grid.add_custom_button('Add items', () => {	
			$.each(frm.doc.sales_items, function (index, source_row) {
			        if(source_row.__checked==true)
			        {
			        var childTable = cur_frm.add_child("assigned_table");
					childTable.item_code=source_row.item_code
					childTable.total_qty = source_row.qty
					childTable.normal_qty = source_row.normal_qty
					childTable.urgent_qty = source_row.urgent_qty
					childTable.reference=source_row.ref
					frm.refresh_fields("assigned_table");
			        }
				});
			});
	}
});

frappe.ui.form.on('Assigned Table', {
	normal_qty:function(frm, cdt, cdn)
	{
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_qty",child.normal_qty + child.urgent_qty)
	},
	urgent_qty:function(frm, cdt, cdn)
	{
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_qty",child.normal_qty + child.urgent_qty)
	}
});