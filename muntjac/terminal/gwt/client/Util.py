# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR, POSTINC,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.Container import (Container,)
from com.vaadin.terminal.gwt.client.RenderInformation import (RenderInformation,)
from com.vaadin.terminal.gwt.client.ApplicationConnection import (ApplicationConnection,)
from com.vaadin.terminal.gwt.client.VCaption import (VCaption,)
from com.vaadin.terminal.gwt.client.UIDL import (UIDL,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
# from com.google.gwt.dom.client.DivElement import (DivElement,)
# from com.google.gwt.dom.client.Node import (Node,)
# from com.google.gwt.dom.client.NodeList import (NodeList,)
# from com.google.gwt.dom.client.Touch import (Touch,)
# from com.google.gwt.user.client.EventListener import (EventListener,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.HashMap import (HashMap,)
# from java.util.HashSet import (HashSet,)
# from java.util.Iterator import (Iterator,)
# from java.util.Map import (Map,)
# from java.util.Set import (Set,)
FloatSize = RenderInformation.FloatSize


class Util(object):

    @classmethod
    def browserDebugger(cls):
        """Helper method for debugging purposes.

        Stops execution on firefox browsers on a breakpoint.
        """
        JS("""
        if($wnd.console)
            debugger;
    """)
        pass

    @classmethod
    def getElementFromPoint(cls, clientX, clientY):
        """Returns the topmost element of from given coordinates.

        TODO fix crossplat issues clientX vs pageX. See quircksmode. Not critical
        for vaadin as we scroll div istead of page.

        @param x
        @param y
        @return the element at given coordinates
        """
        JS("""
        var el = $wnd.document.elementFromPoint(@{{clientX}}, @{{clientY}});
        if(el != null && el.nodeType == 3) {
            el = el.parentNode;
        }
        return el;
    """)
        pass

    _LAZY_SIZE_CHANGE_TIMEOUT = 400
    _latelyChangedWidgets = set()

    class lazySizeChangeTimer(Timer):
        _lazySizeChangeTimerScheduled = False

        def run(self):
            Util_this.componentSizeUpdated(Util_this._latelyChangedWidgets)
            Util_this._latelyChangedWidgets.clear()
            self._lazySizeChangeTimerScheduled = False

        def schedule(self, delayMillis):
            if self._lazySizeChangeTimerScheduled:
                self.cancel()
            else:
                self._lazySizeChangeTimerScheduled = True
            super(_0_, self).schedule(delayMillis)

    @classmethod
    def notifyParentOfSizeChange(cls, widget, lazy):
        """This helper method can be called if components size have been changed
        outside rendering phase. It notifies components parent about the size
        change so it can react.

        When using this method, developer should consider if size changes could
        be notified lazily. If lazy flag is true, method will save widget and
        wait for a moment until it notifies parents in chunks. This may vastly
        optimize layout in various situation. Example: if component have a lot of
        images their onload events may fire "layout phase" many times in a short
        period.

        @param widget
        @param lazy
                   run componentSizeUpdated lazyly
        """
        if lazy:
            cls._latelyChangedWidgets.add(widget)
            cls.lazySizeChangeTimer.schedule(cls._LAZY_SIZE_CHANGE_TIMEOUT)
        else:
            widgets = set()
            widgets.add(widget)
            Util.componentSizeUpdated(widgets)

    @classmethod
    def componentSizeUpdated(cls, paintables):
        """Called when the size of one or more widgets have changed during
        rendering. Finds parent container and notifies them of the size change.

        @param paintables
        """
        if paintables.isEmpty():
            return
        childWidgets = dict()
        for paintable in paintables:
            widget = paintable
            if not widget.isAttached():
                continue
            # ApplicationConnection.getConsole().log(
            # "Widget " + Util.getSimpleName(widget) + " size updated");
            parent = widget.getParent()
            while parent is not None and not isinstance(parent, Container):
                parent = parent.getParent()
            if parent is not None:
                set = childWidgets[parent]
                if set is None:
                    set = set()
                    childWidgets.put(parent, set)
                set.add(paintable)
        parentChanges = set()
        for parent in childWidgets.keys():
            if not parent.requestLayout(childWidgets[parent]):
                parentChanges.add(parent)
        cls.componentSizeUpdated(parentChanges)

    @classmethod
    def parseRelativeSize(cls, *args):
        """None
        ---
        Parses the UIDL parameter and fetches the relative size of the component.
        If a dimension is not specified as relative it will return -1. If the
        UIDL does not contain width or height specifications this will return
        null.

        @param uidl
        @return
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], UIDL):
                uidl, = _0
                hasAttribute = False
                w = ''
                h = ''
                if uidl.hasAttribute('width'):
                    hasAttribute = True
                    w = uidl.getStringAttribute('width')
                if uidl.hasAttribute('height'):
                    hasAttribute = True
                    h = uidl.getStringAttribute('height')
                if not hasAttribute:
                    return None
                relativeWidth = Util.parseRelativeSize(w)
                relativeHeight = Util.parseRelativeSize(h)
                relativeSize = FloatSize(relativeWidth, relativeHeight)
                return relativeSize
            else:
                size, = _0
                if (size is None) or (not size.endswith('%')):
                    return -1
                try:
                    return cls.float(size[:-1])
                except Exception, e:
                    VConsole.log('Unable to parse relative size')
                    return -1
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def getLayout(cls, component):
        """Returns closest parent Widget in hierarchy that implements Container
        interface

        @param component
        @return closest parent Container
        """
        parent = component.getParent()
        while parent is not None and not isinstance(parent, Container):
            parent = parent.getParent()
        if parent is not None:
            assert parent.hasChildComponent(component)
            return parent
        return None

    @classmethod
    def isIE(cls):
        """Detects if current browser is IE.

        @deprecated use BrowserInfo class instead

        @return true if IE
        """
        return BrowserInfo.get().isIE()

    @classmethod
    def isIE6(cls):
        """Detects if current browser is IE6.

        @deprecated use BrowserInfo class instead

        @return true if IE6
        """
        return BrowserInfo.get().isIE6()

    @classmethod
    def isIE7(cls):
        """@deprecated use BrowserInfo class instead
        @return
        """
        return BrowserInfo.get().isIE7()

    @classmethod
    def isFF2(cls):
        """@deprecated use BrowserInfo class instead
        @return
        """
        return BrowserInfo.get().isFF2()

    _escapeHtmlHelper = DOM.createDiv()

    @classmethod
    def escapeHTML(cls, html):
        """Converts html entities to text.

        @param html
        @return escaped string presentation of given html
        """
        DOM.setInnerText(cls._escapeHtmlHelper, html)
        escapedText = DOM.getInnerHTML(cls._escapeHtmlHelper)
        if BrowserInfo.get().isIE() and BrowserInfo.get().getIEVersion() < 9:
            # #7478 IE6-IE8 "incorrectly" returns "<br>" for newlines set using
            # setInnerText. The same for " " which is converted to "&nbsp;"
            escapedText = escapedText.replaceAll('<(BR|br)>', '\n')
            escapedText = escapedText.replaceAll('&nbsp;', ' ')
        return escapedText

    @classmethod
    def escapeAttribute(cls, attribute):
        """Escapes the string so it is safe to write inside an HTML attribute.

        @param attribute
                   The string to escape
        @return An escaped version of <literal>attribute</literal>.
        """
        attribute = attribute.replace('\"', '&quot;')
        attribute = attribute.replace('\'', '&#39;')
        attribute = attribute.replace('>', '&gt;')
        attribute = attribute.replace('<', '&lt;')
        attribute = attribute.replace('&', '&amp;')
        return attribute

    @classmethod
    def addPngFix(cls, el):
        """Adds transparent PNG fix to image element; only use for IE6.

        @param el
                   IMG element
        """
        JS("""
        @{{el}}.attachEvent("onload", function() {
            @com.vaadin.terminal.gwt.client.Util::doIE6PngFix(Lcom/google/gwt/user/client/Element;)(@{{el}});
        },false);
    """)
        pass

    @classmethod
    def doPngFix(cls, el, blankImageUrl):
        JS("""
        var src = @{{el}}.src;
        if (src.indexOf(".png") < 1) return;
        var w = @{{el}}.width || 16; 
        var h = @{{el}}.height || 16;
        if(h==30 || w==28) {
            setTimeout(function(){
                @{{el}}.style.height = @{{el}}.height + "px";
                @{{el}}.style.width = @{{el}}.width + "px";
                @{{el}}.src = @{{blankImageUrl}};
            },10);
        } else {
            @{{el}}.src = @{{blankImageUrl}};
            @{{el}}.style.height = h + "px";
            @{{el}}.style.width = w + "px";
        }
        @{{el}}.style.padding = "0";
        @{{el}}.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='"+src+"', sizingMethod='crop')";  
       """)
        pass

    @classmethod
    def doIE6PngFix(cls, el):
        blankImageUrl = GWT.getModuleBaseURL() + 'ie6pngfix/blank.gif'
        src = el.getAttribute('src')
        if src is not None and not (src == blankImageUrl):
            cls.doPngFix(el, blankImageUrl)

    @classmethod
    def cloneNode(cls, element, deep):
        """Clones given element as in JavaScript.

        Deprecate this if there appears similar method into GWT someday.

        @param element
        @param deep
                   clone child tree also
        @return
        """
        JS("""
        return @{{element}}.cloneNode(@{{deep}});
    """)
        pass

    @classmethod
    def measureHorizontalPaddingAndBorder(cls, element, paddingGuess):
        originalWidth = DOM.getStyleAttribute(element, 'width')
        originalOverflow = ''
        if BrowserInfo.get().isIE6():
            originalOverflow = DOM.getStyleAttribute(element, 'overflow')
            DOM.setStyleAttribute(element, 'overflow', 'hidden')
        originalOffsetWidth = element.getOffsetWidth()
        widthGuess = originalOffsetWidth - paddingGuess
        if widthGuess < 1:
            widthGuess = 1
        DOM.setStyleAttribute(element, 'width', widthGuess + 'px')
        padding = element.getOffsetWidth() - widthGuess
        DOM.setStyleAttribute(element, 'width', originalWidth)
        if BrowserInfo.get().isIE6():
            DOM.setStyleAttribute(element, 'overflow', originalOverflow)
        return padding

    @classmethod
    def measureVerticalPaddingAndBorder(cls, element, paddingGuess):
        originalHeight = DOM.getStyleAttribute(element, 'height')
        originalOffsetHeight = element.getOffsetHeight()
        widthGuess = originalOffsetHeight - paddingGuess
        if widthGuess < 1:
            widthGuess = 1
        DOM.setStyleAttribute(element, 'height', widthGuess + 'px')
        padding = element.getOffsetHeight() - widthGuess
        DOM.setStyleAttribute(element, 'height', originalHeight)
        return padding

    @classmethod
    def measureHorizontalBorder(cls, element):
        if BrowserInfo.get().isIE():
            width = element.getStyle().getProperty('width')
            height = element.getStyle().getProperty('height')
            offsetWidth = element.getOffsetWidth()
            offsetHeight = element.getOffsetHeight()
            if not BrowserInfo.get().isIE7():
                if offsetHeight < 1:
                    offsetHeight = 1
                if offsetWidth < 1:
                    offsetWidth = 10
                element.getStyle().setPropertyPx('height', offsetHeight)
            element.getStyle().setPropertyPx('width', offsetWidth)
            borders = element.getOffsetWidth() - element.getClientWidth()
            element.getStyle().setProperty('width', width)
            if not BrowserInfo.get().isIE7():
                element.getStyle().setProperty('height', height)
        else:
            borders = element.getOffsetWidth() - element.getPropertyInt('clientWidth')
        assert borders >= 0
        return borders

    @classmethod
    def measureVerticalBorder(cls, element):
        if BrowserInfo.get().isIE():
            width = element.getStyle().getProperty('width')
            height = element.getStyle().getProperty('height')
            offsetWidth = element.getOffsetWidth()
            offsetHeight = element.getOffsetHeight()
            # if (BrowserInfo.get().isIE6()) {
            if offsetHeight < 1:
                offsetHeight = 1
            if offsetWidth < 1:
                offsetWidth = 10
            element.getStyle().setPropertyPx('width', offsetWidth)
            # }
            element.getStyle().setPropertyPx('height', offsetHeight)
            borders = element.getOffsetHeight() - element.getPropertyInt('clientHeight')
            element.getStyle().setProperty('height', height)
            # if (BrowserInfo.get().isIE6()) {
            element.getStyle().setProperty('width', width)
            # }
        else:
            borders = element.getOffsetHeight() - element.getPropertyInt('clientHeight')
        assert borders >= 0
        return borders

    @classmethod
    def measureMarginLeft(cls, element):
        return element.getAbsoluteLeft() - element.getParentElement().getAbsoluteLeft()

    @classmethod
    def setHeightExcludingPaddingAndBorder(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 3:
            widget, height, paddingBorderGuess = _0
            if height == '':
                cls.setHeight(widget, '')
                return paddingBorderGuess
            elif height.endswith('px'):
                pixelHeight = int(height[:-2])
                return cls.setHeightExcludingPaddingAndBorder(widget.getElement(), pixelHeight, paddingBorderGuess, False)
            else:
                # Set the height in unknown units
                cls.setHeight(widget, height)
                # Use the offsetWidth
                return cls.setHeightExcludingPaddingAndBorder(widget.getElement(), widget.getOffsetHeight(), paddingBorderGuess, True)
        elif _1 == 4:
            element, requestedHeight, verticalPaddingBorderGuess, requestedHeightIncludesPaddingBorder = _0
            heightGuess = requestedHeight - verticalPaddingBorderGuess
            if heightGuess < 0:
                heightGuess = 0
            DOM.setStyleAttribute(element, 'height', heightGuess + 'px')
            captionOffsetHeight = DOM.getElementPropertyInt(element, 'offsetHeight')
            actualPadding = captionOffsetHeight - heightGuess
            if requestedHeightIncludesPaddingBorder:
                actualPadding += actualPadding
            if actualPadding != verticalPaddingBorderGuess:
                h = requestedHeight - actualPadding
                if h < 0:
                    # Cannot set negative height even if we would want to
                    h = 0
                DOM.setStyleAttribute(element, 'height', h + 'px')
            return actualPadding
        else:
            raise ARGERROR(3, 4)

    @classmethod
    def setWidth(cls, widget, width):
        DOM.setStyleAttribute(widget.getElement(), 'width', width)

    @classmethod
    def setHeight(cls, widget, height):
        DOM.setStyleAttribute(widget.getElement(), 'height', height)

    @classmethod
    def setWidthExcludingPaddingAndBorder(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 3:
            widget, width, paddingBorderGuess = _0
            if width == '':
                cls.setWidth(widget, '')
                return paddingBorderGuess
            elif width.endswith('px'):
                pixelWidth = int(width[:-2])
                return cls.setWidthExcludingPaddingAndBorder(widget.getElement(), pixelWidth, paddingBorderGuess, False)
            else:
                cls.setWidth(widget, width)
                return cls.setWidthExcludingPaddingAndBorder(widget.getElement(), widget.getOffsetWidth(), paddingBorderGuess, True)
        elif _1 == 4:
            element, requestedWidth, horizontalPaddingBorderGuess, requestedWidthIncludesPaddingBorder = _0
            widthGuess = requestedWidth - horizontalPaddingBorderGuess
            if widthGuess < 0:
                widthGuess = 0
            DOM.setStyleAttribute(element, 'width', widthGuess + 'px')
            captionOffsetWidth = DOM.getElementPropertyInt(element, 'offsetWidth')
            actualPadding = captionOffsetWidth - widthGuess
            if requestedWidthIncludesPaddingBorder:
                actualPadding += actualPadding
            if actualPadding != horizontalPaddingBorderGuess:
                w = requestedWidth - actualPadding
                if w < 0:
                    # Cannot set negative width even if we would want to
                    w = 0
                DOM.setStyleAttribute(element, 'width', w + 'px')
            return actualPadding
        else:
            raise ARGERROR(3, 4)

    @classmethod
    def getSimpleName(cls, widget):
        if widget is None:
            return '(null)'
        name = widget.getClass().getName()
        return name[name.rfind('.') + 1:]

    @classmethod
    def setFloat(cls, element, value):
        if BrowserInfo.get().isIE():
            DOM.setStyleAttribute(element, 'styleFloat', value)
        else:
            DOM.setStyleAttribute(element, 'cssFloat', value)

    _detectedScrollbarSize = -1

    @classmethod
    def getNativeScrollbarSize(cls):
        if cls._detectedScrollbarSize < 0:
            scroller = DOM.createDiv()
            scroller.getStyle().setProperty('width', '50px')
            scroller.getStyle().setProperty('height', '50px')
            scroller.getStyle().setProperty('overflow', 'scroll')
            scroller.getStyle().setProperty('position', 'absolute')
            scroller.getStyle().setProperty('marginLeft', '-5000px')
            RootPanel.getBodyElement().appendChild(scroller)
            cls._detectedScrollbarSize = scroller.getOffsetWidth() - scroller.getPropertyInt('clientWidth')
            RootPanel.getBodyElement().removeChild(scroller)
        return cls._detectedScrollbarSize

    @classmethod
    def runWebkitOverflowAutoFix(cls, elem):
        """Run workaround for webkits overflow auto issue.

        See: our bug #2138 and https://bugs.webkit.org/show_bug.cgi?id=21462

        @param elem
                   with overflow auto
        """
        # Add max version if fix lands sometime to Webkit
        # Starting from Opera 11.00, also a problem in Opera
        if (
            (BrowserInfo.get().getWebkitVersion() > 0) or (BrowserInfo.get().getOperaVersion() >= 11) and cls.getNativeScrollbarSize() > 0
        ):
            originalOverflow = elem.getStyle().getProperty('overflow')
            if 'hidden' == originalOverflow:
                return
            # check the scrolltop value before hiding the element
            scrolltop = elem.getScrollTop()
            scrollleft = elem.getScrollLeft()
            elem.getStyle().setProperty('overflow', 'hidden')

            class _1_(Command):

                def execute(self):
                    # Dough, Safari scroll auto means actually just a moped
                    self.elem.getStyle().setProperty('overflow', self.originalOverflow)
                    if (self.scrolltop > 0) or (self.elem.getScrollTop() > 0):
                        scrollvalue = self.scrolltop
                        if scrollvalue == 0:
                            # mysterious are the ways of webkits scrollbar
                            # handling. In some cases webkit reports bad (0)
                            # scrolltop before hiding the element temporary,
                            # sometimes after.
                            scrollvalue = self.elem.getScrollTop()
                        # fix another bug where scrollbar remains in wrong
                        # position
                        self.elem.setScrollTop(scrollvalue - 1)
                        self.elem.setScrollTop(scrollvalue)
                    # fix for #6940 : Table horizontal scroll sometimes not
                    # updated when collapsing/expanding columns
                    # Also appeared in Safari 5.1 with webkit 534 (#7667)
                    if (
                        BrowserInfo.get().isChrome() or (BrowserInfo.get().isSafari() and BrowserInfo.get().getWebkitVersion() >= 534) and (self.scrollleft > 0) or (self.elem.getScrollLeft() > 0)
                    ):
                        scrollvalue = self.scrollleft
                        if scrollvalue == 0:
                            # mysterious are the ways of webkits scrollbar
                            # handling. In some cases webkit may report a bad
                            # (0) scrollleft before hiding the element
                            # temporary, sometimes after.
                            scrollvalue = self.elem.getScrollLeft()
                        # fix another bug where scrollbar remains in wrong
                        # position
                        self.elem.setScrollLeft(scrollvalue - 1)
                        self.elem.setScrollLeft(scrollvalue)

            _1_ = _1_()
            Scheduler.get().scheduleDeferred(_1_)

    @classmethod
    def isCached(cls, uidl):
        return uidl.getBooleanAttribute('cached')

    @classmethod
    def alert(cls, string):
        if True:
            Window.alert(string)

    @classmethod
    def equals(cls, a, b):
        if a is None:
            return b is None
        return a == b

    @classmethod
    def updateRelativeChildrenAndSendSizeUpdateEvent(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 2:
            client, container = _0
            cls.updateRelativeChildrenAndSendSizeUpdateEvent(client, container, container)
        elif _1 == 3:
            client, container, widget = _0
            childIterator = container
            while childIterator.hasNext():
                w = childIterator.next()
                client.handleComponentRelativeSize(w)
            widgets = set()
            widgets.add(widget)
            Util.componentSizeUpdated(widgets)
        else:
            raise ARGERROR(2, 3)

    # Relative sized children must be updated first so the component has
    # the correct outer dimensions when signaling a size change to the
    # parent.

    @classmethod
    def getRequiredWidth(cls, *args):
        JS("""
        if (@{{element}}.getBoundingClientRect) {
          var rect = @{{element}}.getBoundingClientRect();
          return Math.ceil(rect.right - rect.left);
        } else {
          return @{{element}}.offsetWidth;
        }
    """)
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Widget):
                widget, = _0
                return cls.getRequiredWidth(widget.getElement())
            else:
                element, = _0
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def getRequiredHeight(cls, *args):
        JS("""
        var height;
        if (@{{element}}.getBoundingClientRect != null) {
          var rect = @{{element}}.getBoundingClientRect();
          height = Math.ceil(rect.bottom - rect.top);
        } else {
          height = @{{element}}.offsetHeight;
        }
        return height;
    """)
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Widget):
                widget, = _0
                return cls.getRequiredHeight(widget.getElement())
            else:
                element, = _0
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def mayHaveScrollBars(cls, pe):
        """Detects what is currently the overflow style attribute in given element.

        @param pe
                   the element to detect
        @return true if auto or scroll
        """
        overflow = cls.getComputedStyle(pe, 'overflow')
        if overflow is not None:
            if (overflow == 'auto') or (overflow == 'scroll'):
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def getComputedStyle(cls, el, p):
        """A simple helper method to detect "computed style" (aka style sheets +
        element styles). Values returned differ a lot depending on browsers.
        Always be very careful when using this.

        @param el
                   the element from which the style property is detected
        @param p
                   the property to detect
        @return String value of style property
        """
        JS("""
        try {
        
        if (@{{el}}.currentStyle) {
            // IE
            return @{{el}}.currentStyle[@{{p}}];
        } else if (window.getComputedStyle) {
            // Sa, FF, Opera
            var view = @{{el}}.ownerDocument.defaultView;
            return view.getComputedStyle(@{{el}},null).getPropertyValue(@{{p}});
        } else {
            // fall back for non IE, Sa, FF, Opera
            return "";
        }
        } catch (e) {
            return "";
        }

     """)
        pass

    @classmethod
    def runIE7ZeroSizedBodyFix(cls):
        """IE7 sometimes "forgets" to render content. This function runs a hack to
        workaround the bug if needed. This happens easily in framset. See #3295.
        """
        if BrowserInfo.get().isIE7():
            offsetWidth = RootPanel.getBodyElement().getOffsetWidth()
            if offsetWidth == 0:
                cls.shakeBodyElement()

    @classmethod
    def shakeBodyElement(cls):
        """Does some very small adjustments to body element. We need this just to
        overcome some IE bugs.
        """
        shaker = Document.get().createDivElement()
        RootPanel.getBodyElement().insertBefore(shaker, RootPanel.getBodyElement().getFirstChildElement())
        shaker.getStyle().setPropertyPx('height', 0)
        shaker.setInnerHTML('&nbsp;')
        RootPanel.getBodyElement().removeChild(shaker)

    @classmethod
    def getChildPaintableForElement(cls, client, parent, element):
        """Locates the child component of <literal>parent</literal> which contains
        the element <literal>element</literal>. The child component is also
        returned if "element" is part of its caption. If
        <literal>element</literal> is not part of any child component, null is
        returned.

        This method returns the immediate child of the parent that contains the
        element. See
        {@link #getPaintableForElement(ApplicationConnection, Container, Element)}
        for the deepest nested paintable of parent that contains the element.

        @param client
                   A reference to ApplicationConnection
        @param parent
                   The widget that contains <literal>element</literal>.
        @param element
                   An element that is a sub element of the parent
        @return The Paintable which the element is a part of. Null if the element
                does not belong to a child.
        """
        rootElement = parent.getElement()
        while element is not None and element != rootElement:
            paintable = client.getPaintable(element)
            if paintable is None:
                ownerPid = VCaption.getCaptionOwnerPid(element)
                if ownerPid is not None:
                    paintable = client.getPaintable(ownerPid)
            if paintable is not None:
                # We assume everything is a widget however there is no need
                # to crash everything if there is a paintable that is not.
                try:
                    if parent.hasChildComponent(paintable):
                        return paintable
                except cls.ClassCastException, e:
                    pass # astStmt: [Stmt([]), None]
            element = element.getParentElement()
        return None

    @classmethod
    def getPaintableForElement(cls, client, parent, element):
        """Locates the nested child component of <literal>parent</literal> which
        contains the element <literal>element</literal>. The child component is
        also returned if "element" is part of its caption. If
        <literal>element</literal> is not part of any child component, null is
        returned.

        This method returns the deepest nested Paintable. See
        {@link #getChildPaintableForElement(ApplicationConnection, Container, Element)}
        for the immediate child component of parent that contains the element.

        @param client
                   A reference to ApplicationConnection
        @param parent
                   The widget that contains <literal>element</literal>.
        @param element
                   An element that is a sub element of the parent
        @return The Paintable which the element is a part of. Null if the element
                does not belong to a child.
        """
        rootElement = parent.getElement()
        while element is not None and element != rootElement:
            paintable = client.getPaintable(element)
            if paintable is None:
                ownerPid = VCaption.getCaptionOwnerPid(element)
                if ownerPid is not None:
                    paintable = client.getPaintable(ownerPid)
            if paintable is not None:
                # check that inside the rootElement
                while element is not None and element != rootElement:
                    element = element.getParentElement()
                if element != rootElement:
                    return None
                else:
                    return paintable
            element = element.getParentElement()
        return None

    @classmethod
    def focus(cls, el):
        """Will (attempt) to focus the given DOM Element.

        @param el
                   the element to focus
        """
        JS("""
        try {
            @{{el}}.focus();
        } catch (e) {

        }
    """)
        pass

    @classmethod
    def findWidget(cls, element, class1):
        """Helper method to find first instance of given Widget type found by
        traversing DOM upwards from given element.

        @param element
                   the element where to start seeking of Widget
        @param class1
                   the Widget type to seek for
        """
        if element is not None:
            # First seek for the first EventListener (~Widget) from dom
            eventListener = None
            while eventListener is None and element is not None:
                eventListener = Event.getEventListener(element)
                if eventListener is None:
                    element = element.getParentElement()
            if eventListener is not None:
                # Then find the first widget of type class1 from widget
                # hierarchy

                w = eventListener
                while w is not None:
                    if (class1 is None) or (w.getClass() == class1):
                        return w
                    w = w.getParent()
        return None

    @classmethod
    def forceWebkitRedraw(cls, element):
        """Force webkit to redraw an element

        @param element
                   The element that should be redrawn
        """
        style = element.getStyle()
        s = style.getProperty('webkitTransform')
        if (s is None) or (len(s) == 0):
            style.setProperty('webkitTransform', 'scale(1)')
        else:
            style.setProperty('webkitTransform', '')

    @classmethod
    def detachAttach(cls, element):
        """Detaches and re-attaches the element from its parent. The element is
        reattached at the same position in the DOM as it was before.

        Does nothing if the element is not attached to the DOM.

        @param element
                   The element to detach and re-attach
        """
        if element is None:
            return
        nextSibling = element.getNextSibling()
        parent = element.getParentNode()
        if parent is None:
            return
        parent.removeChild(element)
        if nextSibling is None:
            parent.appendChild(element)
        else:
            parent.insertBefore(element, nextSibling)

    @classmethod
    def sinkOnloadForImages(cls, element):
        imgElements = element.getElementsByTagName('img')
        _0 = True
        i = 0
        while True:
            if _0 is True:
                _0 = False
            else:
                i += 1
            if not (i < imgElements.getLength()):
                break
            DOM.sinkEvents(imgElements.getItem(i), Event.ONLOAD)

    @classmethod
    def getChildElementIndex(cls, childElement):
        """Returns the index of the childElement within its parent.

        @param subElement
        @return
        """
        idx = 0
        n = childElement
        while n = n.getPreviousSibling() is not None:
            idx += 1
        return idx

    @classmethod
    def printPaintablesVariables(cls, vars, id, c):
        paintable = c.getPaintable(id)
        if paintable is not None:
            VConsole.log('\t' + id + ' (' + paintable.getClass() + ') :')
            for var in vars:
                VConsole.log('\t\t' + var[1] + ' (' + var[2] + ')' + ' : ' + var[0])

    @classmethod
    def logVariableBurst(cls, c, loggedBurst):
        try:
            VConsole.log('Variable burst to be sent to server:')
            curId = None
            vars = list()
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < len(loggedBurst)):
                    break
                value = loggedBurst[POSTINC(globals(), locals(), 'i')]
                split = loggedBurst[i].split(String.valueOf.valueOf(ApplicationConnection.VAR_FIELD_SEPARATOR))
                id = split[0]
                if curId is None:
                    curId = id
                elif not (curId == id):
                    cls.printPaintablesVariables(vars, curId, c)
                    vars.clear()
                    curId = id
                split[0] = value
                vars.add(split)
            if not vars.isEmpty():
                cls.printPaintablesVariables(vars, curId, c)
        except Exception, e:
            VConsole.error(e)

    @classmethod
    def setStyleTemporarily(cls, element, styleProperty, tempValue):
        """Temporarily sets the {@code styleProperty} to {@code tempValue} and then
        resets it to its current value. Used mainly to work around rendering
        issues in IE (and possibly in other browsers)

        @param element
                   The target element
        @param styleProperty
                   The name of the property to set
        @param tempValue
                   The temporary value
        """
        style = element.getStyle()
        currentValue = style.getProperty(styleProperty)
        style.setProperty(styleProperty, tempValue)
        element.getOffsetWidth()
        style.setProperty(styleProperty, currentValue)

    @classmethod
    def getTouchOrMouseClientX(cls, *args):
        """A helper method to return the client position from an event. Returns
        position from either first changed touch (if touch event) or from the
        event itself.

        @param event
        @return
        ---
        @see #getTouchOrMouseClientX(Event)

        @param event
        @return
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Event):
                event, = _0
                if cls.isTouchEvent(event):
                    return event.getChangedTouches().get(0).getClientX()
                else:
                    return event.getClientX()
            else:
                event, = _0
                return cls.getTouchOrMouseClientX(Event.as_(event))
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def getTouchOrMouseClientY(cls, *args):
        """A helper method to return the client position from an event. Returns
        position from either first changed touch (if touch event) or from the
        event itself.

        @param event
        @return
        ---
        @see #getTouchOrMouseClientY(Event)
        @param currentGwtEvent
        @return
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Event):
                event, = _0
                if cls.isTouchEvent(event):
                    return event.getChangedTouches().get(0).getClientY()
                else:
                    return event.getClientY()
            else:
                currentGwtEvent, = _0
                return cls.getTouchOrMouseClientY(Event.as_(currentGwtEvent))
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def isTouchEvent(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], Event):
                event, = _0
                return event.getType().contains('touch')
            else:
                event, = _0
                return cls.isTouchEvent(Event.as_(event))
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def simulateClickFromTouchEvent(cls, touchevent, widget):
        touch = touchevent.getChangedTouches().get(0)
        createMouseUpEvent = Document.get().createMouseUpEvent(0, touch.getScreenX(), touch.getScreenY(), touch.getClientX(), touch.getClientY(), False, False, False, False, NativeEvent.BUTTON_LEFT)
        createMouseDownEvent = Document.get().createMouseDownEvent(0, touch.getScreenX(), touch.getScreenY(), touch.getClientX(), touch.getClientY(), False, False, False, False, NativeEvent.BUTTON_LEFT)
        createMouseClickEvent = Document.get().createClickEvent(0, touch.getScreenX(), touch.getScreenY(), touch.getClientX(), touch.getClientY(), False, False, False, False)
        # Get target with element from point as we want the actual element, not
        # the one that sunk the event.

        target = cls.getElementFromPoint(touch.getClientX(), touch.getClientY())

        class _2_(ScheduledCommand):

            def execute(self):
                try:
                    self.target.dispatchEvent(self.createMouseDownEvent)
                    self.target.dispatchEvent(self.createMouseUpEvent)
                    self.target.dispatchEvent(self.createMouseClickEvent)
                except Exception, e:
                    pass # astStmt: [Stmt([]), None]

        _2_ = _2_()
        Scheduler.get().scheduleDeferred(_2_)

    @classmethod
    def getIEFocusedElement(cls):
        """Gets the currently focused element for Internet Explorer.

        @return The currently focused element
        """
        JS("""
       if ($wnd.document.activeElement) {
           return $wnd.document.activeElement;
       }
       
       return null;
     """)
        pass

    @classmethod
    def isAttachedAndDisplayed(cls, widget):
        """Kind of stronger version of isAttached(). In addition to std isAttached,
        this method checks that this widget nor any of its parents is hidden. Can
        be e.g used to check whether component should react to some events or
        not.

        @param widget
        @return true if attached and displayed
        """
        if widget.isAttached():
            # Failfast using offset size, then by iterating the widget tree
            notZeroSized = (widget.getOffsetHeight() > 0) or (widget.getOffsetWidth() > 0)
            return notZeroSized or cls.checkVisibilityRecursively(widget)
        else:
            return False

    @classmethod
    def checkVisibilityRecursively(cls, widget):
        if widget.isVisible():
            parent = widget.getParent()
            if parent is None:
                return True
                # root panel
            else:
                return cls.checkVisibilityRecursively(parent)
        else:
            return False

    @classmethod
    def scrollIntoViewVertically(cls, elem):
        """Scrolls an element into view vertically only. Modified version of
        Element.scrollIntoView.

        @param elem
                   The element to scroll into view
        """
        JS("""
        var top = @{{elem}}.offsetTop;
        var height = @{{elem}}.offsetHeight;
    
        if (@{{elem}}.parentNode != @{{elem}}.offsetParent) {
          top -= @{{elem}}.parentNode.offsetTop;
        }
    
        var cur = @{{elem}}.parentNode;
        while (cur && (cur.nodeType == 1)) {
          if (top < cur.scrollTop) {
            cur.scrollTop = top;
          }
          if (top + height > cur.scrollTop + cur.clientHeight) {
            cur.scrollTop = (top + height) - cur.clientHeight;
          }
    
          var offsetTop = cur.offsetTop;
          if (cur.parentNode != cur.offsetParent) {
            offsetTop -= cur.parentNode.offsetTop;
          }
           
          top += offsetTop - cur.scrollTop;
          cur = cur.parentNode;
        }
     """)
        pass
