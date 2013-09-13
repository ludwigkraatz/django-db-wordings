
from django.db import models
from django.utils.functional import Promise

from .consts import *

class EmptyWording(object):
    """@brief Empty Wording class"""

    #def __init__(self,**kwargs):
        #new_uuid = uuid.uuid4()
        #self.pk=hmac.new(str(new_uuid), digestmod=sha1).hexdigest()
        #self.content_type=kwargs.get("content_type")
        #self.identifier=
        #self.language=0

    def getDatabaseStorage(self):
        return "new"
    @property
    def label(self):
        if settings.DEBUG_WORDING:
            return "_missing_"
        else:
            return ""
        return "EMPTY"
    @property
    def identifier(self):
        return ""
    def get_text(self,not_safe=False,editable=False,visible=True):
        text = self.label
        if editable and False:
            text = "<span class=\"wording\" pk="+str(self.pk)+" storage="+self.getDatabaseStorage()+" content_type="+str(self.content_type.pk if self.content_type else 0)+" identifier=\""+(self.identifier or "")+"\" language="+str(self.language.pk if self.language else 0)+" languages='0' languages_cnt=0>"+text+"</span><script>$(function(){$WordingEditor.add($(\"[pk="+str(self.pk)+"]\"));});</script>"
        return text
    def get_label(self):
        return self.get_text()
    def is_empty(self):
        return True
    def productive_label(self):
        if settings.DEBUG:
            return "_missing_"
        else:
            return ""


class WordingClass(models.Model):
    """@brief Class containing wordings in different languages"""
    class Meta:
        abstract=True
    def __unicode__(self):
        return unicode(self.__repr__())
    def createWording(self,string,object_field="name"):
        """@brief creates a wording
        @param string the wording value
        @param object_filed the name of the wording
        """
        self._wordingClass.objects.get_or_create(label=string,object_id=self.id,object_field=object_field,content_type=ContentType.objects.get_for_model(self.__class__))
        return
    def __repr__(self):
        return str(self.id)
    def names(self):
        return self._fields("name")
    def labels(self):
        return self._fields("label")
    def types(self):
        return self._fields("type")
    def branchen(self):
        return self._fields("branche")
    def descriptions(self):
        return self._fields("description")
    def _fields(self,fieldname):
        """@brief ???
        @param fieldname ?
        """
        return self._wordingClass.objects.filter(content_type=ContentType.objects.get_for_model(self.__class__),object_id=self.id,object_field=fieldname)
    def _get_field(self,fieldname,**kwargs):
        """@brief get the fieldname of a wording field
        @param fieldname .
        """
        return self.get_wording(self._fields(fieldname),**kwargs)
    def display_label(self,**kwargs):
        return self.display_name(**kwargs)
    def display_name(self,**kwargs):
        return self.get_wording(self.names(),**kwargs)
    def display_branche(self,**kwargs):
        return self.get_wording(self.branchen(),**kwargs)
    def display_type(self,**kwargs):
        return self.get_wording(self.type(),**kwargs)
    def display_description(self,**kwargs):
        return self.get_wording(self.descriptions(),**kwargs)
    def getFirstWordingMatch(self,*args,**kwargs):
        kwargs.update({
                    'content_type':ContentType.objects.get_for_model(self.__class__),
                    'object_id':self.id
        })

        return self._wordingClass.objects.getFirstMatch(*args,**kwargs)
    def get_wording(self,wording,*args,**kwargs):
        language_id=1
        if 'request' in kwargs and kwargs['request']:
            language_id=kwargs['request'].session.get('language_id', language_id)
        elif 'user' in kwargs:
            language_id=language_id
        wording_=wording.filter(language__id=language_id)
        if wording_.count()<1:
            wording_=wording
        return escape(wording_[0].label) if wording_.count()>0 else EmptyWording().label
    def __repr__(self):
        return self.display_label()
    def __unicode__(self):
        return self.display_label()
    def get_contentType(self):
        return ContentType.objects.get_for_model(self.__class__)



