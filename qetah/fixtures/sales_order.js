frappe.ui.form.on("Sales Order", {
	refresh: function(frm) {
		if(frm.doc.docstatus==1)
		{
			frm.add_custom_button(__('Assigning Tailor'), () => {
				frappe.model.open_mapped_doc({
					method: "tailor_shop.tailor_shop.doctype.assigning_items.assigning_items.assign_measure",
					frm: cur_frm
				})
				});
		}
	}
});


frappe.ui.form.on('Sales Order Item', {
	custom_urgent_qty:function(frm, cdt, cdn)
	{
		var child = locals[cdt][cdn];
		if(child.qty<child.custom_urgent_qty)
		{
			var child = locals[cdt][cdn];
			frappe.model.set_value(cdt, cdn, "custom_urgent_qty",child.qty)
		}
		frappe.model.set_value(cdt, cdn, "custom_normal_qty",child.qty - child.custom_urgent_qty)
	},
	qty:function(frm, cdt, cdn)
	{
		var child = locals[cdt][cdn];
		if(child.qty<child.custom_urgent_qty)
		{
			var child = locals[cdt][cdn];
			frappe.model.set_value(cdt, cdn, "custom_urgent_qty",child.qty)
		}
		frappe.model.set_value(cdt, cdn, "custom_normal_qty",child.qty - child.custom_urgent_qty)
	},
	custom_urgent_rate:function(frm,cdt,cdn)
	{
		var child = locals[cdt][cdn];
		var cust_rate = child.custom_urgent_qty * child.custom_urgent_rate
		var final_rate = child.rate + cust_rate
		frappe.model.set_value(cdt, cdn, "price_list_rate",final_rate)	
		frappe.model.set_value(cdt, cdn, "base_price_list_rate",final_rate)	
		frappe.model.set_value(cdt, cdn, "rate",final_rate)	
	}
});