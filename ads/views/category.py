import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = Category.objects.create(name=data.get('name'))
        return JsonResponse({'id': category.id, 'name': category.name})


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{'id': category.id, 'name': category.name
                              } for category in self.object_list], safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({'id': category.id, 'name': category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get('name')
        self.object.save()
        return JsonResponse({'id': self.object.id, 'name': self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({'id': category.id})
