from wiki.conf import settings

# Article settings.
def can_assign(article, user):
    return not user.is_anonymous() and settings.CAN_ASSIGN(article, user)
def can_assign_owner(article, user):
    return not user.is_anonymous() and settings.CAN_ASSIGN_OWNER(article, user)
def can_change_permissions(article, user):
    return not user.is_anonymous() and settings.CAN_CHANGE_PERMISSIONS(article, user)
def can_delete(article, user):
    return not user.is_anonymous() and settings.CAN_DELETE(article, user)
def can_moderate(article, user):
    return not user.is_anonymous() and settings.CAN_MODERATE(article, user)
def can_admin(article, user):
    return not user.is_anonymous() and settings.CAN_ADMIN(article, user)
