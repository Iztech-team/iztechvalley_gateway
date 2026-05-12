import frappe

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/me"
        raise frappe.Redirect

    from iztechvalley_gateway.api.tenant_picker import get_my_tenant_sites, generate_sso_token

    tenant_sites = get_my_tenant_sites()
    
    user_email = frappe.session.user
    for site in tenant_sites:
        site["sso_token"] = generate_sso_token(user_email, site["name"])

    context.tenant_sites = tenant_sites
    context.user_email = user_email
    context.no_header = 1
    context.show_sidebar = False
    context.title = "Choose a site"