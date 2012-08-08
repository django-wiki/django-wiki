from django.db import models

# First, define the Manager subclass.
class ActiveObjectsManager(models.Manager):
    def get_query_set(self):
        return super(ActiveObjectsManager, self).get_query_set().filter(current_revision__deleted=False)
