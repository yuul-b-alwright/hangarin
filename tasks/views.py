from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from .models import Task, Priority, Category
import os
import requests

# --- 0. OAUTH SETUP GUIDE ---
def oauth_setup_view(request, provider):
    current_site = Site.objects.get_current()
    login_url = f'/accounts/{provider}/login/'
    social_app = SocialApp.objects.filter(provider=provider).first()

    if social_app and current_site in social_app.sites.all():
        return redirect(login_url)

    if provider == 'google':
        title = "🔗 Google OAuth Setup"
        instructions = [
            "1. Go to <a href='https://console.cloud.google.com/' target='_blank'>Google Cloud Console</a>",
            "2. Create a new project or select an existing one",
            "3. Enable the 'Google+ API' in the API Library",
            "4. Go to 'Credentials' and create an OAuth 2.0 credential (Web Application)",
            "5. Add 'http://127.0.0.1:8000' to Authorized JavaScript origins",
            "6. Add 'http://127.0.0.1:8000/accounts/google/login/callback/' to Authorized redirect URIs",
            "7. Copy your Client ID and Client Secret",
            "8. Go to Django admin: <a href='/admin/socialaccount/socialapp/' target='_blank'>Admin SocialApp</a>",
            "9. Create a new Social Application with Provider: Google, and paste your credentials"
        ]
    elif provider == 'github':
        title = "🔗 GitHub OAuth Setup"
        instructions = [
            "1. Go to <a href='https://github.com/settings/developers' target='_blank'>GitHub Settings → Developer settings</a>",
            "2. Click 'New OAuth App'",
            "3. Fill in the form:",
            "&nbsp;&nbsp;• Application name: Hangarin",
            "&nbsp;&nbsp;• Homepage URL: http://127.0.0.1:8000",
            "&nbsp;&nbsp;• Authorization callback URL: http://127.0.0.1:8000/accounts/github/login/callback/",
            "4. Copy your Client ID and Client Secret",
            "5. Go to Django admin: <a href='/admin/socialaccount/socialapp/' target='_blank'>Admin SocialApp</a>",
            "6. Create a new Social Application with Provider: GitHub, and paste your credentials"
        ]
    else:
        title = "Invalid Provider"
        instructions = [f'Provider "{provider}" is not supported.']

    if not social_app:
        instructions.append("<strong>Note:</strong> There is currently no Social Application configured for this provider.")
    else:
        instructions.append("<strong>Note:</strong> Your Social Application exists but is not connected to the current site. Open it in admin and add the current site.")

    return render(request, 'tasks/oauth_setup.html', {
        'title': title,
        'instructions': instructions,
        'provider': provider
    })

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

    # Fetch weather data
    api_key = os.getenv("OPENWEATHER_API_KEY")
    weather_data = {}
    if api_key and api_key != "your_openweather_api_key_here":
        try:
            city = "Manila"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": round(data["main"]["temp"]),
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"],
                    "humidity": data["main"]["humidity"],
                }
        except:
            # Show demo weather if API fails
            weather_data = {
                "city": "Manila",
                "country": "PH",
                "temp": 28,
                "description": "Partly Cloudy",
                "icon": "02d",
                "humidity": 75,
                "is_demo": True,
            }
    else:
        # Show demo weather if no API key set
        weather_data = {
            "city": "Manila",
            "country": "PH",
            "temp": 28,
            "description": "Partly Cloudy",
            "icon": "02d",
            "humidity": 75,
            "is_demo": True,
        }

    return render(request, 'tasks/dashboard.html', {
        'tasks': tasks,
        'priorities': Priority.objects.all(), # Sends choices to the dropdown
        'categories': Category.objects.all(), # Sends choices to the dropdown
        'progress_percentage': progress,
        'weather': weather_data,
    })

# --- 5. WEATHER VIEW ---
def weather_view(request):
    """Fetch and display weather data from OpenWeather API"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = request.GET.get("city", "Manila")

    if not api_key or api_key == "your_openweather_api_key_here":
        weather_data = {
            "error": "OpenWeather API key is missing or invalid.",
            "details": "Please set a valid OPENWEATHER_API_KEY value in your .env file."
        }
        return render(request, "tasks/weather.html", {"weather": weather_data, "city": city})

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    weather_data = {}
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
        }
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            weather_data = {
                "error": "Unauthorized: Invalid OpenWeather API key.",
                "details": "Verify your OPENWEATHER_API_KEY in the .env file and restart the server."
            }
        elif response.status_code == 404:
            weather_data = {
                "error": f"Could not find weather information for '{city}'.",
                "details": "Try a different city name."
            }
        else:
            weather_data = {
                "error": "Failed to fetch weather data.",
                "details": str(e),
            }
    except requests.exceptions.RequestException as e:
        weather_data = {
            "error": "Failed to fetch weather data.",
            "details": str(e),
        }
    except KeyError:
        weather_data = {
            "error": f"Could not parse weather information for '{city}'.",
            "details": "The API response format was unexpected."
        }
    
    return render(request, "tasks/weather.html", {"weather": weather_data, "city": city})