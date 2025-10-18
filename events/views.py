from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Event
from .forms import EventForm


class ModeratorOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_moderator() or user.is_admin())
    
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = '/events/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class EventUpdateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = '/events/'

class EventDeleteView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = '/events/'

class EventJsonView(LoginRequiredMixin, ListView):
    model = Event

    def render_to_response(self, context, **response_kwargs):
        from django.http import JsonResponse
        events = list(context['events'].values('id', 'title', 'description', 'start_date', 'end_date', 'location'))
        return JsonResponse(events, safe=False)
    