from django.contrib.auth.models import Group

def user_in_group(user, group_name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

def is_admin(user) -> bool:
    return user.is_authenticated and (
        user.is_staff or user.is_superuser or user_in_group(user, "Administrador")
    )

def is_socio(user) -> bool:
    return user_in_group(user, "Socio")
