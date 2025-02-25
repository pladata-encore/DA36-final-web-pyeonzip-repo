from django.shortcuts import render
from product.service.product_service import ProductServiceImpl
from django.db.models import Q
from django.core.paginator import Paginator


product_service=ProductServiceImpl.get_instance() # 객체 생성

def product_search(request):
    query = request.GET.get('q','').strip()  # 검색어 가져오기 (공백 제거)

    if query:
        product_list = product_service.find_by_name(query)  # 검색어 기반으로 제품 검색
    else:
        product_list = product_service.find_all()  # 검색어 없으면 전체 목록 반환

    # 페이지네이션: 한페이지당 10개씩
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 최대 표시할 페이지 번호 수
    max_page_links = 10

    # 현재 페이지 번호
    cuurent_page = page_obj.number

    # 시작 페이지와 끝 페이지 계산
    start_index = ((cuurent_page -1) // max_page_links) * max_page_links + 1
    end_index = start_index + max_page_links
    if end_index > paginator.num_pages:
        end_index = paginator.num_pages + 1

    # 실제 템플릿에서 사용할 페이지 범위
    page_range = range(start_index, end_index)

    context = {
        'page_obj' : page_obj,
        'page_range' : page_range,
        'query' : query,
    }

    return render(request, 'product/product_search.html', context)