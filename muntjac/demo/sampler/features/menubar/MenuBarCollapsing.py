# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.menubar.BasicMenuBar import (BasicMenuBar,)
from com.vaadin.demo.sampler.features.menubar.MenuBarTooltips import (MenuBarTooltips,)
from com.vaadin.demo.sampler.features.menubar.MenuBarHiddenItems import (MenuBarHiddenItems,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.menubar.MenuBarWithIcons import (MenuBarWithIcons,)
from com.vaadin.demo.sampler.features.menubar.MenuBarItemStyles import (MenuBarItemStyles,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class MenuBarCollapsing(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'MenuBar, collapsing items'

    def getDescription(self):
        return 'If the root level menu has more items that can fit in view (and if the MenuBar has a specified width), overflowing items will be collapsed to a generated sub-menu last in the root menu, indicated by an arrow.<br /><br/>Resize the browser window to collapse/expand more items.'

    def getRelatedAPI(self):
        return [APIResource(MenuBar)]

    def getRelatedFeatures(self):
        return [BasicMenuBar, MenuBarWithIcons, MenuBarHiddenItems, MenuBarItemStyles, MenuBarTooltips]

    def getRelatedResources(self):
        return None