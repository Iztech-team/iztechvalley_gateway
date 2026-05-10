import frappe


@frappe.whitelist()
def get_my_tenant_sites():
	"""Return list of tenant sites the current user can access.

	- Guest: raises AuthenticationError
	- Administrator: returns all active sites (for management)
	- Regular users: filtered via User Tenant Access records
	"""
	user = frappe.session.user

	if user == "Guest":
		frappe.throw("Authentication required", frappe.AuthenticationError)

	if user == "Administrator":
		return frappe.get_all(
			"Tenant Site",
			filters={"is_active": 1},
			fields=["name", "site_name", "domain"],
			order_by="site_name asc",
		)

	access_records = frappe.get_all(
		"User Tenant Access",
		filters={"user": user},
		fields=["tenant_site"],
	)

	if not access_records:
		return []

	site_names = [r.tenant_site for r in access_records]

	return frappe.get_all(
		"Tenant Site",
		filters={
			"name": ("in", site_names),
			"is_active": 1,
		},
		fields=["name", "site_name", "domain"],
		order_by="site_name asc",
	)
