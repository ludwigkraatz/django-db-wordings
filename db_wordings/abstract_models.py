from django.db.models import Model, fields
from django.db.models.fields import related
from django.utils.html import strip_tags, mark_safe

from db_wordings import get_wording_text
from db_wordings.consts import OBJECT_KIND_CHOICES
from db_wordings.interfaces import WordingInterface

__all__ = ['abstractWordingLanguage', 'abstractSiteWording', 'NonDBWording']

class abstractWordingLanguage(Model):
    """
    @brief the languages a instance of this system provides for the users. This Model is not intended to contain every language
    on earth, but just those where any wording is available. this is beeing represented by the complete attr.
    """
    class Meta:
        abstract = True
        
    code            =   fields.TextField(unique=True)
    parent          =   related.ForeignKey('self', related_name='inherited', blank=True, null=True)
    
    def get_parent(self):
        return self.parent
    
    def has_parent(self, ):
        return self.parent is not None
    
    def get_name(self):
        return get_wording_text(self) or self.get_identifier()
    
    def get_identifier(self):
        return self.code

class abstractSiteWording(WordingInterface, Model):
    """
    @brief a Text wording is a text that is specified by an identifier and a language (or None for global usage)
    """
    class Meta:
        abstract = True

   
class NonDBWording(WordingInterface):
    """
    @brief an Empty wording is a WrappedWording without text and a special attribute [is_empty]
    
    It should cache itself on __init__, if there is a object provided, that can generate a cacheIdentifier.
    """
    def __cmp__(self,other):
        if not self.__nonzero__():
            if type(other) == bool:
                return False == other
        else:
            pass
        
    def __nonzero__(self):
        return not self.is_empty()    
    
    def __init__(self, identifier=None, language=None, kind=None, value=None, *args, **kwargs):
        super(NonDBWording,self).__init__(*args, **kwargs)
        self.content = value
        self.identifier = identifier
        self.language = language # TODO parse code/id/...
        self.kind = kind
        self.parse_content = False

    def as_container(self, *args, **kwargs):
        return mark_safe(super(NonDBWording,self).as_container(*args, **kwargs))
    
    def get_container_attrs(self, ):
        return 'data-is-DB="false" data-identifier="%s" data-kind="%s" data-language="%s"' % (
            str(self.identifier),
            str(self.kind),
            str(self.language.id)
        )
    
    def get_text(self, *args, **kwargs):
        return strip_tags(super(NonDBWording,self).get_text(*args, **kwargs))
