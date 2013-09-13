from db_wordings.settings import dbwording_settings
api_root = dbwording_settings.API_ROOT


from db_wordings.api.views import *

if api_root:
    api_root.register_endpoint(       'languages',
        view            =   LanguageList,
        view_name       =   'language-list',
        active          = True
        )
    api_root.register_endpoint(       'wordings',
        view            =   WordingList,
        view_name       =   'sitewording-list',
        active          = True
        ).register_filter(                  'wording__id', '[0-9a-z-]',
        view            =   WordingDetails,
        view_name       =   'sitewording-detail'
        
    )
