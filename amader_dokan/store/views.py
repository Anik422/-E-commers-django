from multiprocessing import context
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# product models
from store.models import Product, Category, ProductImages

# Product views


class HomeListView(ListView):
    model = Product
    template_name = 'home/index.html'
    context_object_name = 'products'

    def build_page_title(self):
        return 'PHONE KINBO'

# def home(request):
#     context = {
#         'title': 'PHONE KINBO'
#     }
#     return render(request, 'home/index.html', context)


# Product detail function views
# def product_details(request, prod_id):
#     item = Product.objects.get(id=prod_id)
#     photos = ProductImages.object.filter(product=item).order_by('-created')
#     similar_item = Product.objects.filter(category=item.category)
#     context = {
#         'item': item,
#         'similar_item': similar_item,
#         'photos': photos
#     }
#     return render(request, 'home/product.html', context)


# Product detail class base views
class ProductViewDetails(DetailView):
    model = Product
    template_name = 'home/product.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_images'] = ProductImages.objects.filter(
            product=self.object.id)
        context['similar_item'] = Product.objects.filter(
            category=self.object.category)
        return context
