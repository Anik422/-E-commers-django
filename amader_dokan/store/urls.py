from django.urls import path
from store import views

app_name = 'store'
urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    # path('product/<int:prod_id>/',
    #      views.product_details, name='product-details'),
    # path('product/<str:pk>/',
    #      views.ProductViewDetails.as_view(), name='product-details')
    path('product/<str:slug>/',
         views.ProductViewDetails.as_view(), name='product-details'),
    # path('category/<category>/', views.category_view, name='category-view')
]
