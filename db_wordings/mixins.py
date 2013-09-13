from db_wordings import get_wording
from db_wordings import get_language_model, get_wording_model

class SensitiveDataModel(object):
    pass

class UsesWordingMixin(object):
    """
    @brief this is an Mixin defining the behaviour for using Wordings
    """
    
    def update_wording(self, label, *args, **kwargs):
        if self.current_language_label != label:
            return self.create_wording(label, *args, **kwargs)
    
    def create_wording(self, label, language=None, sensitive=None):
        if not label:
            return #TODO: best to be sure of non empty wordings?
        
        #TODO
        sensitive = sensitive if sensitive != None else issubclass(self.__class__, SensitiveDataModel)
        
        if not language:
            # import here, not on top of file
            from django.utils.translation import get_language
            language    =   get_language()
        else:
            WordingModel = get_language_model()
            if not isinstance(language, WordingModel):
                language    =   language = WordingModel.objects.get(code = language.lower())
        
        
        assert kwargs.get("identifier"), "identifier needed, to create a wording"
        if kwargs.pop("sensitive",False):
            Model = SensitiveObjectWording
        else:
            Model = ObjectWording
        
        # What if Creating Object fails, is wording rolled back as well??
        # TODO
        return Model.objects.create(
                                identifier      =   self.get_identifier(),# right method?
                                class_id      =   self._class_id,
                                language        =   language,
                                text            =   label,
                                sensitive       =   sensitive
                              )
    
    def create_sensitive_wording(self,*args,**kwargs):
        kwargs["sensitive"] =   True
        return self.create_wording(*args,**kwargs)
    
    def create_public_wording(self,*args,**kwargs):
        kwargs["sensitive"] =   False
        return self.create_wording(*args,**kwargs)
    
    def get_text(self, **kwargs):
        return get_wording(self, **kwargs)
    
    @property
    def current_language_label(self):
        return self.get_text() or None
    
    @current_language_label.setter
    def current_language_label(self, value):
        self.update_wording(value)
    
    @property
    def wordings(self):
        return get_wordings(self)
    
    def __unicode__(self, ):
        return unicode(self.current_language_label or '')
    def __str__(self, ):
        return str(self.current_language_label or '')