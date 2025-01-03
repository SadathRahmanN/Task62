from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User, Project
from django.db import IntegrityError
from django.apps import AppConfig

# Home View: Display all users and projects
def home(request):
    users = User.objects.all()
    projects = Project.objects.all()
    return render(request, 'home.html', {'users': users, 'projects': projects})

# User Registration View
def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if all([username, email, password]):
            try:
                # Check if a user already exists with the same username or email
                if User.objects.filter(username=username).exists():
                    messages.error(request, "User with this username already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "A user with this email already exists.")
                else:
                    user = User.objects.create(
                        username=username,
                        email=email,
                    )
                    user.set_password(password)  # Hash the password
                    user.save()
                    messages.success(request, "User created successfully!")
                    # Login the user automatically after creating the account
                    login(request, user)
                    return redirect('dashboard')  # Redirect to dashboard after login
            except IntegrityError:
                messages.error(request, "Error creating user, please try again.")
        else:
            messages.error(request, "All fields are required!")
    return render(request, 'home.html')

# Showcase Projects View
def showcase_projects(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        image_url = request.POST.get('image_url')
        link = request.POST.get('link')

        user = get_object_or_404(User, username=username)
        if project_name and description:
            Project.objects.create(
                user=user,
                name=project_name,
                description=description,
                image_url=image_url,
                link=link
            )
            messages.success(request, "Project showcased successfully!")
            return redirect('home')
        else:
            messages.error(request, "Project name and description are required!")
    return render(request, 'showcase_projects.html')

# Login View
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    return render(request, 'login.html')

# Admin Login View
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid credentials or not an admin.")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    return render(request, 'admin_login.html')

# Admin Dashboard View
@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin_dashboard.html')
    return redirect('admin_login')

# Contact Form View
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process form data (save, send email, etc.)
        print(f"Message from {name} ({email}): {message}")
        return HttpResponse("Thank you for contacting us!")
    return render(request, 'contact.html')


# User Dashboard View
@login_required
def dashboard(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        image_url = request.POST.get("image_url", "")
        link = request.POST.get("link")

        if all([name, description, link]):
            Project.objects.create(
                user=request.user,
                name=name,
                description=description,
                image_url=image_url,
                link=link
            )
            messages.success(request, "Project uploaded successfully!")
        else:
            messages.error(request, "Please fill in all required fields.")
        return redirect("dashboard")

    projects = Project.objects.filter(user=request.user)
    return render(request, "dashboard.html", {"user": request.user, "projects": projects})

# Logout View
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# Upload Project via AJAX
@login_required
def upload_project(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        image_url = request.POST.get("image_url", "")
        link = request.POST.get("link")

        if all([name, description, link]):
            project = Project.objects.create(
                user=request.user,
                name=name,
                description=description,
                image_url=image_url,
                link=link
            )
            return JsonResponse({
                "message": "Project uploaded successfully!",
                "project": {
                    "name": project.name,
                    "description": project.description,
                    "image_url": project.image_url,
                    "link": project.link,
                }
            }, status=201)
        return JsonResponse({"error": "Missing required fields."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# Showcase View
def showcase(request):
    projects = Project.objects.all()
    return render(request, 'showcase.html', {'projects': projects})


class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import profiles.signals  # Make sure to include any signals if needed
