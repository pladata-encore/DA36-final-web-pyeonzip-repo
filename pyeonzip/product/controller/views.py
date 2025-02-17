from django.shortcuts import render
from product.service.product_service import ProductServiceImpl
from django.core.paginator import Paginator

product_service=ProductServiceImpl.get_instance() # 객체 생성
# Create your views here.
def index(request):
    return render(request,'main.html')

def all_product_list(request):
    product= product_service.find_all()
    return render(request, 'product/all_product_list.html', context={'product':product})