from django.views.generic import TemplateView
from product.service.product_service import ProductServiceImpl

product_service = ProductServiceImpl()

class MainPageView(TemplateView):
    template_name = "main.html"  # 사용할 템플릿 지정

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 기본 context 가져오기
        context["latest_product"] = product_service.latest_product() # 모든 제품 데이터를 context에 추가
        context['ai_product']=product_service.ai_product()
        return context  # context 반환