from django.shortcuts import render
from product.service.product_service import ProductServiceImpl
from django.core.paginator import Paginator

product_service=ProductServiceImpl.get_instance() # 객체 생성
# Create your views here.
def all_product_list_pagination(request):
        # question service로부터 받아옴
        product = product_service.find_all()

        # paging 처리

        #     Page 객체 속성
        #     paginator.count    전체 게시물 개수
        #     paginator.per_page    페이지당 보여줄 게시물 개수
        #     paginator.page_range    페이지 범위 (range객체: range(1, 32))
        #     number    현재 페이지 번호
        #     previous_page_number()    이전 페이지 번호 (현재페이지가 1인 경우,  EmptyPage오류 발생하므로, has_previous 속성을 사용하여 이전 페이지 유무를 확인)
        #     next_page_number()    다음 페이지 번호 (다음페지이 없는 경우, EmptyPage오류 발생하므로, has_next 속성을 사용하여 다음 페이지 유무를 확인)
        #     has_previous    이전 페이지 유무
        #     has_next    다음 페이지 유무
        #     start_index    현재 페이지 시작 인덱스(1부터 시작)
        #     end_index    현재 페이지의 끝 인덱스(1부터 시작)

        page = request.GET.get('page', 1)
        paginator = Paginator(product, 20)  # 한페이지에 몇개씩?
        page_obj = paginator.get_page(page)
        last_page=paginator.num_pages

        return render(request, 'product/product_list.html', context={'page_obj': page_obj,'last_page':last_page})

def product_detail(request,product_id):
        product = product_service.find_by_id(product_id)
        return render(request, 'product/product_detail.html', context={'product':product})


