from django.urls import path

from ads.views.category import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView

urlpatterns = [
    path('', CategoryListView.as_view(), name='all_category'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('create/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/update/', CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', CategoryDeleteView.as_view()),
]
