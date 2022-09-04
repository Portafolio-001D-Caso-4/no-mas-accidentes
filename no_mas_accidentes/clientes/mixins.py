from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class EsClienteMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="cliente").exists()
