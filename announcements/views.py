from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm


class ModeratorOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_moderator() or user.is_admin())
    
class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'

class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'announcement'

class AnnouncementCreateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    success_url = '/announcements/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Оголошення успішно створено!')
        return super().form_valid(form)
    
class AnnouncementUpdateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_form.html'
    success_url = '/announcements/'

    def form_valid(self, form):
        messages.success(self.request, 'Оголошення успішно оновлено!')
        return super().form_valid(form)

class AnnouncementDeleteView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'announcements/announcement_confirm_delete.html'
    success_url = '/announcements/'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Оголошення успішно видалено!')
        return super().delete(request, *args, **kwargs)

class AnnouncementJsonView(LoginRequiredMixin, ListView):
    model = Announcement

    def render_to_response(self, context, **response_kwargs):
        announcements = list(
            self.get_queryset().values(
                'id', 
                'title', 
                'description', 
                'created_at',
                'updated_at'
            )
        )
        return JsonResponse(announcements, safe=False)