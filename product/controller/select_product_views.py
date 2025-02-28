from django.shortcuts import render
from product.service.product_service import ProductServiceImpl

product_service=ProductServiceImpl.get_instance() # 객체 생성

def select_product_list(request):
    query = request.GET.get("q", "").strip()  # 검색어 가져오기 (공백 제거)

    if query:
        product = product_service.find_by_name(query)  # 검색어 기반으로 제품 검색
    else:
        product = product_service.find_all()  # 검색어 없으면 전체 목록 반환

    return render(request, 'product/select_product_popup.html', context={'product':product, 'query':query})