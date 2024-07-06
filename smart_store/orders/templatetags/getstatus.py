from django import template

register= template.Library()
@register.simple_tag (name='getstatus')

def getstatus(status):
   status=status-1  
   status_array=['Order confirmed','Order processed','Order delivered','Order rejected']
   return status_array[status]
