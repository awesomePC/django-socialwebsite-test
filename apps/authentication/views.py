# from django.shortcuts import render, redirect
# from django.contrib.auth import login, update_session_auth_hash, logout
# # from .forms import LoginForm, SignUpForm
# from django.template import loader
# from django.http import HttpResponse
# # Create your views here.
# def login_view(request):
    
#     # if request.method == 'POST':
#     #     form = LoginForm(data = request.POST)
#     #     if form.is_valid():
#     #         user = form.get_user()
#     #         login(request, user)
#     #         return redirect('/profile')
#     # else:
#     #     form = LoginForm()
#     temp = request.method
#     print(request)
#     print(2222)
#     return render(request, 'accounts/index.html')
    
#     # template = loader.get_template('accounts/index.html')
#     # HttpResponse(template.render())
#     # HttpResponse("hello world")




    # Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash, logout

def login_view(request):
    form = LoginForm(request.POST)
    sign = 0
    msg = None
    print(form)
    if request.method == "POST":
        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            print(email, password)
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
        sign = 1
    # return redirect("/profile")
    return render(request, "home/index.html", {"form": form, "msg": msg, "sign": sign})

def register_user(request):
    sign = 0
    if request.method == 'POST':
        print(123)
        form = SignUpForm(request.POST )
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    sign = 2
    return render(request, 'home/index.html', {'form': form, 'sign': sign})

@login_required(login_url="/login")
def logoutView(request):
    logout(request)
    return redirect('/login')