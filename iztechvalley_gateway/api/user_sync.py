import frappe

@frappe.whitelist(allow_guest=True)
def sync_user_from_tenant(user_data, tenant_domain):
    """Receive user data from tenant and create/update on Front Door."""
    
    # Verify tenant is valid
    tenant_site = frappe.db.get_value("Tenant Site", {"domain": tenant_domain}, "name")
    if not tenant_site:
        return {"status": "error", "message": f"Unknown tenant: {tenant_domain}"}
    
    email = user_data.get("email")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    
    if not email:
        return {"status": "error", "message": "Email is required"}
    
    # Create or update user on Front Door using frappe.get_doc
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "send_welcome_email": 0,
            "enabled": 1
        })
        user.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "success", "message": f"User {email} created on Front Door"}
    else:
        return {"status": "exists", "message": f"User {email} already exists on Front Door"}