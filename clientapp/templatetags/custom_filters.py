from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value for a given key in a dictionary."""
    return dictionary.get(key, None)
from django import template


def dictlookup(dictionary, key):
    """Returns the value for a given key in a dictionary."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

