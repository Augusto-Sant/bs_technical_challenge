"""
Template tags for cart functionality.
"""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Tag for jinja template to get item from dictionary by key."""
    if dictionary is None:
        return None
    return dictionary.get(key)
