import frappe
import hashlib
import json
from frappe.utils import now_datetime

# Enable debug logging
frappe.log_error("SSO: validate_sso_token function started", "SSO Debug")
with open('/tmp/sso_debug.log', 'a') as f:
    f.write(f"validate_sso_token called with token: {frappe.form_dict.get('sso_token', 'None')[:50]}\n")

def validate_sso_token():
    with open('/tmp/sso_debug.log', 'a') as f:
       f.write(f"TOKEN: {token}\n")
       f.write(f"SECRET: {frappe.get_site_config().get('sso_secret')}\n")
    frappe.log_error("SSO: validate_sso_token called", "SSO Debug")
    token = frappe.form_dict.get("sso_token")
    frappe.log_error(f"SSO: token = {token[:50] if token else 'None'}", "SSO Debug")
    
    if not token:
        return False
    
    if frappe.session.user != "Guest":
        frappe.log_error(f"SSO: User already logged in as {frappe.session.user}", "SSO Debug")
        return True
    
    try:
        parts = token.rsplit(":", 1)
        frappe.log_error(f"SSO: parts length = {len(parts)}", "SSO Debug")
        if len(parts) != 2:
            return False
        
        payload_str, signature = parts
        secret = frappe.get_site_config().get("sso_secret")
        frappe.log_error(f"SSO: secret exists = {bool(secret)}", "SSO Debug")
        
        if not secret:
            return False
        
        expected = hashlib.sha256(f"{payload_str}:{secret}".encode()).hexdigest()
        frappe.log_error(f"SSO: signature matches = {signature == expected}", "SSO Debug")
        if signature != expected:
                    with open('/tmp/sso_debug.log', 'a') as f:
                        f.write(f"EXPECTED: {expected}\n")
                        f.write(f"SIGNATURE: {signature}\n")
                        f.write(f"MATCH: {signature == expected}\n")
                    return False
        
        payload = json.loads(payload_str)
        user = payload.get("user")
        tenant = payload.get("tenant")
        exp_str = payload.get("exp")
        
        frappe.log_error(f"SSO: payload user={user}, tenant={tenant}, exp={exp_str}", "SSO Debug")
        
        if exp_str:
            from frappe.utils import get_datetime
            exp = get_datetime(exp_str)
            if now_datetime() > exp:
                frappe.log_error(f"SSO: Token expired at {exp}", "SSO Debug")
                return False
        
        current_site = frappe.local.site
        frappe.log_error(f"SSO: current_site = {current_site}", "SSO Debug")
        
        tenant_site_record = frappe.db.get_value("Tenant Site", {"domain": current_site}, "name")
        frappe.log_error(f"SSO: tenant_site_record = {tenant_site_record}, tenant from token = {tenant}", "SSO Debug")
        
        if tenant and tenant != tenant_site_record:
            frappe.log_error(f"SSO: Tenant mismatch: {tenant} vs {tenant_site_record}", "SSO Debug")
            return False
        
        frappe.log_error(f"SSO: Logging in user {user}", "SSO Debug")
        frappe.local.login_manager = frappe.auth.LoginManager()
        frappe.local.login_manager.user = user
        frappe.local.login_manager.post_login()
        
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/app"
        
        return True
        
    except Exception as e:
        frappe.log_error(f"SSO: Exception: {str(e)}", "SSO Debug")
        return False

# Keep the original function name for the hook
# validate_sso_token is already defined above