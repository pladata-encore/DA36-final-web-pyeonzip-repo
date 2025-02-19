from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from community.entity.models import CommunityForm
from community.service.community_service import CommunityServiceImpl

community_service = CommunityServiceImpl()

def community_list(request):
    communities = community_service.find_all()
    return render(request, 'community/community_list.html', {'communities': communities })

@login_required(login_url='users:login')
def community_write(request):
    if request.method == 'POST':
        return redirect("community:community_save") # 🔹 폼이 제출되면 community_save로 이동
    else:
        form = CommunityForm()
        return render(request, 'community/community_form.html', {'CommunityForm': form})

def community_save(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)

        if form.is_valid():
            products = form.cleaned_data['products']
            product_ids = [product.product_id for product in products]

            community_service.create_community(form.cleaned_data, product_ids)
            return redirect("community:community_list")

        else:
            print('form.errors=', form.errors)

    return redirect("community:community_write")