from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from import_export import resources
from core.pos.forms import ProductForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Product


class ProductListView(ValidatePermissionRequiredMixin, ListView):
    model = Product
    template_name = 'product/list.html'
    permission_required = 'view_product'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Product.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('product_create')
        context['list_url'] = reverse_lazy('product_list')
        context['entity'] = 'Productos'
        return context


class ProductCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product_list')
    url_redirect = success_url
    permission_required = 'add_product'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Creación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProductUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product_list')
    url_redirect = success_url
    permission_required = 'change_product'

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
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProductDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('product_list')
    url_redirect = success_url
    permission_required = 'delete_product'

    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        return context


""" Aquí está un resumen de lo que hace cada clase:

ProductListView: Muestra una lista de productos. Requiere autenticación de usuario (login_required) y valida los permisos del 

usuario (ValidatePermissionRequiredMixin). La lista de productos se obtiene del modelo Product y se muestra 

en la plantilla 'product/list.html'. También maneja solicitudes POST para realizar una búsqueda de productos y devuelve 

los resultados en formato JSON.

ProductCreateView: Permite crear un nuevo producto. También requiere autenticación y valida los permisos del usuario.

Utiliza el formulario ProductForm para recopilar los datos del producto. Después de una creación exitosa, redirige a la lista de productos.

ProductUpdateView: Permite actualizar un producto existente. Requiere autenticación y valida los permisos del usuario. 

Utiliza el formulario ProductForm para editar los datos del producto. Después de una actualización exitosa, redirige a la lista de productos.

ProductDeleteView: Permite eliminar un producto existente. Requiere autenticación y valida los permisos del usuario. Muestra una confirmación 

de eliminación en la plantilla 'product/delete.html' y, después de una eliminación exitosa, redirige a la lista de productos.

En resumen, este código define vistas que permiten mostrar, crear, actualizar y eliminar productos utilizando formularios y plantillas en Django.

También incluye la validación de permisos de usuario para asegurar que solo los usuarios autorizados puedan realizar estas operaciones. """