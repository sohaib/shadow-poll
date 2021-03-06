#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import os
import gettext
from django.utils.translation.trans_real import DjangoTranslation

#RapidSMS Internationalization (i18n)
# 
# Read more about Django i18n: http://docs.djangoproject.com/en/dev/topics/i18n/
# Read more about Python i18n: http://www.python.org/doc/2.5/lib/node733.html
# Read more about RapidSMS i18n: http://docs.rapidsms.org/i18n.html

# path to GNU gettext 'locale' directory
LOCALE_PATH=os.path.join('contrib','locale')

# translation are instantiated globally
_sms_translations = {}
_sms_default = None

# Used to mark sms text that needs to be translated 
from django.utils.translation import ugettext_noop


# ugettext is globally available to make tagging strings easy
def ugettext_from_locale(text, locale=_sms_default):
    """ Used to translate a string given a particulate locale
    
    For example, most modules will import these functions:
        from rapidsms.i18n import ugettext_from_locale as _t
        from rapidsms.i18n import ugettext_noop as _
    '_' will wrap strings that need to be translated for text messages
    '_t' will translate strings given a locale
    For example: 
        response = _t(locale, _("Hello %(name)s!") ) % {"name":name}    

    Keyword arguments:
    text -- the text to translate
    locale -- the language code to translate to (defaults to 'en')

    """
    # TODO: handle mappings from old-style two letter ('en')
    # to new hotness 3-letter codes 'eng'
    global _sms_translations, _sms_default
    translator = _sms_translations[_sms_default].translator
    if locale is None:
        locale = _sms_default
    if locale in _sms_translations:
        translator = _sms_translations[locale].translator
    return translator.ugettext(text)


def init(default='en', languages=[[ 'en','English' ]] , path=LOCALE_PATH):
    """ Global initialization function for sms i18n translators
    
    We use the class-based API of GNU Gettext to provide
    multiple dynamic translations
    Do not call this function in runserver, as it will foobar
    the web translations in unpredictable ways.
    
    Keyword arguments:
    default -- default language code ('en' by default)
    languages -- list of lists identifying supported languages
        of the form [ [ code,name,**aliases ] ] 
        e.g.  [ [ 'en','English' ],[ 'en','Francais','French' ] ] 
    path -- path to 'locale' dir used by gettext to find translation files

    """
    global _sms_translations, _sms_default
    _sms_default = default
    default_from_language = False
    if not _sms_default: 
        # if there is only one translation, it's the default
        if languages and len(languages)==1 and languages[0]:
            _sms_default = languages[0][0]
            default_from_language = True
        else: _sms_default = 'en'
    if not languages: 
        # if there is a default and no languages, 
        # that becomes the default language
        if _sms_default and not default_from_language:
            languages = [[ _sms_default,'Default' ]]
        else:
            languages = [[ 'en','Default' ]]
    for language in languages:
        if language:
            t = _Translation(language[0],language[1:])
            t.translator = gettext.translation('django',path,[t.slug,_sms_default], DjangoTranslation, fallback=True)
            _sms_translations.update ( {t.slug:t} )
    if _sms_default not in _sms_translations:
        raise Exception("i18n enabled but no default language specified! " +
                        "Please add default_language=<language_code> to rapidsms.ini")

class _Translation(object):
    def __init__(self, slug='', names=[]):
        self.slug = slug
        self.names = names
        self.translator = None


