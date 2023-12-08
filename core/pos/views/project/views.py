from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from import_export import resources
from core.pos.forms import ProductForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import *

class ProjectListView(ValidatePermissionRequiredMixin, ListView):
    model = Project
    template_name = 'project/list.html' 
    permission_required = 'view_project'

    # Código omitido por brevedad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proyectos'
        context['create_url'] = reverse_lazy('project_create') 
        context['list_url'] = reverse_lazy('project_list')
        context['entity'] = 'Proyectos'
        return context


class ProjectCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'address', 'start_date', 'estimated_end_date', 'manager']
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list')
    permission_required = 'add_project'

    # Código omitido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Proyecto' 
        context['entity'] = 'Proyectos'
        context['list_url'] = self.success_url 
        context['action'] = 'add'
        return context

# Vistas Update, Delete similares referenciando Project

class ProjectUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Project 
    fields = ['name', 'address', 'start_date', 'estimated_end_date', 'manager']
    template_name = 'project/create.html'
    success_url = reverse_lazy('project_list')
    permission_required = 'change_project'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # Código omitido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Proyecto'
        context['entity'] = 'Proyectos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProjectDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('project_list')
    permission_required = 'delete_project'  

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # Código omitido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Proyecto' 
        context['entity'] = 'Proyectos'
        context['list_url'] = self.success_url
        return context
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

