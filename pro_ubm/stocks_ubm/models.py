from django.db import models
from django.urls import reverse
from decimal import Decimal
from django.utils.timezone import localdate

class Stock(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    stock_available = models.IntegerField()
    landing_cost = models.DecimalField(decimal_places=2,max_digits=55)

    def __str__(self):
        return self.product_name

    def profit_price(self):
        return self.landing_cost * Decimal(1.15)

    def get_absolute_url(self):
        return reverse("tstock:productdetail",kwargs={'pk':self.pk})

    class Meta:
        ordering = ["product_name"]

class SalesRegistry(models.Model):
    stock_name = models.ForeignKey(Stock,on_delete=models.CASCADE,related_name='sstock')
    num_of_items = models.IntegerField()
    sold_price = models.DecimalField(decimal_places=2,max_digits=55)
    sold_date = models.DateField(default=localdate)
    item_profit = models.DecimalField(decimal_places=2,max_digits=55,default=0)
    slanding_cost = models.DecimalField(decimal_places=2,max_digits=55,default=0)

    def __str__(self):
        return self.stock_name.product_name

    def get_absolute_url(self):
        return reverse("tstock:stockout")

class PurchaseRegistry(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    num_of_items = models.IntegerField()
    purchased_date = models.DateField(default=localdate)
    updated_landing_cost = models.DecimalField(decimal_places=2,max_digits=55,default=0)
    bill_num = models.CharField(max_length=100)
    vat = models.IntegerField(default=18)
    unit_price = models.DecimalField(decimal_places=2,max_digits=55,null=True)
    discount = models.IntegerField(default=5)


    def __str__(self):
        return self.stock.product_name

    def get_absolute_url(self):
        return reverse("tstock:stockin")

class ProfitGen(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    qty = models.IntegerField()
    sold_price = models.DecimalField(decimal_places=2,max_digits=55)
    profit = models.DecimalField(decimal_places=2,max_digits=55,default=0)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.stock.product_name

class InvoiceGen(models.Model):
        stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
        qty = models.IntegerField()
        sold_price = models.DecimalField(decimal_places=2,max_digits=55)
        discount = models.IntegerField(default=0)
        price = models.DecimalField(decimal_places=2,max_digits=55,default=0)

        def __str__(self):
            return self.stock.product_name
