import frappe

no_cache = 1

def get_context(context):
    # First, try to log in with usr/pwd (coming from gateway)
    usr = frappe.form_dict.get("usr") or frappe.request.form.get("usr")
    pwd = frappe.form_dict.get("pwd") or frappe.request.form.get("pwd")
    
    if usr and pwd:
        # Try to authenticate with Frappe directly
        try:
            frappe.local.login_manager = frappe.auth.LoginManager()
            frappe.local.login_manager.authenticate(usr, pwd)
            frappe.local.login_manager.post_login()
            frappe.local.response["type"] = "redirect"
            frappe.local.response["location"] = "/app"
            frappe.db.commit()
            return context
        except Exception as e:
            frappe.log_error(f"SSO: usr/pwd auth failed for {usr}: {str(e)}", "SSO")
    
    # If reached here, no valid login
    frappe.local.flags.redirect_location = "/login"
    raise frappe.Redirect