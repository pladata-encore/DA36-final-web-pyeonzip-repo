from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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

def main(request,tab="ALL"):
    page = request.GET.get('page', 1)

    products = product_service.find_all()

    if tab == 'LATEST':
        products = product_service.latest_product()

    elif tab=="AI":
        products=product_service.ai_product().order_by('-updated_at')
        products=product_service.ai_score_count(products)

    paginator = Paginator(products, 20)
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages

    return render(request,'product/product_list.html',context={'page_obj': page_obj,'last_page':last_page,'tab':tab})

def filter_products(request,store="ALL",category="ALL",tab="ALL",page=1):
    page = request.GET.get('page', page)
    products = product_service.find_all()

    if tab == "LATEST":
        products=product_service.latest_product()

    elif tab == "AI":
        products=product_service.ai_product()

    if category=="ALL":
        if store == "ALL":
            pass

        else:
            products =products.filter(convenient_store_name=store)  # 선택한 편의점의 상품만 필터링
    else:
        products = products.filter(Q(convenient_store_name__icontains=store) & Q(product_category_name__icontains=category))

    if tab=="AI":
        products=product_service.ai_score_count(products)

    paginator = Paginator(products, 20)  # 한페이지에 몇개씩?
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages

    return render(request, 'product/filter_product.html', context={'page_obj': page_obj,'last_page':last_page,"store":store,"category":category,"page":page ,"tab":tab})

def product_detail(request,product_id):
        product = product_service.find_by_id(product_id)
        # 각 product에 대한 리뷰 개수를 함께 조회
        reviews = review_service.find_by_product_id(product_id).prefetch_related('reviewrecommender_set')
        # 각 리뷰의 좋아요 개수를 계산해서 추가
        for review in reviews:
            review.recommender_count = review.reviewrecommender_set.count()
            review.recommended=review.recommender.filter(id=request.user.id).exists()
        # 각 상품의 좋아요 조회
        liked=product.likes.filter(id=request.user.id).exists()
        # ai 맛, 가격 점수 조회
        price_score = product.price_score
        taste_score = product.taste_score
        return render(request, 'product/product_detail.html', context={'product':product,"reviews":reviews,"liked":liked, "price_score":price_score,"taste_score":taste_score})

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


def get_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    data = {
        "id": product.product_id,
        "name": product.product_name,
        "image_url": product.product_image_url,
        "price": product.product_price,
        "store": product.convenient_store_name,
        "category": product.product_category_name
    }
    return JsonResponse(data)