class WordingAbstract(models.Model,Promise):
    class Meta:
        abstract=True
        unique_together = (("object_id", "content_type", "language", "object_field", "identifier"),)

    object_id = models.PositiveIntegerField(null=True,blank=True)
    object_field = models.CharField(max_length=25,null=True,blank=True,choices=OBJECTS_FIELD_CHOICES)
    label=models.TextField(null=True,blank=True)
    identifier=models.TextField(null=True,blank=True)
    #position = models.TextField(null=True,blank=True,choices=WORDING_POSITION_CHOICES)
    language=models.ForeignKey("Language",null=True,blank=True,related_name="%(app_label)s_%(class)s_related")
    content_type = models.ForeignKey(ContentType, null=True, blank=True,related_name="%(app_label)s_%(class)s_related")

    __startingClass    =   None
    post_str=""

    object = generic.GenericForeignKey('content_type', 'object_id')
    def __add__(self,other):
        if type(other)==str or type(other)==unicode:
            self.post_str+=other
        return self
    def getDatabaseStorage(self):
        return self._meta.db_schema
    def __unicode__(self):
        return u'"'+escape(self.label)+u'" in '+(self.language.__unicode__() if self.language else "[NO LANGUAGE]")+((u' of '+escape(self.content_type.name)) if self.content_type else "")
    def get_label(self):
        return self.get_text()
    @staticmethod
    def shortenIdentifier(identifier):
        """@brief returns the identifier shortened at the first pipe
        @param identifier The Identifier to shorten
        @return the shortened identifier
        """
        index=identifier.rfind("|")
        return identifier[0:index]
    def productive_label(self):
        return self.label
    def setStartingClass(self,startingClass):
        self.__startingClass=startingClass
        return self
    def getStartingClass(self):
        return self.__startingClass or self.__class__
    def get_text(self,not_safe=False,editable=False,visible=True):
        pre=""
        post=""
        text = escape(self.label) if not_safe else self.label
        if editable:
            text = "<span "+("" if visible else "style=\"display:none;\"")+" class=\"wording\" pk="+str(self.pk)+" storage=\""+self.getDatabaseStorage()+"\" content_type="+str(self.content_type.pk if self.content_type else 0)+" identifier=\""+(self.identifier or "")+"\" language="+str(self.language.pk if self.language else 0)+" languages=\""+",".join([str(x) if x else "0" for x in self.getUsedLanguages()])+"\" languages_cnt="+str(len(self.getUsedLanguages()))+">"+text+"</span><script>$(function(){$WordingEditor.add($(\"[pk="+str(self.pk)+"]\"));});</script>"
        if self.position=="pre":
            post=self.getStartingClass().objects.getFirstMatch(language=self.language,identifier=self.__class__.shortenIdentifier(self.identifier),cached=not editable).get_text(not_safe,editable)
            if self.label[-1] not in [" ","-","(","'",'"',"*","<",">"]:
                post=unicode(str(post)[0].lower()+str(post)[1:])
        if self.position=="post":
            pre=self.getStartingClass().objects.getFirstMatch(language=self.language,identifier=self.__class__.shortenIdentifier(self.identifier),cached=not editable).get_text(not_safe,editable)
        return mark_safe(pre+text+post+self.post_str)
    def get_contentType(self):
        return ContentType.objects.get_for_model(self.__class__)
    def getForLanguage(self,language):
        if self.__class__.objects.filter(content_type=self.content_type,object_field=self.object_field,identifier=self.identifier,object_id=self.object_id,language=language).count():
            return self.__class__.objects.filter(content_type=self.content_type,identifier=self.identifier,object_id=self.object_id,language=language)[0]
        else:
            return self.__class__(
                            content_type=self.content_type,
                            identifier=self.identifier,
                            object_id=self.object_id,
                            object_field=self.object_field,
                            language=language,
                            position=self.position)
    def getDifferentLanguages(self):
        return self.__class__.objects.filter(content_type=self.content_type,identifier=self.identifier,object_field=self.object_field,object_id=self.object_id)
    def getUsedLanguages(self):
        return self.getDifferentLanguages().values_list("language",flat=True).distinct()
    def get_possibleLanguages(self):
        return self.__class__.language.field.rel.to.objects.all()
    def doUpdate(self, **kwargs):
        object_id=kwargs.get('object_id',None)
        try:
            if object_id:
                self.object_id=object_id
                self.save()
        except:
            raise LogException( subject=smart_unicode(u'Wording konnte nicht aktualisiert werden: "%s"' % force_text(kwargs)),
                                            generics=[ ("T",self,force_text(self))])
        return False
    def is_empty(self):
        return False


