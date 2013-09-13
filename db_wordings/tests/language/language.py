from django.template import Template
from django.test import TestCase
from django.template.loader import render_to_string
from django.utils.html import escape
from django.conf import settings
from django.utils.translation import activate, deactivate_all, get_language


from db_wordings import get_language_model, get_wording_model, get_wording_text

from django.contrib.auth import get_user_model

from django.conf import settings

SiteWording = get_wording_model()
WordingLanguage = get_language_model()

class LanguageTests(TestCase):
    LANGUAGES = ('en', 'en-gb', 'en-us')
    
    def setUp(self):
        
        # create languages from django settings        
        parents = {}
        
        for language in self.LANGUAGES:
            
            parent = None
            if '-' in language:
                language_parent = language.split('-')[0]
                if language_parent in parents:
                    parent = parents[language_parent]
                    
            language_instance = WordingLanguage.objects.create(code=language, parent=parent)
            if '-' not in language:
                parents[language] = language_instance
                
            # create test wordings. content=language.code
            SiteWording.objects.create(language=language_instance, content=language, identifier='test_1')
        
        #self.request   =   page.AttrWrapper(
        #                    user                =   (get_user_model())()
        #                    )
        
        #permissions.PermissionChecker(request   =   self.request)
        
        #self.response   =   page.page.DynamicResponse(request=self.request)
        
        #self.dynamic_context    =   page.context.DynamicContext(request=self.request)
        
    #def check_content(self, kind, name, result, description, silent=False):
    #    t = Template('{%% load page_content %%}{%% dynamic_%s "%s" %%}' % (kind,name))
    #    rendered = t.render(self.dynamic_context).strip()
    #    if not silent:
    #        self.assertEqual(rendered, escape(result),
    #                     msg="dynamic_%s for '%s(%s)' test failed, produced '%s', should've produced '%s'" %
    #                     (kind,name,description, rendered, result))
    #    return rendered == escape(result)

    def test_settings(self):
        """ @brief tests whether settings allow language sensitivity """
        
        self.assertTrue(settings.USE_I18N, msg="setting USE_I18N must be True to have languages working")

    def test_language_fix(self):
        """ @brief tests whether the translation fix works properly """
        #TODO
        
        for lang in self.LANGUAGES:
            activate(lang)
            
            self.assertEqual(lang, get_language())
        

    def test_language_sensitivity(self):
        """ @brief tests whether the db selection is done language sensitive """                
        
        for lang in self.LANGUAGES:
            activate(lang)
            
            self.assertEqual(get_wording_text('test_1'), lang)
        

    def test_language_parent_fallback(self):
        """ @brief tests whether the db selection is done language sensitive """                
        SiteWording.objects.filter(identifier='test_1', language__code='en-us').delete()
        
        activate('en-us')
        self.assertEqual(get_wording_text('test_1'), 'en')
        
        