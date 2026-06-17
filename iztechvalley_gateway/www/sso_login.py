import frappe
import requests

no_cache = 1

def get_context(context):
    # قراءة token من الرابط
    token = frappe.form_dict.get("token")
    
    if not token:
        # لا يوجد token → اذهب إلى login
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect
    
    try:
        # الاتصال بـ Gateway للتحقق من صحة الـ token
        gateway_domain = frappe.get_site_config().get("front_door_domain", "login.iztechvalley.local")
        scheme = frappe.conf.get("gateway_scheme", "https")
        gateway_url = f"{scheme}://{gateway_domain}"
        tenant_site = frappe.local.site
        
        response = requests.post(
            f"{gateway_url}/api/method/iztechvalley_gateway.api.tenant_picker.validate_sso_token",
            data={"token": token, "tenant_site": tenant_site},
            timeout=5,
            headers={"Accept": "application/json"}
        )
        
        if response.status_code != 200:
            raise Exception("فشل التحقق من التوكن")
        
        data = response.json()
        if data.get("message", {}).get("status") != "success":
            raise Exception(data.get("message", {}).get("message", "خطأ غير معروف"))
        
        user_email = data["message"]["user"]
        
        # تسجيل الدخول مباشرة بدون كلمة مرور
        from frappe.auth import LoginManager
        login_manager = LoginManager()
        login_manager.login_as(user_email)
        login_manager.post_login()
        
        # التوجيه إلى الصفحة الرئيسية
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/app"
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"SSO token login failed: {str(e)}", "SSO")
        context.error = True
        context.message = "فشل تسجيل الدخول. الرابط غير صالح أو منتهي الصلاحية."
    
    return context
