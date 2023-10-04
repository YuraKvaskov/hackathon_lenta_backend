from django.db import models
from django.contrib.auth import get_user_model

from api.v1.models import Store

User = get_user_model()


class UserStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.store.st_id}"