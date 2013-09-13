
__all__ = ['setup_translation']

def setup_translation():
    from django.utils import translation    
    from db_wordings.utils.translation import trans_real
        
    translation.trans_real = trans_real