from django.shortcuts import render
from product.service.product_service import ProductServiceImpl

product_service=ProductServiceImpl.get_instance() # 객체 생성

def select_product_list(request):
    product= product_service.find_all()
    return render(request, 'product/select_product_popup.html', context={'product':product})