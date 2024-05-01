from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from django.http import JsonResponse
from django.shortcuts import redirect

class ProductListView(View):
    template_name = 'product_list.html'

    def get(self, request):
        return render(request, self.template_name, {})

class ProductListJson(BaseDatatableView):
    model = Product
    columns = ['id', 'title', 'category', 'price']
    order_columns = columns

    def filter_queryset(self, qs):
        search_title = self.request.GET.get('search[value]', None)
        if search_title:
            qs = qs.filter(title__icontains=search_title)
        return qs

    def get_initial_queryset(self):
        return Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        return super(ProductListJson, self).get_context_data(*args, **kwargs)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            return redirect('product_list')
        return self.form_invalid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
