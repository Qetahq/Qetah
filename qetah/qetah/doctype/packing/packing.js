// Copyright (c) 2023, Tailor Shop and contributors
// For license information, please see license.txt

frappe.ui.form.on('Packing', {
	refresh: function(frm) {
		frm.set_df_property('packing_table', 'cannot_add_rows', true);
		frm.set_df_property('packing_table', 'cannot_delete_rows', true);
		frm.set_df_property('packing_table', 'cannot_delete_all_rows', true);

		frm.set_df_property('sales_items', 'cannot_add_rows', true);
		frm.set_df_property('sales_items', 'cannot_delete_rows', true);
		frm.set_df_property('sales_items', 'cannot_delete_all_rows', true);

		frm.set_value('naming_series',"PACK-ITEMS-")
		frm.refresh_field("naming_series")
		// if(frm.doc.docstatus == 0)
		// {
		// 	frm.add_custom_button(__('Send Notification'), () => {
		// 		frappe.model.open_mapped_doc({
		// 			method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.packing_notify",
		// 			frm: cur_frm
		// 		})

		// 	});
		// }
		frm.fields_dict['sales_items'].grid.add_custom_button('Add items', () => {	
			$.each(frm.doc.sales_items, function (index, source_row) {
			        if(source_row.__checked==true)
			        {
			        var childTable = cur_frm.add_child("packing_table");
					childTable.item_code=source_row.item_code
					childTable.total_qty = source_row.qty
					childTable.normal_qty = source_row.normal_qty
					childTable.urgent_qty = source_row.urgent_qty
					childTable.reference=source_row.ref
					frm.refresh_fields("packing_table");
			        }
				});
		});
	},
	onload:function(frm)
	{
		frm.set_value('naming_series',"PACK-ITEMS-")
		frm.refresh_field("naming_series")
	}
});
