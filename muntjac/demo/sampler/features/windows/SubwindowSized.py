# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.windows.SubwindowAutoSized import (SubwindowAutoSized,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SubwindowSized(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Window, explicit size'

    def getDescription(self):
        return 'The size of a window can be specified - here the width is set' + ' in pixels, and the height in percent.'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [SubwindowAutoSized, FeatureSet.Windows]

    def getRelatedResources(self):
        return None
