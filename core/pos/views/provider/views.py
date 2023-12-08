from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.pos.forms import ProviderForm  # Cambiado de CategoryForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Provider  # Cambiado de Category

class ProviderListView(ValidatePermissionRequiredMixin, ListView):
    model = Provider  # Cambiado de Category
    template_name = 'provider/list.html'  # Cambiado de category/list.html
    permission_required = 'view_provider'  # Cambiado de view_category
    url_redirect = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Provider.objects.all():  # Cambiado de Category.objects.all()
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'  # Cambiado de Categorías
        context['create_url'] = reverse_lazy('provider_create')  # Cambiado de category_create
        context['list_url'] = reverse_lazy('provider_list')  # Cambiado de category_list
        context['entity'] = 'Proveedores'  # Cambiado de Categorias
        return context


class ProviderCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Provider  # Cambiado de Category
    form_class = ProviderForm  # Cambiado de CategoryForm
    template_name = 'provider/create.html'  # Cambiado de category/create.html
    success_url = reverse_lazy('provider_list')  # Cambiado de category_list
    url_redirect = success_url
    permission_required = 'add_provider'  # Cambiado de add_category

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Proveedor'  # Cambiado de una Categoria
        context['entity'] = 'Proveedores'  # Cambiado de Categorias
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProviderUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Provider  # Cambiado de Category
    form_class = ProviderForm  # Cambiado de CategoryForm
    template_name = 'provider/create.html'  # Cambiado de category/create.html
    success_url = reverse_lazy('provider_list')  # Cambiado de category_list
    url_redirect = success_url
    permission_required = 'change_provider'  # Cambiado de change_category

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Proveedor'  # Cambiado de una Categoria
        context['entity'] = 'Proveedores'  # Cambiado de Categorias
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProviderDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Provider  # Cambiado de Category
    template_name = 'provider/delete.html'  # Cambiado de category/delete.html
    success_url = reverse_lazy('provider_list')  # Cambiado de category_list
    url_redirect = success_url
    permission_required = 'delete_provider'  # Cambiado de delete_category

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Proveedor'  # Cambiado de una Categoria
        context['entity'] = 'Proveedores'  # Cambiado de Categorias
        context['list_url'] = self.success_url
        return context
