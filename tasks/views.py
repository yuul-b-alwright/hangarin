from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Priority, Category

# --- 1. SIGNUP VIEW ---
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})

# --- 2. LOGIN VIEW ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

# --- 3. LOGOUT VIEW ---
def logout_view(request):
    logout(request)
    return redirect('login')

# --- 4. DASHBOARD VIEW ---
@login_required
def dashboard(request):
    if request.method == 'POST':
        if 'add_task' in request.POST:
            title = request.POST.get('title')
            deadline = request.POST.get('deadline')
            p_id = request.POST.get('priority')
            c_id = request.POST.get('category')
            
            # Integrity check: only save if all fields are selected
            if title and deadline and p_id and c_id:
                Task.objects.create(
                    user=request.user,
                    title=title,
                    deadline=deadline,
                    priority_id=p_id,
                    category_id=c_id
                )
        
        elif 'delete_id' in request.POST:
            get_object_or_404(Task, id=request.POST.get('delete_id'), user=request.user).delete()
        
        elif 'toggle_id' in request.POST:
            task = get_object_or_404(Task, id=request.POST.get('toggle_id'), user=request.user)
            task.is_completed = not task.is_completed
            task.save()
            
        return redirect('dashboard')

    # GET DATA
    tasks = Task.objects.filter(user=request.user).order_by('is_completed', 'deadline')
    
    # Calculate Progress
    total = tasks.count()
    completed = tasks.filter(is_completed=True).count()
    progress = (completed / total * 100) if total > 0 else 0

    return render(request, 'tasks/dashboard.html', {
        'tasks': tasks,
        'priorities': Priority.objects.all(), # Sends choices to the dropdown
        'categories': Category.objects.all(), # Sends choices to the dropdown
        'progress_percentage': progress,
    })