import frappe
import json

no_cache = 1

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = False
    context.title = "Choose a Site"
    return context