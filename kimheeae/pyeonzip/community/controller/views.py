from django.shortcuts import render

from community.entity.models import Community, CommunityForm


# Create your views here.
def index(request):
    return render(request,'main.html')

def community_write(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save(
            pass

        print(request.POST)

    return render(request,'community/community_form.html',{'CommunityForm':CommunityForm})