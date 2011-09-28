# Copyright (C) 2010 IT Mill Ltd.
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


class IResource(object):
    """<code>IResource</code> provided to the client terminal. Support for
    actually displaying the resource type is left to the terminal.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def getMIMEType(self):
        """Gets the MIME type of the resource.

        @return the MIME type of the resource.
        """
        raise NotImplementedError