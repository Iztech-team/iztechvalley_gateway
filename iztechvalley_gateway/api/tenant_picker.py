import frappe
import hashlib
import json
import secrets
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


def _create_sso_token(usr, site_names):
    """Create a one-time SSO token valid for 5 minutes."""
    token = secrets.token_urlsafe(32)
    expires = add_to_date(now_datetime(), minutes=5)
    
    frappe.get_doc({
        "doctype": "SSO Token",
        "token": token,
        "user": usr,
        "allowed_sites": "\n".join(site_names),
        "expires_at": expires,
        "used": 0
    }).insert(ignore_permissions=True)
    frappe.db.commit()
    
    return token


@frappe.whitelist(allow_guest=True)
def verify_user_credentials(usr, pwd):
    """Verify user credentials against all tenants and return accessible sites with token."""
    import requests
    from frappe import _
    
    # Get all active tenant sites
    all_sites = frappe.get_all("Tenant Site", filters={"is_active": 1}, fields=["name", "site_name", "domain"])
    
    accessible_site_names = []
    
    for site in all_sites:
        try:
            # Try to login to this tenant
            scheme = frappe.conf.get("gateway_scheme", "https")
            login_url = f"{scheme}://{site['domain']}/api/method/login"
            response = requests.post(
                login_url, 
                data={"usr": usr, "pwd": pwd}, 
                timeout=5,
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Logged In":
                    accessible_site_names.append(site["name"])
                    frappe.log_error(f"Login successful for {usr} on {site['domain']}", "SSO Login")
        except Exception as e:
            frappe.log_error(f"Failed to check tenant {site['domain']}: {str(e)}", "SSO Login")
    
    if not accessible_site_names:
        return []
    
    # Create a single token for all accessible sites
    token = _create_sso_token(usr, accessible_site_names)
    
    # Return sites with token
    result = []
    for site in all_sites:
        if site["name"] in accessible_site_names:
            result.append({
                "name": site["name"],
                "site_name": site["site_name"],
                "domain": site["domain"],
                "sso_token": token
            })
    
    return result


@frappe.whitelist(allow_guest=True)
def validate_sso_token(token, tenant_site):
    """Called by tenant to validate SSO token."""
    record = frappe.db.get_value(
        "SSO Token",
        {"token": token, "used": 0},
        ["name", "user", "allowed_sites", "expires_at"],
        as_dict=True
    )
    
    if not record:
        return {"status": "error", "message": "Invalid or already-used token"}
    
    if now_datetime() > record.expires_at:
        frappe.db.set_value("SSO Token", record.name, "used", 1)
        frappe.db.commit()
        return {"status": "error", "message": "Token expired"}
    
    allowed = record.allowed_sites.split("\n")
    
    # Convert tenant_site (domain) to site_name
    tenant_site_name = frappe.db.get_value("Tenant Site", {"domain": tenant_site}, "name")
    
    if tenant_site_name not in allowed:
        return {"status": "error", "message": f"Token not valid for this site. Allowed: {allowed}, Got: {tenant_site_name}"}
    
    # One-time use - mark as used
    frappe.db.set_value("SSO Token", record.name, "used", 1)
    frappe.db.commit()
    
    return {"status": "success", "user": record.user}
