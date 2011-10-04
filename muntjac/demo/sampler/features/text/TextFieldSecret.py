# -*- coding: utf-8 -*-
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.features.selects.ComboBoxNewItems import (ComboBoxNewItems,)
from muntjac.demo.sampler.features.text.TextFieldSingle import (TextFieldSingle,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TextFieldSecret(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Text field, secret (password)'

    def getDescription(self):
        return 'For sensitive data input, such as passwords, the text field can' + ' also be set into secret mode where the input will not be' + ' echoed to display.'

    def getRelatedAPI(self):
        return [APIResource(TextField)]

    def getRelatedFeatures(self):
        # TODO update CB -ref to 'suggest' pattern, when available
        return [TextFieldSingle, ComboBoxNewItems, FeatureSet.Texts]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
