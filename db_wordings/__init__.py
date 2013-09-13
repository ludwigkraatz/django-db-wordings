"""
@brief Wordings abstract from an actual laguage specific text/word to an wording object. A specific text depending
on a language is stored in the database. For deployment the wordings are all cached via memcache.

There are customer specific and global Wordings. When using a wording, usuallly a customer specific wording is looked
up first and on failure the global wording is beeing fetched. This way we have both, easy central text management and
high customer possibility where necessary.

Wordings in detail are on the on hand Templates with structural and variable information and on the other real text-wordings.
"""

def get_wording_model():
    from django.conf import settings
    from django.db.models.loading import get_model
    
    return get_model(*getattr(settings, 'DB_WORDINGS__SITE_WORDING_MODEL', 'db_wordings.SiteWording').split('.'))


def get_language_model():
    from django.conf import settings
    from django.db.models.loading import get_model
    
    return get_model(*getattr(settings, 'DB_WORDINGS__LANGUAGE_MODEL', 'db_wordings.WordingLanguage').split('.'))

def get_wording(*args, **kwargs):
    from db_wordings.utils.wordings import get_wording
    
    return get_wording(*args, **kwargs)

def get_wording_text(*args, **kwargs):
    from db_wordings.utils.wordings import get_wording_text
    
    return get_wording_text(*args, **kwargs)
