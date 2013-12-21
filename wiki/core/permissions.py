from wiki.conf import settings
from django.core.exceptions import ImproperlyConfigured
import imp


if settings.PERMISSIONS_MODULE:
    try:
        module_name = settings.PERMISSIONS_MODULE
        m = module_name.split('.')

        file, pathname, description = imp.find_module(m[0])       
        try:
            per = imp.load_module(module_name, file, pathname, description)
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if file:
                file.close()
        
        #Helper for app loading order problem.
        if (not hasattr(per, 'can_read') and not hasattr(per, 'can_write') and not hasattr(per, 'can_admin') and
                not hasattr(per, 'can_can_delete') and not hasattr(per, 'can_moderate') and
                not hasattr(per, 'can_assign') and not hasattr(per, 'can_assign_owner') and 
                not hasattr(per, 'can_change_permissions')):
            raise ImproperlyConfigured('django-wiki: No function was found in your PERMISSIONS_MODULE file. It might be because the app it depends on is no yet loaded. Check app loading order.')
    
    except IOError:
        raise ImproperlyConfigured('django-wiki: Your PERMISSIONS_MODULE file does not seem to exists.')



###############################
# ARTICLE PERMISSION HANDLING #
###############################
#
# All functions are:
#   can_something(article, user)
#      => True/False
#
# All functions can be replaced by pointing their relevant
# settings variable in wiki.conf.settings to a callable(article, user)

def can_read(article, user):
    if callable(settings.CAN_READ):
        return settings.CAN_READ(article, user)
    elif hasattr(per, 'can_read'):
        return per.can_read(article, user)        
    else:
        # Deny reading access to deleted articles if user has no delete access
        article_is_deleted = article.current_revision and article.current_revision.deleted
        if article_is_deleted and not article.can_delete(user):
            return False
        
        # Check access for other users...
        if user.is_anonymous() and not settings.ANONYMOUS:
            return False
        elif article.other_read:
            return True
        elif user.is_anonymous():
            return  False
        if user == article.owner:
            return True
        if article.group_read:
            if article.group and user.groups.filter(id=article.group.id).exists():
                return True
        if article.can_moderate(user):
            return True
        return False
        
def can_write(article, user):
    if callable(settings.CAN_WRITE):
        return settings.CAN_WRITE(article, user)
    elif hasattr(per, 'can_write'):
        return per.can_write(article, user)         
    else:
        # Check access for other users...
        if user.is_anonymous() and not settings.ANONYMOUS_WRITE:
            return False
        elif article.other_write:
            return True
        elif user.is_anonymous():
            return  False
        if user == article.owner:
            return True
        if article.group_write:
            if article.group and user and user.groups.filter(id=article.group.id).exists():
                return True
        if article.can_moderate(user):
            return True
        return False

def can_assign(article, user):
    if callable(settings.CAN_ASSIGN):
        return settings.CAN_ASSIGN(article, user)
    elif hasattr(per, 'can_assign'):
        return per.can_assign(article, user)        
    else:
        return not user.is_anonymous() and user.has_perm('wiki.assign')

def can_assign_owner(article, user):
    if callable(settings.CAN_ASSIGN_OWNER):
        return settings.CAN_ASSIGN_OWNER(article, user)
    elif hasattr(per, 'can_assign_owner'):
        return per.can_assign_owner(article, user)        
    else:
        return False

def can_change_permissions(article, user):
    if callable(settings.CAN_CHANGE_PERMISSIONS):
        return settings.CAN_CHANGE_PERMISSIONS(article, user)
    elif hasattr(per, 'can_change_permissions'):
        return per.can_change_permissions(article, user)        
    else:
        return (
            not user.is_anonymous() and (
                article.owner == user or 
                user.has_perm('wiki.assign')
            )
        )

def can_delete(article, user):
    if callable(settings.CAN_DELETE):
        return settings.CAN_DELETE(article, user)
    elif hasattr(per, 'can_delete'):
        return per.can_delete(article, user)        
    else:
        return not user.is_anonymous() and article.can_write(user)

def can_moderate(article, user):
    if callable(settings.CAN_MODERATE):
        return settings.CAN_MODERATE(article, user)
    elif hasattr(per, 'can_moderate'):
        return per.can_moderate(article, user)        
    else:
        return not user.is_anonymous() and user.has_perm('wiki.moderate')

def can_admin(article, user):
    if callable(settings.CAN_ADMIN):
        return settings.CAN_ADMIN(article, user)
    elif hasattr(per, 'can_admin'):
        return per.can_admin(article, user)        
    else:
        return not user.is_anonymous() and user.has_perm('wiki.admin')

