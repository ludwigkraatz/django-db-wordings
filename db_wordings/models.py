from django.db.models import fields, permalink
from django.db.models.fields import related
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

#from db_wordings.settings import dbwording_settings
from django.conf import settings
from db_wordings.abstract_models import abstractSiteWording, abstractWordingLanguage
from db_wordings.managers import WordingManager
from db_wordings.consts import OBJECT_KIND_CHOICES


__all__ = ['WordingLanguage', 'SiteWording']

class WordingLanguage(abstractWordingLanguage):
    class Meta(abstractWordingLanguage.Meta):
        swappable = 'DB_WORDINGS__LANGUAGE_MODEL'
        
    objects =   WordingManager()
    

class SiteWording(abstractSiteWording):
    class Meta(abstractSiteWording.Meta):
        swappable = 'DB_WORDINGS__SITE_WORDING_MODEL'
        unique_together = ( ('language', 'identifier', 'kind'),
                            ('language', 'object_id', 'content_type', 'kind'), )
        
    
    kind            =   fields.TextField(null=True, blank=True, choices=OBJECT_KIND_CHOICES)
    language        =   related.ForeignKey(getattr(settings, 'DB_WORDINGS__LANGUAGE_MODEL', WordingLanguage), related_name='site_wordings')
    content         =   fields.TextField(null=True, blank=True)
    parse_content   =   fields.BooleanField(default=False)
    
    # this is used for direct access to an wording. e.g. landing_page:headline
    # usually wordings with identifier are handled to be more safe, because its unlikely
    # that they contain user inserted data. see is_content_safe() method
    identifier      =   fields.TextField(null=True, blank=True)
    
    # when a wording relates to an object, there is no need for an identifier
    object_id       =   fields.IntegerField(null=True, blank=True)
    content_type    =   related.ForeignKey(ContentType, null=True, blank=True)
    object          =   generic.GenericForeignKey('content_type', 'object_id')
        
    objects =   WordingManager()