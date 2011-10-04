# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.embedded.ImageEmbed import (ImageEmbed,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class FlashEmbed(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Flash'

    def getDescription(self):
        return 'Flash movies, such as YouTube videos, can easily be embedded to your applications.'

    def getRelatedAPI(self):
        return [APIResource(Embedded), APIResource(ThemeResource), APIResource(ClassResource), APIResource(ExternalResource)]

    def getRelatedFeatures(self):
        return [ImageEmbed]

    def getRelatedResources(self):
        return None
