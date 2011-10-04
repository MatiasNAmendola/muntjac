
from muntjac.ui import Accordion

from muntjac.demo.sampler.FeatureSet import Tabsheets
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.demo.sampler.features.accordions.AccordionDisabled import \
    AccordionDisabled


class AccordionIcons(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Accordion with icons'


    def getDescription(self):
        return 'The accordion \'tabs\' can contain icons in addition to the caption.'


    def getRelatedAPI(self):
        return [APIResource(Accordion)]


    def getRelatedFeatures(self):
        return [AccordionDisabled, Tabsheets]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
