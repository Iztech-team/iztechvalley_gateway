import frappe

@frappe.whitelist(allow_guest=True)
def sync_user_from_tenant(user_data, tenant_domain):
    """Receive user data from tenant and sync (add/update/delete) on Front Door."""
    
    # Set user to Administrator to bypass permissions
    frappe.set_user("Administrator")
    
    # Clean tenant_domain
    tenant_domain = tenant_domain.split(":")[0].strip().lower()
    action = user_data.get("action", "insert")
    email = user_data.get("email")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")
    enabled = user_data.get("enabled", 1)
    
    # Verify tenant is valid
    tenant_site = frappe.db.get_value("Tenant Site", {"domain": tenant_domain}, "name")
    if not tenant_site:
        return {"status": "error", "message": f"Unknown tenant: {tenant_domain}"}
    
    if not email:
        return {"status": "error", "message": "Email is required"}
    
    # Handle DELETE action - فقط حذف الصلاحية، وليس المستخدم بالكامل
    if action == "delete":
        # حذف access record الخاص بهذا المستخدم وهذا الموقع فقط
        frappe.db.delete("User Tenant Access", {"user": email, "tenant_site": tenant_site})
        frappe.db.commit()
        
        # تحقق مما إذا كان المستخدم لا يزال لديه صلاحيات لمواقع أخرى
        remaining_access = frappe.db.count("User Tenant Access", {"user": email})
        
        if remaining_access == 0:
            # إذا لم يعد لديه أي صلاحيات، احذف المستخدم بالكامل
            if frappe.db.exists("User", email):
                frappe.delete_doc("User", email, force=True)
                frappe.db.commit()
            return {"status": "success", "message": f"User {email} deleted from Front Door (no remaining access)"}
        else:
            return {"status": "success", "message": f"Access removed for {email} on {tenant_site}. User still has access to {remaining_access} other site(s)"}
    
    # Handle INSERT or UPDATE
    if not frappe.db.exists("User", email):
        # Create user
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
        # Update user
        user = frappe.get_doc("User", email)
        user.first_name = first_name
        user.last_name = last_name
        user.enabled = enabled
        user.save(ignore_permissions=True)
        frappe.db.commit()
    
    # Grant or update access
    if not frappe.db.exists("User Tenant Access", {"user": email, "tenant_site": tenant_site}):
        from frappe.client import insert
        insert({
            "doctype": "User Tenant Access",
            "user": email,
            "tenant_site": tenant_site
        })
        frappe.db.commit()
    
    return {"status": "success", "message": f"User {email} synced (action: {action})"}