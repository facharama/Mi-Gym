from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def ensure_groups(sender, **kwargs):
    for name in ["Socio", "Administrador"]:
        Group.objects.get_or_create(name=name)
