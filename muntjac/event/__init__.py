"""Provides classes and interfaces for the inheritable event model. The model
supports inheritable events and a flexible way of registering and unregistering
event listeners. It's a fundamental building block of Muntjac, and as it is
included in L{muntjac.ui.abstract_component.AbstractComponent}, all UI
components automatically support it.

Package Specification
---------------------

The core of the event model is the inheritable event class hierarchy, and the
L{EventRouter} which provide a simple, ubiquitous mechanism to transport events
to all interested parties.

The power of the event inheritance arises from the possibility of receiving not
only the events of the registered type, I{but also the ones which are inherited
from it}. For example, let's assume that there are the events C{GeneralEvent}
and C{SpecializedEvent} so that the latter inherits the former. Furthermore we
have an object C{A} which registers to receive C{GeneralEvent} type events from
the object C{B}. C{A} would of course receive all C{GeneralEvent}s generated by
C{B}, but in addition to this, C{A} would also receive all C{SpecializedEvent}s
generated by C{B}. However, if C{B} generates some other events that do not
have C{GeneralEvent} as an ancestor, C{A} would not receive them unless it
registers to listen for them, too.

The interface to attaching and detaching listeners to and from an object
works with methods. One specifies the event that should trigger the listener,
the trigger method that should be called when a suitable event occurs and the
object owning the method. From these a new listener is constructed and added
to the event router of the specified component.

The interface is defined in L{MethodEventSource}, and a straightforward
implementation of it is defined in L{EventRouter} which also includes a method
to actually fire the events.

All fired events are passed to all registered listeners, which are of type
L{ListenerMethod}. The listener then checks if the event type matches with the
specified event type and calls the specified trigger method if it does."""
