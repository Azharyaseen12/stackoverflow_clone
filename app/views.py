from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages

# Create your views here.


@login_required(login_url='login')
def delete_question(request, id):
    user = request.user
    question = get_object_or_404(Questions, pk = id)
    if question.user.id == user.id:
        question.delete()
        return redirect('home')
    else:
        return HttpResponse("you cannot delete this post")            

@login_required(login_url='login')
def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        results = Questions.objects.filter(title__icontains=search)
        
        return render(request , 'app/search_results.html',{'results':results})
        
    

@login_required(login_url='login')
def update_profile(request,id):     
    user = get_object_or_404(User, pk= id) 
    user_profile = User_profile.objects.get(user=user.id)
    if request.method == 'POST':
        new_bio = request.POST.get('bio')    
        new_phone = request.POST.get('phone')   
        new_image = request.FILES.get('image') if 'image' in request.FILES else None
        user_profile.bio = new_bio
        user_profile.phone = new_phone
        user_profile.image = new_image
        user_profile.save()    
        return redirect('profile',user.id)

    return render(request , 'app/update_profile.html')

@login_required(login_url='login')
def create_profile(request,id): 
    user = request.user
    if request.method == 'POST':
        bio = request.POST.get('bio')    
        phone = request.POST.get('phone')   
        image = request.FILES.get('image') if 'image' in request.FILES else None
        user_profile = User_profile.objects.create(
            user=request.user,
            bio=bio,
            phone=phone,
            image=image
        )
        return redirect('profile',id)

    return render(request , 'app/createprofile.html')


@login_required(login_url='login')
def profile(request, id): 
    user = get_object_or_404(User, pk= id)
    user_profile = User_profile.objects.filter(user=user.id)
    question_asked = Questions.objects.filter(user=user.id).order_by('-date_created')[:5]
    answers = Comment.objects.filter(name=user)
        
    return render(request , 'app/profile.html',{'profile':user_profile,'question_asked':question_asked,'answers':answers})
    
@login_required(login_url='login')
def detail(request, question_id):    
    question = get_object_or_404(Questions, pk= question_id)
    answer = Comment.objects.filter(question=question.id)
    return render(request, 'app/question_detail.html' ,{'question':question, 'answer':answer})

@login_required(login_url='login')
def answer(request, question_id):
    question = get_object_or_404(Questions, pk= question_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        my_answer = Comment(name=name,content=content,question=question)
        my_answer.save()
        return redirect('detail',question.id)
    return render(request, 'app/answer.html')

@login_required(login_url='login')
def like(request, question_id):
    question = get_object_or_404(Questions, pk= question_id)    
    user = request.user
    if request.method == 'GET':
        if question.likes.filter(pk = user.id).exists():
            question.likes.remove(user)
            question.save()
            liked = False
            return redirect('detail',question.id)
            
        else:
            question.likes.add(user)
            question.save()
            liked = True
        return redirect('detail',question.id)
        

@login_required(login_url='login')
def ask_question(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = request.user
        post_question = Questions(title=title, content=content, user=user)
        post_question.save()
        return redirect('home')
          
    return render(request, 'app/ask_question.html')
    
@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact_form = Contact(name=name,email=email,subject=subject,message=message)
        contact_form.save()
    return render(request, 'app/contact.html')

@login_required(login_url='login')
def questions(request):   
    question = Questions.objects.all().order_by('-date_created')    
    
    return render (request,'app/questions.html', { 'question':question }) 

@login_required(login_url='login')
def HomePage(request):   
    question = Questions.objects.all().order_by('-date_created')    
    
    return render (request,'app/home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        

    return render (request,'app/signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
           messages.error(request, "invalid credentials")
            


    return render (request,'app/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')