class NoDeleteModelAdminMixin:
    def has_delete_permission(self, request, obj=None):
        return False


class NoAddModelAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False


class NoChangeModelAdminMixin:
    def has_change_permission(self, request, obj=None):
        return False


class AddOnlyModelAdminMixin(NoDeleteModelAdminMixin, NoChangeModelAdminMixin):
    pass


class ChangeOnlyModelAdminMixin(NoDeleteModelAdminMixin, NoAddModelAdminMixin):
    pass


class ReadOnlyModelAdminMixin(ChangeOnlyModelAdminMixin, NoChangeModelAdminMixin):
    pass
