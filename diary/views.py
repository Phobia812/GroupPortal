from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Grade
from .forms import GradeForm

class ModeratorOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_moderator() or user.is_admin())

class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'diary/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        user = self.request.user
        if user.is_admin() or user.is_moderator():
            return Grade.objects.all()
        return Grade.objects.filter(student=user)

class GradeCreateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'diary/grade_form.html'
    success_url = reverse_lazy('grade_list')

class GradeUpdateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'diary/grade_form.html'
    success_url = reverse_lazy('grade_list')

class GradeDeleteView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, DeleteView):
    model = Grade
    template_name = 'diary/grade_confirm_delete.html'
    success_url = reverse_lazy('grade_list')
