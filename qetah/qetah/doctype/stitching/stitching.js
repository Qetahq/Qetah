// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stitching', {
	refresh: function(frm) {
		frm.set_df_property('stitching_table', 'cannot_add_rows', true);
       frm.set_df_property('stitching_table', 'cannot_delete_rows', true);
       frm.set_df_property('stitching_table', 'cannot_delete_all_rows', true);

        frm.set_df_property('sales_items', 'cannot_add_rows', true);
       frm.set_df_property('sales_items', 'cannot_delete_rows', true);
       frm.set_df_property('sales_items', 'cannot_delete_all_rows', true);

		frm.set_value('naming_series',"STI-ITEMS-")
		frm.refresh_field("naming_series")
		// if(frm.doc.docstatus == 0)
		// {
		// 	frm.add_custom_button(__('Send Notification'), () => {
		// 		frappe.model.open_mapped_doc({
		// 			method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.stitching_notify",
		// 			frm: cur_frm
		// 		})

		// 	});
		// }
		if(frm.doc.docstatus == 1)
		{
			frm.add_custom_button(__('Create Embroidery'), () => {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.create_embroidery",
					frm: cur_frm
				})
			});
		}

		frm.fields_dict['sales_items'].grid.add_custom_button('Add items', () => {	
			$.each(frm.doc.sales_items, function (index, source_row) {
			        if(source_row.__checked==true)
			        {
			        var childTable = cur_frm.add_child("stitching_table");
					childTable.item_code=source_row.item_code
					childTable.total_qty = source_row.qty
					childTable.normal_qty = source_row.normal_qty
					childTable.urgent_qty = source_row.urgent_qty
					childTable.reference=source_row.ref
					frm.refresh_fields("stitching_table");
			        }
				});
			});
	},
	onload:function(frm)
	{
		frm.set_value('naming_series',"STI-ITEMS-")
		frm.refresh_field("naming_series")
	}
});
