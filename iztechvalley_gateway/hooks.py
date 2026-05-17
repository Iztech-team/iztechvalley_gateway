app_name = "iztechvalley_gateway"
app_title = "Iztechvalley Gateway"
app_publisher = "Iztechvalley"
app_description = "SaaS Front Door layer for multi-site ERPNext"
app_email = "nazeeh.rzeqat@iztechvalley.ps"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "iztechvalley_gateway",
# 		"logo": "/assets/iztechvalley_gateway/logo.png",
# 		"title": "Iztechvalley Gateway",
# 		"route": "/iztechvalley_gateway",
# 		"has_permission": "iztechvalley_gateway.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/iztechvalley_gateway/css/iztechvalley_gateway.css"
# app_include_js = "/assets/iztechvalley_gateway/js/iztechvalley_gateway.js"

# include js, css files in header of web template
# web_include_css = "/assets/iztechvalley_gateway/css/iztechvalley_gateway.css"
# web_include_js = "/assets/iztechvalley_gateway/js/iztechvalley_gateway.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "iztechvalley_gateway/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "iztechvalley_gateway/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "iztechvalley_gateway.utils.jinja_methods",
# 	"filters": "iztechvalley_gateway.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "iztechvalley_gateway.install.before_install"
# after_install = "iztechvalley_gateway.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "iztechvalley_gateway.uninstall.before_uninstall"
# after_uninstall = "iztechvalley_gateway.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "iztechvalley_gateway.utils.before_app_install"
# after_app_install = "iztechvalley_gateway.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "iztechvalley_gateway.utils.before_app_uninstall"
# after_app_uninstall = "iztechvalley_gateway.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "iztechvalley_gateway.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    "User": {
        "after_insert": "iztechvalley_gateway.hooks_backup.user_hooks.after_insert_user",
        "on_update": "iztechvalley_gateway.hooks_backup.user_hooks.on_update_user",
        "before_delete": "iztechvalley_gateway.hooks_backup.user_hooks.before_delete_user",
        "on_trash": "iztechvalley_gateway.hooks_backup.user_hooks.on_trash_user",
        "validate": "iztechvalley_gateway.hooks_backup.user_hooks.validate_user"
    }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"iztechvalley_gateway.tasks.all"
# 	],
# 	"daily": [
# 		"iztechvalley_gateway.tasks.daily"
# 	],
# 	"hourly": [
# 		"iztechvalley_gateway.tasks.hourly"
# 	],
# 	"weekly": [
# 		"iztechvalley_gateway.tasks.weekly"
# 	],
# 	"monthly": [
# 		"iztechvalley_gateway.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "iztechvalley_gateway.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "iztechvalley_gateway.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "iztechvalley_gateway.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["iztechvalley_gateway.utils.before_request"]
# after_request = ["iztechvalley_gateway.utils.after_request"]

# Job Events
# ----------
# before_job = ["iztechvalley_gateway.utils.before_job"]
# after_job = ["iztechvalley_gateway.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"iztechvalley_gateway.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []



# -----------------------------------------------------------------------------
# Front Door: redirect users to /me site picker after login
# Guarded by site name in the function itself.
# -----------------------------------------------------------------------------
on_session_creation = "iztechvalley_gateway.auth.session.on_session_creation"


# Include front_door styles on web pages (notably /me)
web_include_css = "/assets/iztechvalley_gateway/css/front_door.css"

# SSO: Validate token before each request
#before_app_request = "iztechvalley_gateway.auth.sso.validate_sso_token"
csrf_exempted_paths = [
    "api/method/iztechvalley_gateway.api.user_sync.sync_user_from_tenant"
]

system_settings = {
    "allow_guest_to_access_user_api": 1
}