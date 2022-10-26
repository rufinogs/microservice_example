from django.db.models import Model, UUIDField, CharField, EmailField
import uuid


class User(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=45, blank=False, null=False)
    surname = CharField(max_length=45, blank=False, null=False)
    last_name = CharField(max_length=45, null=True)
    phone = CharField(max_length=45, unique=True)
    email = EmailField(null=True, unique=True)
