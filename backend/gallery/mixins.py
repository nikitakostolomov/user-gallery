from users.models import User


class UserQuerySetMixin:
    def get_queryset(self, *args, **kwargs):
        return User.objects.filter(**{self.lookup_field: self.request.user.pk})
