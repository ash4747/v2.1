from django.shortcuts import render, redirect
from .models import Tutorial,UserRelationship,UserBlocked
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm,AddFriendForm,DeleteFriendForm,DeleteFriendForm,BlockFriendForm

def contextOfHomepage(error):
    username = user.username
    friendList = friendsOf(username)
    blockList = BeBlockedBy(username)
    context = {'error':error, 'username': username, 'friendList': friendList,'blockList': blockList}
    return context
    
def friendsOf(username):
    friends = UserRelationship.objects.filter(selfname__exact=username)
    friendList = ''
    for friend in friends:
        friendList = friendList + '\n' + '\'' + friend.friendname + '\''
    return friendList

def BeBlockedBy(username):
    friends = UserBlocked.objects.filter(selfname__exact=username)
    friendList = ''
    for friend in friends:
        friendList = friendList + '\n' + '\'' + friend.blockname + '\''
    return friendList
# Create your views here.
def homepage(request):
    username = request.COOKIES.get('username', '')
    friendList = friendsOf(username)
    blockList = BeBlockedBy(username)
    if request.method == 'POST':
        if 'add' in request.POST:
            aff = AddFriendForm(request.POST)
            if aff.is_valid():
                friendWaitToAdd = aff.cleaned_data['friendWaitToAdd']
                isRelationExist = UserRelationship.objects.filter(selfname__exact=username,
                                                                  friendname__exact=friendWaitToAdd)
                isfFiendWaitToAddExist = User.objects.filter(username__exact=friendWaitToAdd)
                if not isfFiendWaitToAddExist:
                    context = {'error': 'friendWaitToAdd is not exist', 'username': username, 'friendList': friendList,
                               'blockList': blockList,"tutorials":Tutorial.objects.all}
                    #context=contextOfHomepage( 'friendWaitToAdd is not exist')
                    return render(request, 'main/home.html', context)
                else:
                    if isRelationExist:
                        context = {'error1': request.method, 'error': 'friendWaitToAdd is  already your friend',
                                   'username': username, 'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
                        return render(request, 'main/home.html', context)
                    else:
                        UserRelationship.objects.create(selfname=username, friendname=friendWaitToAdd)
                        friendList = friendsOf(username)
                        context = {'error': 'done', 'username': username, 'friendList': friendList,
                                   'blockList': blockList,"tutorials":Tutorial.objects.all}
                        return render(request, 'main/home.html', context)
            else:
                context = {'username': username, 'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
                return render(request, 'main/home.html', context)

        elif 'delete' in request.POST:
            dff = DeleteFriendForm(request.POST)
            if dff.is_valid():
                friendWaitToDelete = dff.cleaned_data['friendWaitToDelete']
                isRelationExist = UserRelationship.objects.filter(selfname__exact=username,
                                                                  friendname__exact=friendWaitToDelete)
                isfFiendWaitToDelete = User.objects.filter(username__exact=friendWaitToDelete)
                if not isfFiendWaitToDelete:
                    context = {'error': 'friendWaitToDelete is not exist', 'username': username,
                               'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
                    return render(request, 'main/home.html', context)
                else:
                    if not isRelationExist:
                        context = {'error': 'friendWaitToDelete is not your friend', 'username': username,
                                   'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
                        return render(request, 'main/home.html', context)
                    else:
                        UserRelationship.objects.filter(selfname=username, friendname=friendWaitToDelete).delete()
                        friends = UserRelationship.objects.filter(selfname__exact=username)
                        friendList = ''
                        for friend in friends:
                            friendList = friendList + '\n' + '\'' + friend.friendname + '\''
                        context = {'error': 'done', 'username': username, 'friendList': friendList,
                                   'blockList': blockList,"tutorials":Tutorial.objects.all}
                        return render(request, 'main/home.html', context)
            else:
                context = {'username': username, 'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
                return render(request, 'main/home.html', context)
        elif 'block' in request.POST:
            bff = BlockFriendForm(request.POST)
            if bff.is_valid():
                friendWaitToBlock = bff.cleaned_data['friendWaitToBlock']
                isRelationExist = UserBlocked.objects.filter(selfname__exact=username,
                                                             blockname__exact=friendWaitToBlock)
                isfFiendWaitToBlock = User.objects.filter(username__exact=friendWaitToBlock)
                if not isfFiendWaitToBlock:
                    context = {'error': 'friendWaitToBlock is not exist', 'username': username,
                               'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
                    return render(request, 'main/home.html', context)
                else:
                    if isRelationExist:
                        context = {'error': 'already blocked', 'username': username, 'friendList': friendList,'blockList': blockList,"tutorials":Tutorial.objects.all}
                        return render(request, 'main/home.html', context)
                    else:
                        UserBlocked.objects.create(selfname=username, blockname=friendWaitToBlock)
                        blockList = BeBlockedBy(username)
                        context = {'error': 'done', 'username': username, 'friendList': friendList,
                                   'blockList': blockList,"tutorials":Tutorial.objects.all}
                        return render(request, 'main/home.html', context)
            else:
                context = {'username': username, 'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
                return render(request, 'main/home.html', context)

    else:
        context = {'username': username, 'friendList': friendList, 'blockList': blockList,"tutorials":Tutorial.objects.all}
        return render(request, 'main/home.html', context)


  


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request,"Logged out successfully!")
    return redirect("main:login")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                response=redirect('/homepage')
                response.set_cookie('username', username, 3600)#cookie usename
                return redirect('/homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})
