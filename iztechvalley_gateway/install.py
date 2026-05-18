import frappe

def after_install():
    """Create all required DocTypes for SSO"""
    
    # 1. Tenant Site
    if not frappe.db.exists("DocType", "Tenant Site"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Tenant Site",
            "module": "Tenant Management",
            "fields": [
                {"fieldname": "site_name", "label": "Site Name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "domain", "label": "Domain", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "is_active", "label": "Is Active", "fieldtype": "Check", "default": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}],
            "autoname": "field:site_name"
        })
        doc.insert()
        frappe.db.commit()
        print("Tenant Site DocType created")
    else:
        print("Tenant Site DocType already exists")
    
    # 2. User Tenant Access
    if not frappe.db.exists("DocType", "User Tenant Access"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "User Tenant Access",
            "module": "Tenant Management",
            "fields": [
                {"fieldname": "user", "label": "User", "fieldtype": "Link", "options": "User", "reqd": 1},
                {"fieldname": "tenant_site", "label": "Tenant Site", "fieldtype": "Link", "options": "Tenant Site", "reqd": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}],
            "autoname": "hash"
        })
        doc.insert()
        frappe.db.commit()
        print("User Tenant Access DocType created")
    else:
        print("User Tenant Access DocType already exists")
    
    # 3. SSO Token
    if not frappe.db.exists("DocType", "SSO Token"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "SSO Token",
            "module": "Tenant Management",
            "fields": [
                {"fieldname": "token", "label": "Token", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"fieldname": "user", "label": "User", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "allowed_sites", "label": "Allowed Sites", "fieldtype": "Text"},
                {"fieldname": "expires_at", "label": "Expires At", "fieldtype": "Datetime", "reqd": 1},
                {"fieldname": "used", "label": "Used", "fieldtype": "Check", "default": 0}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}],
            "autoname": "field:token"
        })
        doc.insert()
        frappe.db.commit()
        print("SSO Token DocType created")
    else:
        print("SSO Token DocType already exists")
    
    print("All DocTypes created successfully!")