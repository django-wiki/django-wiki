# This package and all its sub-packages are part of django-wiki,
# except where otherwise stated.
#
# django-wiki is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-wiki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-wiki. If not, see <http://www.gnu.org/licenses/>.


from wiki.core.version import get_version

default_app_config = 'wiki.apps.WikiConfig'

VERSION = (0, 4, 1, 'final', 0)
__version__ = get_version(VERSION)
