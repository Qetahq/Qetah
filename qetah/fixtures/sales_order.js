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
	custom_is_this_urgent: function(frm, cdt, cdn)
	{
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "custom_urgent_qty", 0);
		frappe.model.set_value(cdt, cdn, "custom_urgent_rate", 0);
	},
custom_urgent_rate: function(frm, cdt, cdn) {
  let child = locals[cdt][cdn];

  // Find all the "Urgent Cost" items for the current row
  let urgent_cost_items = frm.doc.items.filter(function(item) {
    return item.item_code === "Urgent Cost" && item.docname === child.name;
  });

  // Update the existing "Urgent Cost" item, if any
  if (urgent_cost_items.length > 0) {
    urgent_cost_items.forEach(function(item) {
      frappe.model.set_value(item.doctype, item.name, "rate", child.custom_urgent_rate);
      frappe.model.set_value(item.doctype, item.name, "qty", child.custom_urgent_qty);
    });
  } else {
    // Find the index of the current row's item
    let current_item_idx = frm.doc.items.findIndex(function(item) {
      return item.name === child.name;
    });

    // Check if an "Urgent Cost" item already exists below the current row's item
    let urgent_cost_item_below = frm.doc.items.find(function(item, index) {
      return item.item_code === "Urgent Cost" && index > current_item_idx;
    });

    if (urgent_cost_item_below) {
      // Update the existing "Urgent Cost" item below the current row's item
      frappe.model.set_value(urgent_cost_item_below.doctype, urgent_cost_item_below.name, "rate", child.custom_urgent_rate);
      frappe.model.set_value(urgent_cost_item_below.doctype, urgent_cost_item_below.name, "qty", child.custom_urgent_qty);
    } else {
      // Create a new "Urgent Cost" item and insert it after the current row's item
      let new_item = frappe.model.add_child(frm.doc, "Sales Order Item", "items", current_item_idx + 2);
      new_item.item_code = "Urgent Cost";
      new_item.item_name = "Urgent Cost";
      new_item.uom = "Nos";
      new_item.rate = child.custom_urgent_rate;
      new_item.qty = child.custom_urgent_qty;
    }
  }

  // Refresh the item list
  refresh_field("items");
},

custom_urgent_qty: function(frm, cdt, cdn) {
  let child = locals[cdt][cdn];

  // Find all the "Urgent Cost" items for the current row
  let urgent_cost_items = frm.doc.items.filter(function(item) {
    return item.item_code === "Urgent Cost" && item.docname === child.name;
  });

  // Update the existing "Urgent Cost" item, if any
  if (urgent_cost_items.length > 0) {
    urgent_cost_items.forEach(function(item) {
      frappe.model.set_value(item.doctype, item.name, "rate", child.custom_urgent_rate);
      frappe.model.set_value(item.doctype, item.name, "qty", child.custom_urgent_qty);
    });
  } else {
    // Find the index of the current row's item
    let current_item_idx = frm.doc.items.findIndex(function(item) {
      return item.name === child.name;
    });

    // Check if an "Urgent Cost" item already exists below the current row's item
    let urgent_cost_item_below = frm.doc.items.find(function(item, index) {
      return item.item_code === "Urgent Cost" && index > current_item_idx;
    });

    if (urgent_cost_item_below) {
      // Update the existing "Urgent Cost" item below the current row's item
      frappe.model.set_value(urgent_cost_item_below.doctype, urgent_cost_item_below.name, "rate", child.custom_urgent_rate);
      frappe.model.set_value(urgent_cost_item_below.doctype, urgent_cost_item_below.name, "qty", child.custom_urgent_qty);
    } else {
      // Create a new "Urgent Cost" item and insert it after the current row's item
      let new_item = frappe.model.add_child(frm.doc, "Sales Order Item", "items", current_item_idx + 2);
      new_item.item_code = "Urgent Cost";
      new_item.item_name = "Urgent Cost";
      new_item.uom = "Nos";
      new_item.rate = child.custom_urgent_rate;
      new_item.qty = child.custom_urgent_qty;
    }
  }

  // Refresh the item list
  refresh_field("items");
}

});

frappe.ui.form.on('Sales Order', {
    onload: function(frm) {
        // Set the delivery date to the current date for new Sales Orders
        if (frm.is_new()) {
            const today = frappe.datetime.get_today();
            frappe.model.set_value('Sales Order', frm.doc.name, 'delivery_date', today);
        }
    }
});