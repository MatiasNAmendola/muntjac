# -*- coding: utf-8 -*-
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.features.table.TableClickListenersExample import (TableClickListenersExample,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TableClickListeners(Feature):

    def getDescription(self):
        return 'You can assign a click listener to the column headers and footers to handle user mouse clicks.'

    def getName(self):
        return 'Table, click listeners'

    def getRelatedAPI(self):
        return [APIResource(Table)]

    def getRelatedFeatures(self):
        return [FeatureSet.Tables]

    def getRelatedResources(self):
        return None

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return TableClickListenersExample()
