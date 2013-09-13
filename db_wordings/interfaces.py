from django.template import Template, Context
from django.utils.encoding import force_text
from django.utils.html import mark_safe

class WordingInterface(object):
    
    def get_text(self, context=None):
        return force_text(self.get_parsed_content(context=context)) if self.has_content() else ""
    
    def as_container(self, context=None):
        """ this basically is here for compatibility reasons with the django-containerfield app. """
        
        ret = mark_safe('<span class="wording-container" ' + self.get_container_attrs() + '>')
        ret += self.get_text(context=context)
        ret += mark_safe('</span>')
        return ret
    
    def get_container_attrs(self, ):
        return 'data-is-DB=true'
    
    
    def get_parsed_content(self, context=None):
        if self.is_template():
            template = Template(self.get_content())
            
            if isinstance(context, dict):
                context = Context(context)
            elif not isinstance(context, Context):
                if settings.DEBUG:
                    raise Exception
                context = None
                
            return template.render(context)
        return self.get_content()
    
    def get_content(self, *args, **kwargs):
        return self.content
    
    def has_content(self, ):
        return bool(self.content)    
    
    def is_empty(self):
        return False
    
    def is_template(self):
        return self.parse_content
    
    def __str__(self):
        return self.get_text()
    