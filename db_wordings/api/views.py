import json as simplejson

from django.utils.functional import SimpleLazyObject
from django import template
from django import shortcuts

from introspective_api import generics
from introspective_api.response import ApiResponse

from db_wordings.api import serializers
from db_wordings import get_language_model, get_wording_model
from db_wordings.settings import dbwording_settings

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import filters

    
class LanguageList(generics.ListAPIView):
    """
    API endpoint that represents a list of entities.
    """

    model = get_language_model()
    serializer_class = serializers.LanguageSerializer
    
class WordingList(generics.ListAPIView):
    """
    API endpoint that represents a list of entities.
    """

    model = get_wording_model()
    serializer_class = serializers.WordingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('identifier',)
    
class WordingDetails(generics.RetrieveUpdateAPIView):
    """
    API endpoint that represents a list of entities.
    """

    model = get_wording_model()
    serializer_class = serializers.WordingSerializer
    
    lookup_field = 'id'