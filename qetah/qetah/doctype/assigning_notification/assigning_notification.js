// Copyright (c) 2023, Tailor Shop and contributors
// For license information, please see license.txt

frappe.ui.form.on('Assigning Notification', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 0)
		{
			// frm.add_custom_button(__('Create Measurements'), () => {
			// 	frappe.model.open_mapped_doc({
			// 		method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.open_measurements",
			// 		frm: cur_frm
			// 	})
			// });

			frm.add_custom_button(__('Measurements'),
			function() {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.open_measurements",
					frm: cur_frm
				})
			}, __("Create"));


			frm.add_custom_button(__('Cutting'),
			function() {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.open_cutting",
					frm: cur_frm
				})
			}, __("Create"));

			frm.add_custom_button(__('Stitching'),
			function() {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.open_stitching",
					frm: cur_frm
				})
			}, __("Create"));


			frm.add_custom_button(__('Embroidery'),
			function() {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.open_embroidery",
					frm: cur_frm
				})
			}, __("Create"));


			frm.add_custom_button(__('Ironing'),
			function() {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.open_ironing",
					frm: cur_frm
				})
			}, __("Create"));

			frm.add_custom_button(__('Packing'),
			function() {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.open_packing",
					frm: cur_frm
				})
			}, __("Create"));

			// frm.add_custom_button(__('Send notification'), () => {
			// frm.set_value("send","")
   //          frappe.call({
   //              method: 'tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.measure_notify',
   //              args: {
   //                  'ref_name': frm.doc.name
   //              },
   //              callback: function(r) {
   //  				frm.set_value("send","sent")
   //  				frm.refresh_fields("send")
   //  				frm.save();
   //              }
   //          });
   //      	});
		}
	}
});
