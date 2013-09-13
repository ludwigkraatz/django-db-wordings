"""
@brief the Wordingmanagers to fetch db stored Wordings
"""
from django.db.models import Manager
from django.db.models.query import QuerySet

from db_wordings.utils.wordings import get_language_object
from db_wordings.abstract_models import NonDBWording

class WordingQuerySet(QuerySet):
    def as_container(self,*args, **kwargs): #TODO
        try:
             return self.get(*args, **kwargs).as_container()
             return NonDBWording(self.get(*args,**kwargs).__dict__).as_container()
        except self.model.DoesNotExist:
            return NonDBWording().as_container()
        
    def get_text(self, *args, **kwargs): #TODO: context
        try:
            return self.get(*args,**kwargs).get_text()
        except self.model.DoesNotExist:
            return NonDBWording().get_text()
    """        
    #TODO use not???
    def _filter_or_exclude(self,*args,**kwargs):
        new_kwargs  =   self.clean_identifier_for_db(kwargs)        
        return super(WordingQuerySet,self)._filter_or_exclude(*args,**new_kwargs)
  
    def clean_identifier_for_db(self,kwargs):
        new_kwargs  =   {}
        for key,value in kwargs.iteritems():
            if key.startswith("identifier"):
                value.replace(self.model.get_class_namespace(),"")
            new_kwargs[key] =   value
        return new_kwargs
    """    
    def filter_for_current_language(self):
        try:
            return self.filter(language = get_language_object())
        except self.model.DoesNotExist:
            return NonDBWording() #TODO set kwargs
    
    def get_for_current_language(self, language=None, orig_language=None):
        language = get_language_object(language)
        orig_language = orig_language or language
        
        try:
            return self.get(language = language)
        except self.model.DoesNotExist:
            if language.has_parent():
                return self.get_for_current_language(language.get_parent(), orig_language=orig_language)
            else:
                return NonDBWording(language = orig_language) #TODO set kwargs

class WordingManager(Manager):
    use_for_related_fields = True
    def get_query_set(self):
        return WordingQuerySet(self.model)