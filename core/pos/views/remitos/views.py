# ESTAS CLASES SON AGREGADAS A URL
import json
import os
from core.pos.forms import RemitoForm, ClientForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Remito, Product, RemitoProduct, Client, Sale, SaleProduct
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.pos.mixins import ExistsCompanyMixin
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DeleteView, UpdateView, View
from weasyprint import HTML, CSS

from core.pos.forms import RemitoForm, ClientForm, SaleForm
from core.pos.mixins import ValidatePermissionRequiredMixin, ExistsCompanyMixin
from core.reports.forms import ReportForm


class RemitoListView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'remitos/list.html'
    permission_required = 'view_remitos'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Remito.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(
                        date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_products_detail':
                data = []
                for i in RemitoProduct.objects.filter(remito_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Remitos'
        context['create_url'] = reverse_lazy('remitos_create')
        context['list_url'] = reverse_lazy('remitos_list')
        context['entity'] = 'Remitos'
        return context


class RemitoCreateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'remitos/create.html'
    success_url = reverse_lazy('sale_list')
    url_redirect = success_url
    permission_required = 'add_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(
                    name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    sale = Sale()
                    sale.date_joined = request.POST['date_joined']
                    sale.client_id = int(request.POST['client'])
                    sale.iva = float(request.POST['iva'])
                    sale.save()
                    for i in products:
                        detail = SaleProduct()
                        detail.sale_id = sale.id
                        detail.product_id = int(i['id'])
                        detail.cant = int(i['cant'])
                        detail.price = float(i['pvp'])
                        detail.subtotal = detail.cant * detail.price
                        detail.save()
                        detail.product.stock -= detail.cant
                        detail.product.save()
                    sale.calculate_invoice()
                    data = {'id': sale.id}
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(names__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    form = ClientForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear remitos'
        context['entity'] = 'Remitos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        context['frmClient'] = ClientForm()
        
        return context


class RemitoDeleteView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Remito
    template_name = 'remitos/delete.html'
    success_url = reverse_lazy('remitos_list')
    url_redirect = success_url
    permission_required = 'delete_remitos'

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
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class RemitoInvoicePdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('remitos/invoice.html')
            context = {
                'remitos': Remito.objects.get(pk=self.kwargs['pk']),
                'icon': f'{settings.MEDIA_URL}logo.png'
            }
            html = template.render(context)
            css_url = os.path.join(
                settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('remitos_list'))


class RemitoInvoicePdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('remitos/invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'icon': f'{settings.MEDIA_URL}logo.png'
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('remitos_list'))


class RemitoUpdateView(ExistsCompanyMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Remito
    form_class = RemitoForm
    template_name = 'remitos/create.html'
    success_url = reverse_lazy('remitos_list')
    url_redirect = success_url
    permission_required = 'change_sale'

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = RemitoForm(instance=instance)
        form.fields['client'].queryset = Client.objects.filter(
            id=instance.client.id)
        return form

    def get_details_product(self):
        data = []
        remitos = self.get_object()
        for i in remitos.remitosproduct_set.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            data.append(item)
        return json.dumps(data)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.name
                    # item['text'] = i.name
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(
                    name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    with transaction.atomic():
                        products = json.loads(request.POST['products'])
                        remitos = self.get_object()
                        remitos.date_joined = request.POST['date_joined']
                        remitos.client_id = int(request.POST['client'])
                        remitos.iva = float(request.POST['iva'])
                        remitos.save()
                        remitos.saleproduct_set.all().delete()
                        for i in products:
                            detail = RemitoProduct()
                            detail.remitos_id = remitos.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])
                            detail.price = float(i['pvp'])
                            detail.subtotal = detail.cant * detail.price
                            detail.save()
                            detail.product.stock -= detail.cant
                            detail.product.save()
                        remitos.calculate_invoice()
                        data = {'id': remitos.id}
                    data = {'id': remitos.id}
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                clients = Client.objects.filter(
                    Q(names__icontains=term) | Q(dni__icontains=term))[0:10]
                for i in clients:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_client':
                with transaction.atomic():
                    form = ClientForm(request.POST)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        context['frmClient'] = ClientForm()
        return context

    model = Remito
    template_name = 'remitos/delete.html'
    success_url = reverse_lazy('remitos_list')
    permission_required = 'delete_remitos'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            self.object.delete()
            data['success'] = 'Remito eliminado exitosamente.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
