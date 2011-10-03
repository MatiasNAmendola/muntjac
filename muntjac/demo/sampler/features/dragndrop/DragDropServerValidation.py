# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dragndrop.DragDropHtml5FromDesktop import (DragDropHtml5FromDesktop,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropTreeSorting import (DragDropTreeSorting,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropTableTree import (DragDropTableTree,)
from com.vaadin.demo.sampler.features.dragndrop.DragDropRearrangeComponents import (DragDropRearrangeComponents,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class DragDropServerValidation(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getDescription(self):
        return 'In more complex cases, the browser might not have enough information to decide whether something can be dropped at a given location. ' + 'In these cases, the drag mechanism can ask the server whether dropping an item at a particular location is allowed. ' + 'Drag persons onto others with the same last name.'

    def getName(self):
        return 'Drop validation, server'

    def getRelatedAPI(self):
        return [APIResource(ServerSideCriterion), APIResource(Table), APIResource(DropHandler)]

    def getRelatedFeatures(self):
        return [DragDropTreeSorting, DragDropTableTree, DragDropRearrangeComponents, DragDropHtml5FromDesktop]

    def getRelatedResources(self):
        return None