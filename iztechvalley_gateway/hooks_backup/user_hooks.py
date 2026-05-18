import frappe
import requests

def sync_to_front_door(doc, action):
    """Helper function to sync user changes to Front Door"""
    print(f"=== sync_to_front_door called with action: {action} for {doc.name} ===", flush=True)
    # Only sync from tenant sites, not from Front Door itself
    if frappe.local.site == "login.iztechvalley.local":
        return
    
    # Don't sync system users
    if doc.name in ["Administrator", "Guest"]:
        return
    
    user_data = {
        "email": doc.name,
        "first_name": doc.first_name,
        "last_name": doc.last_name,
        "enabled": doc.enabled,
        "action": action  # "insert", "delete", "update"
    }
    
    tenant_domain = frappe.local.site
    
    try:
        front_door_domain = frappe.get_site_config().get("front_door_domain", "login.iztechvalley.local")
        front_door_url = f"http://{front_door_domain}/api/method/iztechvalley_gateway.api.user_sync.sync_user_from_tenant"
        response = requests.post(
            front_door_url,
            json={"user_data": user_data, "tenant_domain": tenant_domain},
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        frappe.log_error(f"User sync ({action}) to Front Door: {response.status_code} - {response.text[:200]}", "User Sync")
    except Exception as e:
        frappe.log_error(f"Failed to sync user {doc.name} ({action}): {str(e)}", "User Sync")


def after_insert_user(doc, method):
    """Called after a User is inserted"""
    sync_to_front_door(doc, "insert")


def on_update_user(doc, method):
    """Called when a User is updated"""
    sync_to_front_door(doc, "update")


def before_delete_user(doc, method):
    """Called before a User is deleted"""
    sync_to_front_door(doc, "delete")

def on_trash_user(doc, method):
    """Called when a User is deleted (trashed)"""
    print(f"=== on_trash_user called for {doc.name} on {frappe.local.site} ===", flush=True)
    sync_to_front_door(doc, "delete")

def validate_user(doc, method):
    """Called when a user is being validated (including before delete)"""
    # Check if the user is being deleted
    if doc.flags.ignore_permissions:
        # User is being deleted
        sync_to_front_door(doc, "delete")