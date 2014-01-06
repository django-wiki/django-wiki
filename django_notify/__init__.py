# -*- coding: utf-8 -*-
# This package and all its sub-packages are part of django_notify,
# except where otherwise stated.
#
# django_notify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django_notify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django_notify. If not, see <http://www.gnu.org/licenses/>.

# Unused feature, atm. everything is bundled with django-wiki
VERSION = "0.0.4"

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.utils.translation import ugettext as _

from . import models

_disable_notifications = False

def notify(message, key, target_object=None, url=None, filter_exclude={}):
    """
    Notify subscribing users of a new event. Key can be any kind of string,
    just make sure to reuse it where applicable! Object_id is some identifier
    of an object, for instance if a user subscribes to a specific comment thread,
    you could write:
    
    notify("there was a response to your comment", "comment_response", 
           target_object=PostersObject, 
           url=reverse('comments:view', args=(PostersObject.id,)))
    
    The below example notifies everyone subscribing to the "new_comments" key
    with the message "New comment posted".
    
    notify("New comment posted", "new_comments")
    
    filter_exclude: a dictionary to exclude special elements of subscriptions
    in the queryset, for instance filter_exclude={''}
    
    """
    
    if _disable_notifications:
        return 0
    
    if target_object:
        if not isinstance(target_object, Model):
            raise TypeError(_(u"You supplied a target_object that's not an instance of a django Model."))
        object_id = target_object.id
    else:
        object_id = None
        
    objects = models.Notification.create_notifications(
        key, 
        object_id=object_id, 
        message=message, 
        url=url, 
        filter_exclude=filter_exclude,
    )
    return len(objects)
    
