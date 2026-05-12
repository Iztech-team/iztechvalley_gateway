import frappe
import hashlib
import json
from frappe.utils import now_datetime, add_to_date


@frappe.whitelist()
def get_my_tenant_sites():
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


def generate_sso_token(user, tenant_site):
    """Generate a time-limited SSO token for a user and specific tenant."""
    secret = frappe.get_site_config().get("sso_secret")
    if not secret:
        frappe.throw("SSO secret not configured")

    expires = add_to_date(now_datetime(), hours=1)
    payload = {
        "user": user,
        "tenant": tenant_site,
        "exp": expires.isoformat()
    }
    payload_str = json.dumps(payload, sort_keys=True)
    token = hashlib.sha256(f"{payload_str}:{secret}".encode()).hexdigest()
    return f"{payload_str}:{token}"


@frappe.whitelist(allow_guest=True)
def verify_user_credentials(usr, pwd):
    """Verify user credentials against all tenants and return accessible sites."""
    import requests
    from frappe import _
    
    # Get all active tenant sites
    all_sites = frappe.get_all("Tenant Site", filters={"is_active": 1}, fields=["name", "site_name", "domain"])
    
    accessible_sites = []
    
    for site in all_sites:
        try:
            # Try to login to this tenant
            login_url = f"http://{site['domain']}/api/method/login"
            response = requests.post(
                login_url, 
                data={"usr": usr, "pwd": pwd}, 
                timeout=5,
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Logged In":
                    # Login successful
                    accessible_sites.append({
                        "name": site["name"],
                        "site_name": site["site_name"],
                        "domain": site["domain"]
                    })
                    frappe.log_error(f"Login successful for {usr} on {site['domain']}", "SSO Login")
        except Exception as e:
            frappe.log_error(f"Failed to check tenant {site['domain']}: {str(e)}", "SSO Login")
    
    return accessible_sites