#-------------------------------------------------------------------------------
# Name:        eveData
# Purpose:     Connect to the API, CREST to get game data
#
# Author:      Gallica
#
# Created:     13/04/2015
# Copyright:   (c) Gallica 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib.request
import urllib.parse
import xml.dom.minidom

class eveData:

    def __init__(self, auth=None, crest=None, system='prod'):

        if system == 'prod':
            self.apiurl = 'https://api.eveonline.com'
            self.pubcresturl = 'https://public-crest.eveonline.com'
            self.authcresturl = 'https://crest-tq.eveoline.com'
            self.imagesurl = 'https://image.eveonline.com'
        else:
            self.apiurl = 'https://api.testeveonline.com'
            self.pubcresturl = 'https://public-crest-sisi.testeveonline.com'
            self.authcresturl = 'https://api-sisi.testeveoline.com'
            self.imagesurl = 'https://image.testeveonline.com'

        if auth is None:
            raise ValueError('Need to have an Eve API key')
        elif len(auth) != 2:
            raise ValueError('Need a tuple ( key, vCode)')
        else:
            self.apikey = auth

        if crest:
            self.crestauth = crest


    def getCharacters():
