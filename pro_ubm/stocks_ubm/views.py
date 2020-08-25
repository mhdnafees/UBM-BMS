from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DetailView,View
from .models import Stock,SalesRegistry,PurchaseRegistry,ProfitGen
from .models import ProfitGen as progeneration
from .models import InvoiceGen as invoicegeneration
from .forms import AddProductForm,UpdateProductForm,StockInForm,StockOutForm,StockOutFormset,StockInFormset,ProfitGenForm,ProfitGenFormset,InvoiceGenForm,InvoiceGenFormset
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.timezone import localdate
from datetime import datetime, timedelta, time, date

from django.db.models import Sum, Count, F, DecimalField, IntegerField

from rest_framework.views import APIView
from rest_framework.response import Response

from decimal import Decimal


# Create your views here.


class CustomMixin(object):

    def get_context_data(self, **kwargs):
        todaydate = localdate()
        yesterday = todaydate - timedelta(1)
        l_month = todaydate - timedelta(30)
        context = super(CustomMixin, self).get_context_data(**kwargs)
        #  Stock Page #
        context['stock_list'] = Stock.objects.all().order_by('product_name')
        context['lowstock'] = Stock.objects.all().filter(sstock__sold_date__month__exact=l_month.month, sstock__num_of_items__gte=1, stock_available__lte=2).distinct().order_by('stock_available')
        context['lowstockall'] = Stock.objects.all().filter(stock_available__lte=2).order_by('stock_available')
        #  Index Page #
        context['totalprofit'] = SalesRegistry.objects.aggregate(total_profit=Sum('item_profit'))
        context['stockvalue'] = Stock.objects.aggregate(stock_value=Sum(F('landing_cost')*F('stock_available'), output_field=DecimalField()))
        context['lmonthprofit'] = SalesRegistry.objects.filter(sold_date__month__exact=l_month.month, sold_date__year__exact=l_month.year).aggregate(lmonth_profit=Sum('item_profit'))
        context['yesterdayprofit'] = SalesRegistry.objects.filter(sold_date__day__exact=yesterday.day, sold_date__year__exact=yesterday.year, sold_date__month__exact=yesterday.month ).aggregate(yesterday_profit=Sum('item_profit'))
        context['cmonthprofit'] = SalesRegistry.objects.filter(sold_date__month__exact=todaydate.month, sold_date__year__exact=todaydate.year).aggregate(cmonth_profit=Sum(('item_profit'), output_field=IntegerField()))
        context['cyearprofit'] = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year).aggregate(cyear_profit=Sum(('item_profit'), output_field=IntegerField()))
        #  Sales Register Page #
        context['sales_list'] = SalesRegistry.objects.all().order_by('-sold_date')
        #  Purchase Register Page #
        context['purchase_list'] = PurchaseRegistry.objects.all().order_by('-purchased_date')
        #  Profit Gen Page #
        context['profitgenlist'] = progeneration.objects.all().order_by('stock')
        context['profitgenprofit'] = progeneration.objects.all().aggregate(total=Sum('profit'))
        context['profitgendiscount'] = progeneration.objects.all().aggregate(total=Sum('discount'))
        context['profitgenqty'] = progeneration.objects.all().aggregate(total=Sum('qty'))
        context['profitgentotal'] =  progeneration.objects.all().aggregate(total=Sum(F('sold_price')*F('qty'),output_field=DecimalField()))
        #  Invoice Gen Page #
        context['invoicegenlist'] = invoicegeneration.objects.all().order_by('id')
        context['invoicegengrandtotal'] = invoicegeneration.objects.all().aggregate(total=Sum('price'))
        #  Todays stats Page #
        context['salestoday_list'] = SalesRegistry.objects.all().filter(sold_date__exact=todaydate).order_by('-sold_date')
        context['purchasetoday_list'] = PurchaseRegistry.objects.all().filter(purchased_date__exact=todaydate).order_by('-purchased_date')
        context['salestoday_totalsales'] = SalesRegistry.objects.all().filter(sold_date__exact=todaydate).aggregate(totalsales=Sum(F('sold_price')*F('num_of_items'),output_field=DecimalField()),profit=Sum('item_profit'),totalunits=Sum('num_of_items'))
        context['salesmosttoday_list'] = SalesRegistry.objects.all().filter(sold_date__exact=todaydate).order_by('-num_of_items')[:5]
        return context

class index(CustomMixin,ListView):

    template_name = 'stocks_ubm/index.html'
    model = SalesRegistry

