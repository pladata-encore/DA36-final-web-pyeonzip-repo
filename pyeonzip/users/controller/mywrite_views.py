from django.shortcuts import render



def mywrite(request):
    return render(request, 'users/mywrite.html')