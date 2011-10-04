# -*- coding: utf-8 -*-
from muntjac.demo.sampler.ExampleUtil import (ExampleUtil,)
# from com.vaadin.ui.AbstractSelect.Filtering import (Filtering,)


class ComboBoxContainsExample(VerticalLayout, Property.ValueChangeListener):

    def __init__(self):
        # Shows a notification when a selection is made.
        self.setSpacing(True)
        # Creates a new combobox using an existing container
        l = ComboBox('Please select your country', ExampleUtil.getISO3166Container())
        # Sets the combobox to show a certain property as the item caption
        l.setItemCaptionPropertyId(ExampleUtil.iso3166_PROPERTY_NAME)
        l.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        # Sets the icon to use with the items
        l.setItemIconPropertyId(ExampleUtil.iso3166_PROPERTY_FLAG)
        # Set a reasonable width
        l.setWidth(350, self.UNITS_PIXELS)
        # Set the appropriate filtering mode for this example
        l.setFilteringMode(Filtering.FILTERINGMODE_CONTAINS)
        l.setImmediate(True)
        l.addListener(self)
        # Disallow null selections
        l.setNullSelectionAllowed(False)
        self.addComponent(l)

    def valueChange(self, event):
        selected = ExampleUtil.getISO3166Container().getContainerProperty(str(event.getProperty()), 'name')
        self.getWindow().showNotification('Selected country: ' + selected)