class TodayStats(CustomMixin,ListView):


    template_name = 'stocks_ubm/todaystats.html'
    model = SalesRegistry

class TotalStocksAndAddProduct(CustomMixin,CreateView):


    form_class = AddProductForm
    model = Stock
    template_name = 'stocks_ubm/stockandadd.html'

class ProductDetail(DetailView):


    model = Stock

    def get_context_data(self, *args, **kwargs):
        self.objects = self.get_object()
        stock = self.objects
        context = super().get_context_data(**kwargs)
        context['sales_list'] =SalesRegistry.objects.all().filter(stock_name__product_name__exact = stock.product_name).order_by('-sold_date')
        context['total_units'] =SalesRegistry.objects.all().filter(stock_name__product_name__exact = stock.product_name).aggregate(totalunits=Sum('num_of_items'))
        context['purchase_list'] =PurchaseRegistry.objects.all().filter(stock__product_name__exact = stock.product_name).order_by('-purchased_date')
        return context

class UpdateProduct(UpdateView):


    model = Stock
    form_class = UpdateProductForm
    template_name = 'stocks_ubm/update_product.html'

class UpdateProductHTML(ListView):


    model = Stock
    template_name = 'stocks_ubm/update_producthtml.html'

####################################################################
##################### SALES REGISTRY ###############################
####################################################################

class SalesRegister(CustomMixin,ListView):


    model = SalesRegistry
    template_name = 'stocks_ubm/salesregister_list.html'

