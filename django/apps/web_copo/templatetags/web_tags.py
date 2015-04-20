__author__ = 'fshaw'
from django import template
import jsonpickle
register = template.Library()

@register.filter("mongo_id")
def mongo_id(value):
    # return the $oid field of _id (which is a dict)
    try:
        return str(value['_id']['$oid'])
    except:
        return str(value['_id'])