class WordingWrapper(WordingClass,WordingAbstract):
    class Meta:
        abstract=True
    def __init__(self,text,identifier=None,language_info=None,object_field=None,safe=False):
        self.text=text
        self.identifier=identifier
        self.language_info=language_info
        self.safe=safe
        super(WordingWrapper,self).__init__()
    def getFirstWordingMatch(self,*args,**kwargs):
        return self
    def get_text(self,not_safe=False,editable=False,visible=True):
        return mark_safe(self.text) if self.safe and not not_safe else conditional_escape(self.text)
    def is_empty(self):
        return False
    def display_label(self,*args,**kwargs):
        return self.get_text() or ""
    def save(self):
        raise Exception("Wrapper cannot beeing saved")
    def has_content(self):
        return bool(self.text)


class WordingManager(models.Manager):

    __cache =   get_cache("wording")#{}

    def getTextFromSecondaryCache(self,identifier,object_field):
        key =   ":".join([self.model._meta.db_schema,"None",str(identifier),str(object_field)])
        cached=self.__cache.get(key)
        return cached
        # old
        if not 0 in self.__cache[self.model]:
            return None
        if not object_field in self.__cache[self.model][0]:
            return None
        if not identifier in self.__cache[self.model][0][object_field]:
            return None
        cached  = self.__cache[self.model][0][object_field][identifier]
        return WordingWrapper(cached,identifier=identifier,object_field=object_field,safe=True) if cached != None else EmptyWording()
    def getTextFromCache(self,identifier,object_field,language_info):
        try:
            key =   ":".join([self.model._meta.db_schema,str(language_info),str(identifier),str(object_field)])
            cached=self.__cache.get(key) or self.getTextFromSecondaryCache(identifier,object_field)
            return WordingWrapper(cached,identifier=identifier,language_info=language_info,object_field=object_field,safe=True) \
                                if cached != None else None#EmptyWording()
            ## old
            if not self.model in self.__cache:
                return None
            if not language_info in self.__cache[self.model]:
                return self.getTextFromSecondaryCache(identifier,object_field)
            if not object_field in self.__cache[self.model][language_info]:
                return self.getTextFromSecondaryCache(identifier,object_field)
            if not identifier in self.__cache[self.model][language_info][object_field]:
                return self.getTextFromSecondaryCache(identifier,object_field)
            cached  = self.__cache[self.model][language_info][object_field][identifier]
            return WordingWrapper(cached,identifier=identifier,language_info=language_info,object_field=object_field,safe=True) \
                            if cached != None else EmptyWording()
        except:
            return EmptyWording()
    def writeTextInCache(self,identifier,object_field,language_info,wording):
        if not wording:
            return
        key =   ":".join([self.model._meta.db_schema,str(language_info),str(identifier),str(object_field)])
        cached=self.__cache.set(key,wording.get_text())
        return
        #old
        if not self.model in self.__cache:
            self.__cache[self.model] =   {}
        if not language_info in self.__cache[self.model]:
            self.__cache[self.model][language_info] =   {}
        if not object_field in self.__cache[self.model][language_info]:
            self.__cache[self.model][language_info][object_field] =   {}
        self.__cache[self.model][language_info][object_field][identifier] =   wording.get_text() if wording else None
    def getFirstMatch(self,*args,**kwargs):
        language_info=kwargs.pop("language_info",None)
        language=kwargs.pop("language",None)
        do_cached=kwargs.pop("cached",True)
        request=kwargs.pop("request",None)
        user=kwargs.pop("user",None)
        languages=kwargs.get("language__in",[])
        object_field=kwargs.get("object_field",None)
        if type(languages)!=list:
            languages=[languages]
        if languages==[]:
            try:
                if language_info and type(language_info) == list:
                    #languages=[2]
                    languages=[x.pk for x in self.model.language.field.rel.to.objects.filter(code__in=language_info)]
                    #if language_info == ["en"]:
                    #    raise Exception()
                elif request and hasattr(request,"user"):
                    #languages=[2]
                    languages=[x.pk for x in self.model.language.field.rel.to.objects.filter(code__in=request.user.getLanguageCodes())]
                    #if language_info == ["en"]:
                    #    raise Exception()
                elif user and hasattr(user,"getLanguageCodes"):
                    #languages=[2]
                    languages=[x.pk for x in self.model.language.field.rel.to.objects.filter(code__in=user.getLanguageCodes())]
                    #if language_info == ["en"]:
                    #    raise Exception()
                else:
                    #return WordingWrapper("_"+str(language_info))
                    languages=[1]
                #if not (request and request.user.is_staff()):
                #    languages=[1]
                #else:
                #    languages=[2]
            except:
                languages=[1]
        for language in languages:
            if "identifier" in kwargs and do_cached:
                cached =    self.getTextFromCache(kwargs["identifier"],object_field,language)
                if cached:
                    return cached
            query=self.filter(language__pk=language,*args,**kwargs)# if isinstance(language,basestring) else language.code)
            if query.count():
                if "identifier" in kwargs and do_cached:
                    self.writeTextInCache(kwargs["identifier"],object_field,language,query[0])
                return query[0]
            elif hasattr(self.model,"_parentWordingClass"):
                result=self.model._parentWordingClass.objects.getFirstMatch(*args,**kwargs)
                if issubclass(result.__class__,WordingAbstract):# or issubclass(result.__class__,WordingWrapper):
                    result=result.setStartingClass(self.model)
                    if "identifier" in kwargs and do_cached:
                        self.writeTextInCache(kwargs["identifier"],object_field,language,result)
                    return result

        if "identifier" in kwargs and do_cached:
            cached =    self.getTextFromCache(kwargs["identifier"],object_field,None)
            if cached:
                return cached
        query=self.filter(*args,**kwargs)# if isinstance(language,basestring) else language.code)
        if query.count():
            if "identifier" in kwargs and do_cached:
                self.writeTextInCache(kwargs["identifier"],object_field,None,query[0])
            return query[0]
        else:
            if "identifier" in kwargs and "|" in kwargs["identifier"]:
                kwargs2=kwargs.copy()
                kwargs2["identifier"]=self.model.shortenIdentifier(kwargs["identifier"])
                kwargs3=kwargs.copy()
                kwargs3["cached"]    =   do_cached
                if do_cached:
                    cached =    self.getTextFromCache(kwargs2["identifier"],object_field,None)
                    if cached:
                        return cached
                match= self.getFirstMatch(*args,**kwargs2)
                if  do_cached:
                    if not match.is_empty():
                        self.writeTextInCache(kwargs2["identifier"],object_field,None,match)
                    else:
                        self.writeTextInCache(kwargs2["identifier"],object_field,None,None)
                return match
            if "identifier" in kwargs and do_cached:
                self.writeTextInCache(kwargs["identifier"],object_field,None,None)
            return EmptyWording()
    def get_languages(self,**kwargs):
        x=self.filter(content_type=ContentType.objects.get_for_model(self.model.language.field.rel.to),object_id__isnull=False)
        if "request" in kwargs:
            if kwargs.get("request").user.profile().languages.all()[:1]:
                lang=kwargs.get("request").user.profile().languages.all().order_by("id")[0]
            x.filter(language=lang)
        if "language" in kwargs:
            x.filter(language=kwargs.get("language"))
        if "order_by" in kwargs:
            x.order_by(kwargs.get("order_by"))
        return x#,[x.object for x in x]

    def get_or_create(self,dict=None, **kwargs):
        if not dict:
            return super(WordingManager,self).get_or_create(**kwargs)
        if 'request' in kwargs:
            request=kwargs.pop('request')
        y=self.do_exist(dict,**kwargs)
        if y:
            return y
        return self.do_new(dict,doReturn=True,**kwargs)
    def do_exist(self,dict,**kwargs):
        postfix="__iexact"
        if "postfix" in kwargs:
            postfix=kwargs.pop('postfix')
        if isinstance(dict,self.model):
            return dict
        erlaubt=[    'label','label__in','label__iexact','label__exact','label__isnull','label__icontains','label__contains',
                    'content_type','content_type__isnull',
                    'object_field','object_field__isnull',
                    'language','language__in','language__isnull',
                    'object_id__isnull',
                    'model',
                    'object']

        try:
            if set(kwargs.keys()) - set(erlaubt) != set([]):
                diff=list(set(kwargs.keys()) - set(erlaubt))
                LogException(subject=smart_unicode(u"Unerlaubte Keys bei Exist-Ueberpruefung auf %s in kwargs: '%s'"  % (force_text(self.model),force_text(diff)) ))
                for unerlaubt in diff:
                    dictDel=kwargs.pop(unerlaubt)

            lookup={}

            if isinstance(dict,self.model):
                return dict
            elif dict:
                if type(dict)==type([]):
                    for x in dict:
                        if x:
                            y=self.do_exist(x,**kwargs)
                            if y:
                                return y
                else:
                    if type(dict)!=type({}):
                        dict={'label'+postfix:dict}
                    if set(dict.keys()) - set(erlaubt) != set([]):
                        diff=list(set(dict.keys()) - set(erlaubt))
                        LogException(subject=smart_unicode(u"Unerlaubte Keys bei Exist-Ueberpruefung auf %s im dict: '%s'"  % (force_text(self.model),force_text(diff)) ))
                        for unerlaubt in diff:
                            dictDel=dict.pop(unerlaubt)
                    lookup.update(dict)
                    lookup.update(kwargs)
                    model=          lookup.pop('model',None)
                    object=         lookup.pop('object',None)
                    language=       lookup.pop('language__in',lookup.pop('language',None))
                    if language:
                        if type(language)==type([]):
                            tLangs=[]
                            for lang in language:
                                tLang=Language.objects.do_exist(lang)
                                if tLang:
                                    tLangs.append(tLang)
                            if not tLangs:
                                return False
                            lookup.update({'language__in':tLangs})
                        else:
                            tLang=Language.objects.do_exist(language)
                        if tLang:   #use language__in if u want ONE language to fit, too
                            lookup.update({'language':tLang})
                        else:
                            lookup.update({'language__isnull':True})
                    if model:
                        content_type=ContentType.objects.get_for_model(model)
                        lookup.update({'content_type':content_type})
                    if object:
                        content_type=ContentType.objects.get_for_model(object)
                        object_id=object.pk
                        lookup.update({ 'content_type':content_type,
                                        'object_id':object_id})
                    y= self.model.objects.filter(**lookup)[:1]
                    return y[0] if y else None
            return False
        except:
            raise LogException(subject=smart_unicode(u"Fehler bei Exist-Ueberpruefung auf %s:Dict '%s',kwargs '%s'"  % (force_text(self.model),force_text(dict),force_text(kwargs) ) ))
    def do_new(self,dict, **kwargs):
        if dict==None:
            return None
        if type(dict)==type({}):
            dict=dict.copy()

        doReturn=kwargs.get('doReturn',None)
        if type(dict)==type({}):
            if not 'label' in dict:
                raise LogException(subject=smart_unicode(u'Label wurde nicht uebergeben: "%s"' % force_text(dict)))
        else:
            if not dict:
                raise LogException(subject=smart_unicode(u'Label wurde nicht uebergeben: "%s"' % force_text(dict)))
            dict={'label':dict}

        object_field=kwargs.get('object_field',dict.get('object_field',None))
        model=kwargs.get('model',dict.get('model',None))
        content_type=kwargs.get('content_type',dict.get('content_type',None))
        object_id=kwargs.get('object_id',dict.get('object_id',None))

        do_language=None
        done_wording=None
        other_Exceptions=[]

        try:
            if content_type:
                if not isinstance(content_type,ContentType):
                    raise LogException(subject=smart_unicode(u"Content_type muss auch eine Instanz der Klasse ContentType sein!"),
                                                generics=[ ("S",None,u"Content_Type:  '%s'" % force_text(content_type))])
            elif model:
                try:
                    content_type=ContentType.objects.get_for_model(model)
                except:
                    raise LogException(subject=smart_unicode(u"Zum Model konnte kein Content_Type ermittelt werden!"),
                                                generics=[ ("S",None,smart_unicode(u"Model:  '%s'") % force_text(model))])

            if 'language' in dict:
                do_language=Language.objects.do_exist(dict['language'])
                if not do_language:
                    try:
                        do_language=Language.objects.get_or_create(dict['language'])
                    except LogException as log:
                        raise LogException( subject=smart_unicode(u'Language konnte nicht erstellt werden!'),
                                            generics=[ ("T",None,smart_unicode(u"Language:  '%s'") % force_text(dict['language']))],
                                            otherExceptions=[log])
                    except:
                        raise LogException( subject=smart_unicode(u'Language konnte nicht erstellt werden!'),
                                            generics=[ ("T",None,smart_unicode(u"Language:  '%s'") % force_text(dict['language']))])
        except LogException as log:
            other_Exceptions.append(log)
        except:
            other_Exceptions.append(LogException(subject=smart_unicode(u'Wording konnte nicht vollstaendig erstellt werden!')))
        try:
            done_wording=self.model(id=None,object_id=object_id,object_field=object_field,label=dict['label'],language=do_language if do_language else None,content_type=content_type if content_type else None)
            done_wording.save()
        except:
            raise LogException(subject=smart_unicode(u'Wording konnte nicht erstellt werden!'),otherExceptions=other_Exceptions)
        if other_Exceptions:
            raise other_Exceptions[0] if len(other_Exceptions)==1 else LogException(subject=smart_unicode(u'Exceptionwrapper'),otherExceptions=other_Exceptions)
        if doReturn:
            return done_wording