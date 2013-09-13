from django.utils.translation import get_language
from db_wordings import get_wording_model, get_language_model

from django.utils.functional import SimpleLazyObject
from django.utils.encoding import python_2_unicode_compatible


__all__ = [
            'get_language_object',
            'get_wordings', 'get_wording', 'get_wording_text',
            'as_wording'
           ]


# all wordings are cached here
_wordings = {}

# handles for wordings, by language are cached here
_seen_site_wordings = {}
_seen_object_wordings = {}

# translates languages Codes into language Objects (ids)
_seen_languages = {}

def get_language_object(language_code=None):
    language = language_code or get_language()
    LanguageModel = get_language_model()
    
    if isinstance(language, LanguageModel):
        return language
    
    global _seen_languages
    
    if language not in _seen_languages:
        _seen_languages[language] = LanguageModel.objects.get(code = language)
        
    return _seen_languages[language]

def get_language_id(language_code=None):
    return get_language_object(language_code).id


def resolve_wording_kwargs(identifier_or_object=False, identifier=False, object_id=False, language=False, kind=False, content_type=False):
    wording_filter = {}
    identifier_hash = None
    object_hash = None
    
    # arg 0 = identifier_or_object
    if identifier_or_object != False:
        if isinstance(identifier_or_object, basestring):
            # is identifier
            identifier = identifier or identifier_or_object
            identifier_hash = 'db_wordings:identifier:' + str(identifier)
            
        elif hasattr(identifier_or_object, 'pk'):
            # is object
            object_id = object_id or identifier_or_object.pk
            # TODO
            #content_type = content_type or identifier_or_object.pk
            #object_hash = 'db_wordings:object:' + content_type + '_' + object_id
            
        else:
            raise TypeError, 'arg[0] is invalid! should be identifier or object'
    
    # kwargs: 
    if object_id != False:
        wording_filter['object_id'] = object_id
    if content_type != False:
        wording_filter['content_type'] = content_type
    
    if identifier != False:
        wording_filter['identifier'] = identifier
    
    if kind != False:# TODO: default is kind==None
        wording_filter['kind'] = kind
    
    if language != False:
        if not isinstance(language, get_language_model()):
            language = get_language_object(language)
        wording_filter['language'] = language
    
    return wording_filter, (identifier or None), object_hash, (kind or None), (language or None)



def as_wording(value=None, *args, **kwargs):
    from db_wordings.abstract_models import NonDBWording
    kwargs['value'] = value
    return NonDBWording(*args, **kwargs)

def get_wordings(*args, **kwargs):
    wording_filter = resolve_wording_kwargs(*args, **kwargs)[0]
        
    return get_wording_model().objects.filter(**wording_filter)

def get_wording(*args, **kwargs):
    return SimpleLazyObject(lambda: get_actual_wording(*args, **kwargs))


def get_actual_wording(*args, **kwargs):
    """
    for current language
    """
    global _seen_site_wordings, _wordings
    WordingModel = get_wording_model()
    skip_cache = True
    
    wording = None    
    wording_filter, identifier, object_hash, kind, language = resolve_wording_kwargs(*args, **kwargs)    
    cache_identifier = identifier or object_hash
    
    # cur_language is a language code (e.g. en-us or de)
    cur_language = language or get_language()
    if cur_language not in _seen_site_wordings:
        _seen_site_wordings[cur_language] = {}
        
    cur_wordings = _seen_site_wordings.get(cur_language)
    
    cur_wording_dict = cur_wordings.get(cache_identifier, False)
    if cur_wording_dict is not False:
        cur_wording_id = cur_wording_dict.get(kind, False)
    
    if  skip_cache \
        or  ( cur_wording_id is False):
        
        wordings = get_wordings(*args, **kwargs)        
        tmp_language = get_language_object(cur_language)
        
        while (tmp_language is not None):
            try:
                wording = wordings.get(language = tmp_language)
                break
            except WordingModel.DoesNotExist:
                # try once more the parent language if there is one
                if tmp_language.has_parent():
                    tmp_language = tmp_language.get_parent()
                    
                else:
                    # TODO:
                    #if kind:
                    # return get_wording() kwargs['kind']=None
                    #else:
                    tmp_language = None
        
        if tmp_language is not None:
            # store the actual Wording content
            wording_id = str(wording.id)
            _wordings[wording_id] = wording
        else:
            # store in cache, that the DB can't return a matching wording
            wording_id = None
        
        # link the wording to the current cache_identifier & kind
        if not cache_identifier in cur_wordings:
            cur_wordings[cache_identifier] = {}
        cur_wordings[cache_identifier][kind] = wording_id
    
    # if there is no DB value for this wording
    if cur_wordings[cache_identifier][kind] is None:
        # return an (Empty) NonDBWording
        kwargs['language'] = get_language_object(cur_language)
        return as_wording(None, *args, **kwargs)
    
    # if wording was fetched from DB, return it
    if wording:
        return wording
    
    # otherwise try to get it from cache
    cur_wording = _wordings.get(cur_wording_id, False)
    if cur_wording is False:
        # if that fails, return it from DB
        return WordingModel.objects.get(id=cur_wording_id)
    
    return cur_wording
    

def get_wording_text(*args, **kwargs):
    """
    for current language
    """
    text_settings = kwargs.pop('text_settings', {})
    return get_wording(*args, **kwargs).get_text(**text_settings)
