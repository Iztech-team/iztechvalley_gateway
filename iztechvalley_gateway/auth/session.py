import frappe
from urllib.parse import quote

FRONT_DOOR_SITE = frappe.get_site_config().get("front_door_domain", "login.iztechvalley.local")


def on_session_creation(login_manager=None):
    """Redirect user based on number of accessible sites.
    
    - If user has access to exactly 1 site → direct redirect with SSO token
    - If user has access to multiple sites → show site picker (/me)
    - If user has no access → show site picker (will show empty message)
    - Administrator follows same rules (based on their site access)
    """
    if frappe.local.site != FRONT_DOOR_SITE:
        return
    
    user = frappe.session.user
    
    # Get accessible sites for this user
    from iztechvalley_gateway.api.tenant_picker import get_my_tenant_sites
    sites = get_my_tenant_sites()
    
    if len(sites) == 0:
        # No access to any site - show picker (will show "no access" message)
        frappe.local.response["home_page"] = "/me"
    elif len(sites) == 1:
        # Exactly one site - redirect directly with SSO token
        site = sites[0]
        from iztechvalley_gateway.api.tenant_picker import generate_sso_token
        token = generate_sso_token(user, site["name"])
        redirect_url = f"//{site['domain']}/sso_login?sso_token={quote(token)}"
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = redirect_url
    else:
        # Multiple sites - show picker
        frappe.local.response["home_page"] = "/me"