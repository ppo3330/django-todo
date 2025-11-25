from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date
from django.db import models

def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        deadline = request.POST.get("deadline")

        if title:
            Task.objects.create(
                title=title,
                deadline=deadline if deadline else None
            )
        return redirect('task_list')
        
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'completed':
        tasks = Task.objects.filter(is_completed=True)
    elif filter_type == 'active':
        tasks = Task.objects.filter(is_completed=False)
    else:
        tasks = Task.objects.all()

    tasks = tasks.order_by(
        'is_completed',
        models.Case(
            models.When(deadline=None, then=1),
            default=0,
            output_field=models.IntegerField()
        ),
        'deadline'
    )

    today = date.today()

    for t in tasks:
        if t.deadline:
            t.dday = (t.deadline - today).days
        else:
            t.dday = None

    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'filter': filter_type,
        'today': today
    })

def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('task_list')

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        new_title = request.POST.get("title")
        new_deadline = request.POST.get("deadline")

        if new_title:
            task.title = new_title
        
        task.deadline = new_deadline if new_deadline else None
        task.save()
        return redirect('task_list')

    return render(request, 'todo/task_edit.html', {'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')