class StockOut(CreateView):


    model = SalesRegistry
    form_class = StockOutForm
    template_name = 'stocks_ubm/stockout_form.html'

    def get_context_data(self, **kwargs):
        context = super(StockOut, self).get_context_data(**kwargs)
        context['formset'] = StockOutFormset(queryset=SalesRegistry.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        formset = StockOutFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            stock = get_object_or_404(Stock, pk=instance.stock_name.pk)
            sqty = instance.num_of_items
            stock.stock_available -= sqty
            instance.slanding_cost = stock.landing_cost
            stock.save()
            instance.save()
            sale = get_object_or_404(SalesRegistry, pk=instance.pk)
            if instance.num_of_items < 0:
                sale.item_profit = -(stock.landing_cost - instance.sold_price) * instance.num_of_items
            else:
                sale.item_profit = (instance.sold_price - stock.landing_cost) * instance.num_of_items
            sale.save()
        return HttpResponseRedirect('/stockout')

####################################################################
##################### PURCHASE REGISTRY ############################
####################################################################

class StockIn(CreateView):


    model = PurchaseRegistry
    form_class = StockInForm
    template_name = 'stocks_ubm/stockin_form.html'

    def get_context_data(self, **kwargs):
        context = super(StockIn, self).get_context_data(**kwargs)
        context['formset'] = StockInFormset(queryset=PurchaseRegistry.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        formset = StockInFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            stock = get_object_or_404(Stock, pk=instance.stock.pk)
            sqty = instance.num_of_items
            stock.stock_available += sqty
            tempdis = instance.unit_price*Decimal(instance.discount/100)
            tempvatdis = instance.unit_price - tempdis
            instance.updated_landing_cost = tempvatdis + (tempvatdis * Decimal(instance.vat/100))
            stock.landing_cost = instance.updated_landing_cost
            stock.save()
            instance.save()
        return HttpResponseRedirect('/stockin')

class PurchaseRegister(CustomMixin,ListView):


    model = PurchaseRegistry
    template_name = 'stocks_ubm/purchaseregister_list.html'

 # API CHART DATA
class ChartData(APIView):


    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        todaydate = localdate()
        l_month = todaydate - timedelta(30)
        l_year = todaydate - timedelta(365)

        jan = SalesRegistry.objects.filter(sold_date__month__exact=1, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        feb = SalesRegistry.objects.filter(sold_date__month__exact=2, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        march = SalesRegistry.objects.filter(sold_date__month__exact=3, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        april = SalesRegistry.objects.filter(sold_date__month__exact=4, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        may = SalesRegistry.objects.filter(sold_date__month__exact=5, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        june = SalesRegistry.objects.filter(sold_date__month__exact=6, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        july = SalesRegistry.objects.filter(sold_date__month__exact=7, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        aug = SalesRegistry.objects.filter(sold_date__month__exact=8, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        sept = SalesRegistry.objects.filter(sold_date__month__exact=9, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        oct = SalesRegistry.objects.filter(sold_date__month__exact=10, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        nov = SalesRegistry.objects.filter(sold_date__month__exact=11, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        dec = SalesRegistry.objects.filter(sold_date__month__exact=12, sold_date__year__exact=todaydate.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))

        jan_profit = jan['total_profit']
        feb_profit = feb['total_profit']
        march_profit = march['total_profit']
        april_profit = april['total_profit']
        may_profit = may['total_profit']
        june_profit = june['total_profit']
        july_profit = july['total_profit']
        aug_profit = aug['total_profit']
        sept_profit = sept['total_profit']
        oct_profit = oct['total_profit']
        nov_profit = nov['total_profit']
        dec_profit = dec['total_profit']

        janl = SalesRegistry.objects.filter(sold_date__month__exact=1, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        febl = SalesRegistry.objects.filter(sold_date__month__exact=2, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        marchl = SalesRegistry.objects.filter(sold_date__month__exact=3, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        aprill = SalesRegistry.objects.filter(sold_date__month__exact=4, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        mayl = SalesRegistry.objects.filter(sold_date__month__exact=5, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        junel = SalesRegistry.objects.filter(sold_date__month__exact=6, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        julyl = SalesRegistry.objects.filter(sold_date__month__exact=7, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        augl = SalesRegistry.objects.filter(sold_date__month__exact=8, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        septl = SalesRegistry.objects.filter(sold_date__month__exact=9, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        octl = SalesRegistry.objects.filter(sold_date__month__exact=10, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        novl = SalesRegistry.objects.filter(sold_date__month__exact=11, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))
        decl = SalesRegistry.objects.filter(sold_date__month__exact=12, sold_date__year__exact=l_year.year).aggregate(total_profit=Sum(('item_profit'), output_field=IntegerField()))

        jan_profitl = janl['total_profit']
        feb_profitl = febl['total_profit']
        march_profitl = marchl['total_profit']
        april_profitl = aprill['total_profit']
        may_profitl = mayl['total_profit']
        june_profitl = junel['total_profit']
        july_profitl = julyl['total_profit']
        aug_profitl = augl['total_profit']
        sept_profitl = septl['total_profit']
        oct_profitl = octl['total_profit']
        nov_profitl = novl['total_profit']
        dec_profitl = decl['total_profit']

        curmonth = SalesRegistry.objects.filter(sold_date__month__exact=todaydate.month, sold_date__year__exact=todaydate.year).aggregate(tmonth_profit=Sum(('item_profit'), output_field=IntegerField()))
        lasmonth = SalesRegistry.objects.filter(sold_date__month__exact=l_month.month, sold_date__year__exact=l_month.year).aggregate(lmonth_profit=Sum(('item_profit'), output_field=IntegerField()))

        curmonth_profit = curmonth['tmonth_profit']
        lasmonth_profit = lasmonth['lmonth_profit']
        yettoachieve = lasmonth['lmonth_profit'] - curmonth['tmonth_profit']

        curyear = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year).aggregate(cyear_profit=Sum(('item_profit'), output_field=IntegerField()))

        curyear_profit = curyear['cyear_profit']
        yearyettoachieve = 1000000 - curyear['cyear_profit']

        if yearyettoachieve < 0:
            yearyettoachieve = 0
        else:
            yearyettoachieve = yearyettoachieve

        if yettoachieve < 0:
            yettoachieve = 0
        else:
            yettoachieve = yettoachieve

        ysoldbison = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="bison").exclude(stock_name__product_name__icontains="putty").aggregate(bison_ysold=Sum(('num_of_items'), output_field=IntegerField()))
        ysoldrangoli = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="rangoli").aggregate(rangoli_ysold=Sum(('num_of_items'), output_field=IntegerField()))
        ysoldeclean = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="easy").aggregate(eclean_ysold=Sum(('num_of_items'), output_field=IntegerField()))
        ysoldsilk = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="silk").aggregate(silk_ysold=Sum(('num_of_items'), output_field=IntegerField()))

        ysoldwalmasta = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="walmasta").aggregate(walmasta_ysold=Sum(('num_of_items'), output_field=IntegerField()))
        ysoldsmooth = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="smooth").aggregate(smooth_ysold=Sum(('num_of_items'), output_field=IntegerField()))
        ysoldantidust = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="antidust").aggregate(antidust_ysold=Sum(('num_of_items'), output_field=IntegerField()))
        ysoldallguard = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="allguard").aggregate(allguard_ysold=Sum(('num_of_items'), output_field=IntegerField()))
        ysoldlonglife = SalesRegistry.objects.filter(sold_date__year__exact=todaydate.year, stock_name__product_name__icontains="longlife").aggregate(longlife_ysold=Sum(('num_of_items'), output_field=IntegerField()))

        ysoldbison_sum = ysoldbison['bison_ysold']
        ysoldrangoli_sum = ysoldrangoli['rangoli_ysold']
        ysoldeclean_sum = ysoldeclean['eclean_ysold']
        ysoldsilk_sum = ysoldsilk['silk_ysold']

        ysoldwalmasta_sum = ysoldwalmasta['walmasta_ysold']
        ysoldsmooth_sum = ysoldsmooth['smooth_ysold']
        ysoldantidust_sum = ysoldantidust['antidust_ysold']
        ysoldallguard_sum = ysoldallguard['allguard_ysold']
        ysoldlonglife_sum = ysoldlonglife['longlife_ysold']

        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        YC = [jan_profit,feb_profit,march_profit,april_profit,may_profit,june_profit,july_profit,aug_profit,sept_profit,oct_profit,nov_profit,dec_profit]
        YL = [jan_profitl,feb_profitl,march_profitl,april_profitl,may_profitl,june_profitl,july_profitl,aug_profitl,sept_profitl,oct_profitl,nov_profitl,dec_profitl]

        labelsM = ["Current Profit","Yet to achieve"]
        MCurNMLas = [curmonth_profit,yettoachieve]

        labelsY = ["Current Profit","Yet to achieve"]
        YCurrent = [curyear_profit,yearyettoachieve]

        labelsMbar = ["Bison","Rangoli","EClean","Silk","Walmasta","Wcoat Smooth","AntiDust","All Guard","Long Life"]
        Mbar = [ysoldbison_sum,ysoldrangoli_sum,ysoldeclean_sum,ysoldsilk_sum,ysoldwalmasta_sum,ysoldsmooth_sum,ysoldantidust_sum,ysoldallguard_sum,ysoldlonglife_sum]

        data ={
            "labels": labels,
            "YCur": YC,
            "YLas": YL,
            "labelsM": labelsM,
            "MCurNMLas": MCurNMLas,
            "labelsY": labelsY,
            "YCurrent": YCurrent,
            "labelsMbar": labelsMbar,
            "Mbar": Mbar,
        }
        return Response(data)

# API CHART DATA
###################################################################
######################### Profit Gen ############################
###################################################################
class ProfitGen(CreateView):


    model = ProfitGen
    form_class = ProfitGenForm
    template_name = 'stocks_ubm/profitgen.html'

    def get_context_data(self, **kwargs):
        context = super(ProfitGen, self).get_context_data(**kwargs)
        context['formset'] = ProfitGenFormset(queryset=SalesRegistry.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        formset = ProfitGenFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        a=progeneration.objects.all().delete()
        instances = formset.save(commit=False)
        for instance in instances:
            stock = get_object_or_404(Stock, pk=instance.stock.pk)
            instance.save()
            sale = get_object_or_404(progeneration, pk=instance.pk)
            profitdis = (instance.sold_price - stock.landing_cost) * instance.qty
            sale.profit = profitdis - Decimal(profitdis*Decimal(instance.discount/100))
            sale.save()
        return HttpResponseRedirect('profitgenlist')

class ProfitGenList(CustomMixin,ListView):

    model = progeneration
    template_name = 'stocks_ubm/profitgenlist.html'

###################################################################
######################### Invoice Gen ############################
###################################################################

class InvoiceGen(CreateView):


    model = invoicegeneration
    form_class = InvoiceGenForm
    template_name = 'stocks_ubm/invoicegen.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceGen, self).get_context_data(**kwargs)
        context['formset'] = InvoiceGenFormset(queryset=SalesRegistry.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        formset = InvoiceGenFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        a=invoicegeneration.objects.all().delete()
        instances = formset.save(commit=False)
        for instance in instances:
            stock = get_object_or_404(Stock, pk=instance.stock.pk)
            instance.save()
            sale = get_object_or_404(invoicegeneration, pk=instance.pk)
            pricedis = (instance.sold_price) * instance.qty
            sale.price = pricedis - Decimal(pricedis*Decimal(instance.discount/100))
            sale.save()
        return HttpResponseRedirect('invoicegenlist')

class InvoiceGenList(CustomMixin,ListView):

    model = invoicegeneration
    template_name = 'stocks_ubm/invoicegenlist.html'
