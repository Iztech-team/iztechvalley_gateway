import frappe

FRONT_DOOR_SITE = "login.iztechvalley.local"
PICKER_PAGE = "/me"


def on_session_creation(login_manager=None):
	"""Redirect non-Administrator users to the site picker after login.

	Runs on every successful login. Guarded by site name so it never affects
	tenant sites even if this app is somehow installed there.
	"""
	if frappe.local.site != FRONT_DOOR_SITE:
		return

	if frappe.session.user == "Administrator":
		return

	frappe.local.response["home_page"] = PICKER_PAGE
