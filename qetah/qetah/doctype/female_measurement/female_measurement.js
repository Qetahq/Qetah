// Copyright (c) 2024, noxer and contributors
// For license information, please see license.txt

frappe.ui.form.on('Female Measurement', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Female Measurement', {
	refresh(frm) {
		// your code here
		frm.set_value("total_dress",  frm.doc.normal + frm.doc.urgent1);

	}
});
