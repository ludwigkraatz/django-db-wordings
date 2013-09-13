
from django.template import Template
from django.test import TestCase
from django.utils.html import escape

from django.utils.functional import Promise
from django.utils.encoding import force_text


from django.utils.translation import activate, deactivate_all, get_language

class WordingTests(TestCase):
    
    def setUp(self):
        language_instance = WordingLanguage.objects.create(code=get_language())
                
        # create test wordings. content=language.code
        SiteWording.objects.create(language=language_instance, content=get_language(), identifier='test_1')
    
    def test_get_wording(self):
        from .. import get_wording,get_text
        from .. import EmptyWording
        
        empty   =   get_wording(identifier=EXPN__SITE_WORDING__NAMESPACE+"_nothing_there_")
        self.assertIsInstance(
            empty,Promise,
            msg="request of wording should return a Promise Instance, returned '%s'" % str(empty))
        
        # determine class by is_empty func of Wording, because get_wording is a lazy func and just returns a proxy,
        # never a (Empty)Wording
        is_empty    =   empty.is_empty()
        text    =   empty.get_text()
        
        self.assertTrue(
            is_empty,
            msg="request of not existing wording should be empty, returned '%s'" % str(is_empty))
        self.assertEqual(
            text,u"",
            msg="request of not existing wording should result in u'', returned '%s'" % str(text))
        
        text   =   force_text(get_text(identifier=EXPN__SITE_WORDING__NAMESPACE+'_nothing_there_'))
        self.assertEqual(
            text,u"",
            msg="request of not existing wording should result in u'', returned '%s'" % str(text))
   