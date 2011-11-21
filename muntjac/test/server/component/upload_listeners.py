# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from muntjac.test.server.component.abstract_listener_methods_test import \
    AbstractListenerMethodsTest

from muntjac.ui.upload import \
    (Upload, IProgressListener, SucceededEvent, ISucceededListener,
     StartedEvent, IStartedListener, FailedEvent, IFailedListener,
     FinishedEvent, IFinishedListener)

from muntjac.terminal.stream_variable import IStreamingProgressEvent


class UploadListeners(AbstractListenerMethodsTest):

    def testProgressListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, IStreamingProgressEvent,
                IProgressListener)

    def testSucceededListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, SucceededEvent,
                ISucceededListener)

    def testStartedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, StartedEvent,
                IStartedListener)


    def testFailedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, FailedEvent,
                IFailedListener)

    def testFinishedListenerAddGetRemove(self):
        self._testListenerAddGetRemove(Upload, FinishedEvent,
                IFinishedListener)
