import frappe
from frappe.model.document import Document


class UserTenantAccess(Document):
	def validate(self):
		existing = frappe.db.exists(
			"User Tenant Access",
			{
				"user": self.user,
				"tenant_site": self.tenant_site,
				"name": ("!=", self.name or ""),
			},
		)
		if existing:
			frappe.throw(f"User {self.user} already has access to {self.tenant_site}")
