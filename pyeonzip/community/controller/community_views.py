from django.shortcuts import render
from community.entity.models import Community, CommunityForm
from django.contrib.auth.decorators import login_required

def community_list(request):
    communities = Community.objects.all()
    return render(request, 'community/community_list.html', {'communities': communities })

@login_required(login_url='users:login')
def community_write(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community=form.save()
            print("cc",community)
            pass
        else:
            print('form.errors=',form.errors)
    else:
        form = CommunityForm()
    return render(request, 'community/community_form.html', {'CommunityForm': form})