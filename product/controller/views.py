from django.shortcuts import render

import users.urls
from product.entity.models import Product
from product.service.product_service import ProductServiceImpl
from django.core.paginator import Paginator
from review.service.review_service import ReviewServiceImpl
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


product_service=ProductServiceImpl.get_instance() # 객체 생성
review_service=ReviewServiceImpl.get_instance()
# Create your views here.

def product_main(request):
    product = product_service.find_all()
    page = request.GET.get('page', 1)
    paginator = Paginator(product, 20)  # 한페이지에 몇개씩?
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages
    return render(request,"product/product_list.html",context={'page_obj': page_obj,'last_page':last_page})


def product_list(request,tab="all"):
    print(tab)
    product = product_service.find_all()
    page = request.GET.get('page', 1)
    paginator = Paginator(product, 20)  # 한페이지에 몇개씩?
    page_obj = paginator.get_page(page)
    last_page=paginator.num_pages

    if tab == 'latest':
        # latest_product_tab에 대한 HTML 조각 렌더링
        product = product_service.latest_product()
        page = request.GET.get('page', 1)
        paginator = Paginator(product, 20)  # 한페이지에 몇개씩?
        page_obj = paginator.get_page(page)
        last_page = paginator.num_pages
        print("product",product)

    elif tab == 'ai':
        pass

    return render(request, 'product/all_product.html',context={'page_obj': page_obj,'last_page':last_page,"tab":tab})




# def all_product_pagination(request):
#         # question service로부터 받아옴
#         product = product_service.find_all()
#         page = request.GET.get('page', 1)
#         paginator = Paginator(product, 20)  # 한페이지에 몇개씩?
#         page_obj = paginator.get_page(page)
#         last_page=paginator.num_pages
#
#         return render(request, 'product/product_list.html', context={'page_obj': page_obj,'last_page':last_page})
#
#
# def latest_product_pagination(request):
#     # question service로부터 받아옴
#     product = product_service.latest_product()
#     page = request.GET.get('page', 1)
#     paginator = Paginator(product, 20)  # 한페이지에 몇개씩?
#     page_obj = paginator.get_page(page)
#     last_page = paginator.num_pages
#
#     return render(request, 'product/all_product.html', context={'page_obj': page_obj, 'last_page': last_page})

def product_detail(request,product_id):
        product = product_service.find_by_id(product_id)
        # 각 product에 대한 리뷰 개수를 함께 조회
        reviews = review_service.find_by_product_id(product_id)
        liked=product.likes.filter(id=request.user.id).exists()
        return render(request, 'product/product_detail.html', context={'product':product,"reviews":reviews,"liked":liked})

@login_required(login_url='users:login')
def product_likes(request, product_id):
    try:
        product,liked = product_service.add_remove_likes(product_id, request.user)
        likes_count = product.likes.count() if hasattr(product, 'likes') else 0

        print('product.likes.count() =', likes_count)
        return JsonResponse({
            'result': 'success',
            'likes_count': likes_count,
            'liked':liked
        })
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        }, status=400)


def filter_products(request,store="ALL"):
    print(store)
    if store == "ALL":
        products = Product.objects.all()  # 전체 상품
    else:
        products = Product.objects.filter(convenient_store_name=store)  # 선택한 편의점의 상품만 필터링

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 20)  # 한페이지에 몇개씩?
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages
    # product_list = [
    #     {
    #         "id": product.product_id,
    #         "name": product.product_name,
    #         "price": product.product_price,
    #         "store": product.convenient_store_name,
    #         "image": product.product_image_url if product.product_image_url else "/static/images/logo.png",
    #         "likes": product.likes.count(),
    #         "reviews": product.Product_reviews.count(),
    #     }
    #     for product in page_obj
    # ]
    #
    # data = {
    #     "products": product_list,  # 상품 리스트
    #     "total_pages": paginator.num_pages,  # 총 페이지 수
    #     "current_page": page_obj.number,  # 현재 페이지
    # }
    # return JsonResponse(products)
    #
    return render(request, 'product/filter_page_list.html', context={'page_obj': page_obj,'last_page':last_page,"store":store})
