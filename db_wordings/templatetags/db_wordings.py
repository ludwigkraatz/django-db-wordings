
from django.conf import settings
from django import template
from django.template.defaulttags import register
from django.utils.encoding import force_text
from django.utils.html import mark_safe, escapejs, escape, conditional_escape, strip_tags

# cant use 'db_wordings' - would result in importing this exact same file
from .. import get_wording

def internal_wording(identifier, kind=None):
    
    return get_wording(identifier, kind=kind)
        
def wording_container(context, identifier, *args, **kwargs):
    
    as_var  =   kwargs.get("as",None)
    
    in_js   =   kwargs.get("in_js",False)
    as_attr =   kwargs.get("as_attr",False)
    
    wording_obj =   internal_wording(identifier, kwargs.get('kind', None))
    
    #try:
    #    permission_checker    =   context.get_permission_checker()
    #except AttributeError: # wrong Context: maybe because of djangos 404
    #    permission_checker = None #return ''
    
    if not (in_js or as_attr) and settings.DEBUG: #(permission_checker and permission_checker.permission_for(permissions.DEBUG_CONTAINER)):
        text    =   wording_obj.as_container(context=context)
    else:
        text    =   wording_obj.get_text(context=context)        
        
    
    if kwargs.get("safe",False):
        text    =   mark_safe(text)
    
    if kwargs.get("allow_html",False):
        text    =   escapejs(text)
        
    if kwargs.get("strip_tags",False):
        text    =   strip_tags(text)
    
    #if kwargs.get("escape",not kwargs.get("safe",False)):
    #    text    =   conditional_escape(text)
        
    text =  conditional_escape(text)
    
    if as_var:
        setattr(context, as_var, text)
        return ""
    
    return text
        
def site_wording(context, identifier, *args, **kwargs):
    kwargs.update({"safe":True})    
    return wording_container(context, identifier, *args, **kwargs)

def object_wording(context, identifier, *args, **kwargs):
    kwargs.update({"safe":False})
    return wording_container(context, identifier, *args, **kwargs)
    
@register.simple_tag(takes_context=True)
def objectwording(context, identifier, *args, **kwargs):
    return object_wording(context, identifier, *args, **kwargs)

@register.simple_tag(takes_context=True)
def sitewording(context, identifier, *args, **kwargs):
    return site_wording(context, identifier, *args, **kwargs)

@register.simple_tag(takes_context=True)
def sitewording_attr(context, identifier, *args, **kwargs):
    return site_wording(context, identifier, as_attr=True, *args, **kwargs)

@register.simple_tag(takes_context=True)
def sitewording_js(context, identifier, *args, **kwargs):
    return site_wording(context, identifier, in_js=True, *args, **kwargs)
    
@register.simple_tag(takes_context=True)
def wording(context,identifier,*args,**kwargs):
    return wording_container(context, identifier, *args, **kwargs)

@register.simple_tag(takes_context=True)
def wording_attr(context, identifier, *args, **kwargs):
    return wording_container(context, identifier, as_attr=True, *args, **kwargs)

@register.simple_tag(takes_context=True)
def wording_js(context, identifier, *args, **kwargs):
    return wording_container(context, identifier, in_js=True, *args, **kwargs)

class WordingContainerNode(template.Node):
    # TODO: all wordings within this node should be listed in this container (for debug/editing purposes)
    def render(self, context):
        return ''

@register.tag('wordingcontainer')
def wordingContainer(parser, token):
    node = parser.parse(('endwordingcontainer', ))
    parser.delete_first_token()
    return WordingContainerNode()
