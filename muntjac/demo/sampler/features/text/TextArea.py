# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.text.RichTextEditor import (RichTextEditor,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.features.text.TextFieldSingle import (TextFieldSingle,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TextArea(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Text area'

    def getDescription(self):
        return 'A text field can be configured to allow multiple lines of input.' + '<br>The amount of columns and lines can be set, and both are set here to' + ' 20 characters. Note that this only affects the width and height of the' + ' component, not the allowed length of input.'

    def getRelatedAPI(self):
        return [APIResource(TextField)]

    def getRelatedFeatures(self):
        return [RichTextEditor, TextFieldSingle, FeatureSet.Texts]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
