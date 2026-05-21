import frappe

@frappe.whitelist(allow_guest=True)
def sync_user_from_tenant(user_data, tenant_domain):
    """Receive user data from tenant and sync (add/update/delete) on Front Door."""
    
    # Set user to Administrator to bypass permissions
    frappe.set_user("Administrator")
    
    # Clean tenant_domain (remove port if exists)
    tenant_domain = tenant_domain.split(":")[0].strip().lower()
    action = user_data.get("action", "insert")
    email = user_data.get("email")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    enabled = user_data.get("enabled", 1)
    
    # Verify tenant is valid (check if domain exists in Tenant Site)
    tenant_site = frappe.db.get_value("Tenant Site", {"domain": tenant_domain}, "name")
    if not tenant_site:
        return {"status": "error", "message": f"Unknown tenant: {tenant_domain}"}
    
    if not email:
        return {"status": "error", "message": "Email is required"}
    
    # =================================================================
    # DELETE ACTION - Remove user access only, not the entire user
    # =================================================================
    if action == "delete":
        # Delete only the access record for this specific user and tenant site
        frappe.db.delete("User Tenant Access", {"user": email, "tenant_site": tenant_site})
        frappe.db.commit()
        
        # Check if user still has access to any other tenant sites
        remaining_access = frappe.db.count("User Tenant Access", {"user": email})
        
        if remaining_access == 0:
            # No remaining access - delete the user completely
            if frappe.db.exists("User", email):
                frappe.delete_doc("User", email, force=True)
                frappe.db.commit()
            return {"status": "success", "message": f"User {email} deleted from Front Door (no remaining access)"}
        else:
            # User still has access to other sites - keep the user
            return {"status": "success", "message": f"Access removed for {email} on {tenant_site}. User still has access to {remaining_access} other site(s)"}
    
    # =================================================================
    # INSERT or UPDATE ACTION - Create or update user
    # =================================================================
    if not frappe.db.exists("User", email):
        # Create new user
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "send_welcome_email": 0,
            "enabled": enabled
        })
        user.insert(ignore_permissions=True)
        frappe.db.commit()
    else:
        # Update existing user
        user = frappe.get_doc("User", email)
        user.first_name = first_name
        user.last_name = last_name
        user.enabled = enabled
        user.save(ignore_permissions=True)
        frappe.db.commit()
    
    # Grant or update access - add User Tenant Access if not exists
    if not frappe.db.exists("User Tenant Access", {"user": email, "tenant_site": tenant_site}):
        from frappe.client import insert
        insert({
            "doctype": "User Tenant Access",
            "user": email,
            "tenant_site": tenant_site
        })
        frappe.db.commit()
    
    return {"status": "success", "message": f"User {email} synced (action: {action})"}