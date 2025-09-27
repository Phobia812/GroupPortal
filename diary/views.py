from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Grade
from .forms import GradeForm

def is_moderator_or_admin(user):
    return user.is_authenticated and (user.is_moderator() or user.is_admin())

@login_required
def grade_list(request):
    user = request.user
    if user.is_admin() or user.is_moderator():
        grades = Grade.objects.all()
    else:
        grades = Grade.objects.filter(student=user)

    return render(request, 'diary/grade_list.html', {'grades': grades})

@login_required
@user_passes_test(is_moderator_or_admin)
def grade_add(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'diary/grade_form.html', {'form': form})

@login_required
@user_passes_test(is_moderator_or_admin)
def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'diary/grade_form.html', {'form': form})

@login_required
@user_passes_test(is_moderator_or_admin)
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grade_list')
    return render(request, 'diary/grade_confirm_delete.html', {'grade': grade})