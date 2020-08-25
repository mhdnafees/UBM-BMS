from django.urls import path, include
from . import views

app_name = 'tstock'

urlpatterns = [
    path('',views.index.as_view(),name='index'),

    path('todaystats',views.TodayStats.as_view(),name='todaystats'),

    path('totalstocksandaddproduct/',views.TotalStocksAndAddProduct.as_view(),name='totalstocksandaddproduct'),
    path('productdetail/<int:pk>/',views.ProductDetail.as_view(),name='productdetail'),
    path('updateproducthtml/',views.UpdateProductHTML.as_view(),name='updateproducthtml'),
    path('updateproduct/<int:pk>',views.UpdateProduct.as_view(),name='updateproduct'),

    path('stockout/',views.StockOut.as_view(),name='stockout'),
    path('salesregister/',views.SalesRegister.as_view(),name='salesregister'),

    path('stockin/',views.StockIn.as_view(),name='stockin'),
    path('purchaseregister/',views.PurchaseRegister.as_view(),name='purchaseregister'),

    path('api/chart/data',views.ChartData.as_view(),name="api-chart-data"),

    path('profitgen',views.ProfitGen.as_view(),name='profitgen'),
    path('profitgenlist',views.ProfitGenList.as_view(),name='profitgenlist'),
    path('invoicegen',views.InvoiceGen.as_view(),name='invoicegen'),
    path('invoicegenlist',views.InvoiceGenList.as_view(),name='invoicegenlist'),

]
