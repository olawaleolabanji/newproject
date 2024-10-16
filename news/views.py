from django.shortcuts import render, redirect, reverse
from news.models import Blog, Comment, Contact
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import re
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.

def homepage(request):
    all_products = ['Luxury Bags', 'Shoes', 'Jeweries']
    context = {"product": all_products}
    return render (request, 'app/index.html', context)
    
@login_required
def news(request):
    return render(request, 'app/news.html')

def welcome(request, name):
    context = {"person": name}
    return render(request, "app/path.html", context)

# @login_required
# def blogs(request):
    # all_blogs = Blog.objects.all().order_by("-Created_at")[:20]
    # context = {'blogs': all_blogs}
    # return render(request, 'app/blog.html', context)

@login_required
def blogs(request):
    user = request.user
    my_blogs = Blog.objects.filter(owner=user).order_by('-Created_at')
    other_blogs = Blog.objects.all().exclude(owner=user).order_by("-Created_at")
    context = {'my_blogs': my_blogs, "other_blogs": other_blogs}
    return render(request, "app/blog.html", context)

@login_required
def read(request, id):
    user = request.user
    single_blog = Blog.objects.filter(id=id).first()
    if not single_blog:
        messages.error(request, 'Invalid blog')
        return redirect (blogs)
    if request.method == 'POST':
        body = request.POST.get('comment')
        if not body:
            messages.error(request, 'comment can not be empty')
            return redirect(reverse('read', kwargs ={'id':id}))
        Comment.objects.create(
            owner = user,
            blog = single_blog,
            body = body
        )
        return redirect(reverse('read', kwargs ={'id':id}))
    blog_comments = Comment.objects.filter(blog=single_blog).order_by ('-created_at')
    context = {'blog': single_blog, "comments":blog_comments}
    return render (request, 'app/read.html' , context)

@login_required
def delete (request, id):
    user = request.user
    sub_blog = Blog.objects.filter(id=id).first()
    if not sub_blog:
        messages.error(request, 'Invalid blog')
        return redirect (blogs)
    if sub_blog.owner != user and not user.is_staff:
        messages.error(request, "Unauthorise access")
        return redirect (blog)
    sub_blog.delete ()
    messages.success(request, "Blog deleted successfully")
    return redirect (blogs)

@login_required
def create (request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get("title")
        body = request.POST.get ('body')
        image = request.FILES.get ('image')
        des = request.POST.get ('description')
        if not title or not body or not image:
            messages.error(request, 'Fill the required field')
            return redirect(create)
        if len(title) >250:
            messages.error(request, "title too long")
            return redirect(create)
        Blog.objects.create (
            title = title,
            body = body,
            image = image,
            description = des,
            owner = user,
        )
        messages.success(request, "Blog created successful")
        return redirect (homepage)
        
    return render (request, 'app/user.html')

@login_required
def edit(request, id):
    user = request.user
    single_blog = Blog.objects.filter(id=id).first()
    if not single_blog:
        messages.error(request, 'Invalid blog')
        return redirect (blogs)
    if single_blog.owner != user:
        messages.error(request, "Unauthorised access")
        return redirect(blogs)
    context = {"blog": single_blog}
    if request.method=="POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        description = request.POST.get("description")
        image = request.POST.get("image")
        if not title or not body:
            messages.error(request, 'Invalid blog')
            return redirect(edit)
        if len(title) >250:
            messages.error(request, "title too long")
            return redirect(blogs)
        single_blog.title = title
        single_blog.body = body
        single_blog.description = description
        if image:
            single_blog.image = image
        single_blog.save()
        messages.success(request, 'Blog Edited successful')
        return redirect (homepage)
    return render(request, "app/edit.html", context)


def strong_password(password):
    """
    Validate strong password:
    - Length: 8-128 characters
    - Uppercase letter (A-Z)
    - Lowercase letter (a-z)
    - Digit (0-9)
    - Special character (!, @, #, $, etc.)
    """
    pattern = r"^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%#?&])[A-Za-z\d@$!%#?&]{8,128}$"
    return bool(re.match(pattern, password))

def signup (request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if not username or not email or not password or not cpassword:
            messages.error(request, "All field are required")
            return redirect(signup)
        if password != cpassword:
            messages.error(request, "password not desame")
            return redirect(signup)
        if len(password) < 8:
            messages.error(request, "maximum length required")
            return redirect(signup)
        if not strong_password(password):
            messages.error(request, "Password must contain at least one uppercase, lowercase, number and a special character")
            return redirect(signup)
        if len(username) < 5:
            messages.error(request, "maximum length required")
            return redirect(signup)
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            messages.error(request, 'User already exist')
            return redirect(signup)
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            messages.error(request, "Email already exists")
            return redirect(signup)
        user = User.objects.create(
            username = username,
            email = email,
            first_name = firstname,
            last_name = lastname,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Signed up successfully")
        return redirect(homepage)
        
    return render(request, 'app/signup.html')


def login (request):
    if request.user.is_authenticated:
        return redirect(homepage)
    next = request.GET.get('next')
    if request.method == "POST":
        username =request.POST.get("username")
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, "fill your login details")
            return redirect(login)
        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'Invalid login credentials')
            return redirect(login)
        auth.login(request, user)
        return redirect(next or homepage)

    return render(request, "app/login.html")

def logout(request):
    auth.logout(request)
    return redirect(login)

def contact (request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if not name or not email or not message:
            message.error(request, 'All field require')
            return redirect(contact)
        send_email = EmailMessage(
            subject = "Thank you for reaching out to us ",
            body = f"HELLO {name},\n\nWe have recieve your message,\n\n One of our staff will contant you in 24hrs\n\nSigned\nCEO",
            from_email = settings.EMAIL_HOST_USER,
            to = [email]
        )
        send_email.send()
        
        new_contact = Contact.objects.create(
            name = name,
            email = email,
            message = message,
        )
        send_email = EmailMessage(
            subject = "New contact us message",
            body = f"someone filled the form with the following details:\n\nName:{name}\n\nEmail:{email}\n\n\tMessage:{message}",
            from_email = settings.EMAIL_HOST_USER,
            to = ['olazdengineer@gmail.com']
        )
        send_email.send()
        messages.success(request, "message sent successfully")
        return redirect(homepage)

    return render(request, "app/contact.html")