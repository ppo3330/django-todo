from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')
        
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'completed':
        tasks = Task.objects.filter(is_completed=True)
    elif filter_type == 'active':
        tasks = Task.objects.filter(is_completed=False)
    else:
        tasks = Task.objects.all()

    tasks = tasks.order_by('-created_at')

    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'filter': filter_type
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
        if new_title:
            task.title = new_title
            task.save()
            return redirect('task_list')

    return render(request, 'todo/task_edit.html', {'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')