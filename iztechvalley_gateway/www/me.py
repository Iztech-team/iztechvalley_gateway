import frappe

no_cache = 1


def get_context(context):
	"""Render the site picker page for the logged-in user."""
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login?redirect-to=/me"
		raise frappe.Redirect

	from iztechvalley_gateway.api.tenant_picker import get_my_tenant_sites

	context.tenant_sites = get_my_tenant_sites()
	context.user_email = frappe.session.user
	context.no_header = 1
	context.show_sidebar = False
	context.title = "Choose a site"
