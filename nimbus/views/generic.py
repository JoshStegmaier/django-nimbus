from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .mixins import GenerateActionMixin

class DetailViewWithActionStream(GenerateActionMixin, DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.generate_action()
        return super(DetailViewWithActionStream, self).dispatch(request, *args, **kwargs)

    def get_action_actor(self, *args, **kwargs):
        return self.request.user

    def get_action_verb(self, *args, **kwargs):
        return 'viewed'

    def get_action_action_object(self, *args, **kwargs):
        return self.get_object()