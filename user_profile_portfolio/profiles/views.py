from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User, Project
from django.contrib import messages  # For flashing messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Home View: Display all users and projects
def home(request):
    users = User.objects.all()
    projects = Project.objects.all()
    return render(request, 'home.html', {'users': users, 'projects': projects})

# Create User View: Handle user registration
def create_user(request):
    if request.method == 'POST':
        # Validate form data
        username = request.POST['username']
        bio = request.POST['bio']
        skills = request.POST['skills']
        contact = request.POST['contact']

        if username and bio and skills and contact:
            User.objects.create(
                username=username,
                bio=bio,
                skills=skills,
                contact=contact
            )
            messages.success(request, "User created successfully!")
            return redirect('home')
        else:
            messages.error(request, "All fields are required!")
    return render(request, 'create_user.html')

# Showcase Projects View: Handle project showcase submission
def showcase_projects(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            project_name = request.POST['project_name']
            description = request.POST['description']
            image_url = request.POST['image_url']
            link = request.POST['link']
            
            # Validate project data
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
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")
    
    return render(request, 'showcase_projects.html')

# Login User View: Handle user authentication
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Access 'email' instead of 'username'
        password = request.POST.get('password')

        # Authenticate the user using the email
        try:
            user = User.objects.get(email=email)  # Retrieve the user by email
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
    
    return render(request, 'login.html')


# Admin Login View: Handle admin authentication
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Attempt to retrieve the user by email (assuming you are storing email in the username field)
            user = User.objects.get(email=email)
            
            # Authenticate the user with the username and password
            user = authenticate(request, username=user.username, password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')  # Redirect to the admin dashboard
            else:
                messages.error(request, 'Invalid credentials or not an admin.')
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')

    return render(request, 'admin_login.html')

# Admin Dashboard View: Show the admin dashboard after login
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'admin_dashboard.html')
    else:
        return redirect('admin_login')  # Redirect to admin login if not logged in as admin

# Contact Form View: Handle contact form submission
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # You can process the data here, e.g., save to database or send an email
        print(f"Message from {name} ({email}): {message}")
        return HttpResponse("Thank you for contacting us!")
    return render(request, 'contact.html')  # If you have a separate contact template

# Signup View: Render the signup page
def signup_view(request):
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html') 

from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('home')  # Redirect to login page after logout