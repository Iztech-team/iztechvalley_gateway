import frappe
import requests

def after_insert_user(doc, method):
    """Called after a User document is inserted on a Tenant."""
    
    # Only sync from tenant sites, not from Front Door itself
    if frappe.local.site == "login.iztechvalley.local":
        return
    
    # Don't sync system users
    if doc.name in ["Administrator", "Guest"]:
        return
    
    # Prepare data to send
    user_data = {
        "email": doc.name,
        "first_name": doc.first_name,
        "last_name": doc.last_name,
    }
    
    tenant_domain = frappe.local.site
    
    # Call Front Door API
    try:
        front_door_url = "http://login.iztechvalley.local/api/method/iztechvalley_gateway.api.user_sync.sync_user_from_tenant"
        response = requests.post(
            front_door_url,
            json={"user_data": user_data, "tenant_domain": tenant_domain},
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        frappe.log_error(f"User sync to Front Door: {response.status_code} - {response.text}", "User Sync")
    except Exception as e:
        frappe.log_error(f"Failed to sync user {doc.name}: {str(e)}", "User Sync")