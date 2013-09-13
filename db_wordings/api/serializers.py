from introspective_api import serializers
from db_wordings import get_language_model, get_wording_model

class LanguageSerializer(serializers.ModelSerializer):#Hyperlinked
    _options_class = serializers.HyperlinkedModelSerializerOptions
    #url             =   serializers.HyperlinkedIdentityField(view_name="widget-detail", slug_field="pk")
    
    class Meta:
        #fields      =   ('id', 'endpoint_name', 'identifier', 'public')
        model       =   get_language_model()
    
class WordingSerializer(serializers.HyperlinkedModelSerializer):#Hyperlinked
    _options_class = serializers.HyperlinkedModelSerializerOptions
    #url             =   serializers.HyperlinkedIdentityField(view_name="widget-detail", slug_field="pk")
    
    class Meta:
        #fields      =   ('id', 'endpoint_name', 'identifier', 'public')
        model       =   get_wording_model()
        lookup_field = 'id'
    