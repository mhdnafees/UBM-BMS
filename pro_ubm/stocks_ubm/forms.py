from django import forms
from .models import Stock,SalesRegistry,PurchaseRegistry,ProfitGen,InvoiceGen
from django.forms import modelformset_factory


class AddProductForm(forms.ModelForm):
    class Meta():
        model = Stock
        fields = ('product_name','stock_available','landing_cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product_name"].label = "Product Name:"
        self.fields["stock_available"].label = "Quantity:"
        self.fields["landing_cost"].label = "Landing Cost:"

class UpdateProductForm(forms.ModelForm):
    class Meta():
        model = Stock
        fields = ('stock_available','landing_cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stock_available"].label = "Stock Available:"
        self.fields["landing_cost"].label = "Landing Cost:"

class DateInput(forms.DateInput):
    input_type = 'date'

class StockOutForm(forms.ModelForm):
    class Meta():
        model = SalesRegistry
        fields = ('sold_date','stock_name','num_of_items','sold_price')
        widgets = {
            'sold_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sold_date"].label = "sold_date"
        self.fields["stock_name"].label = "stock_name"
        self.fields["num_of_items"].label = "num_of_items"
        self.fields["sold_price"].label = "sold_price"

StockOutFormset = modelformset_factory(SalesRegistry, form=StockOutForm, fields=('stock_name','num_of_items','sold_price','sold_date'), extra=10)

class StockInForm(forms.ModelForm):
    class Meta():
        model = PurchaseRegistry
        fields = ('purchased_date','stock','num_of_items','updated_landing_cost')
        widgets = {
            'purchased_date': DateInput(),
        }

StockInFormset = modelformset_factory(PurchaseRegistry, form=StockInForm, fields=('stock','num_of_items','updated_landing_cost','purchased_date'), extra=10)

class ProfitGenForm(forms.ModelForm):
    class Meta():
        model = ProfitGen
        fields = ('stock','qty','sold_price','discount')

ProfitGenFormset = modelformset_factory(ProfitGen, form=ProfitGenForm, fields=('stock','qty','sold_price','discount'), extra=15)

class InvoiceGenForm(forms.ModelForm):
    class Meta():
        model = InvoiceGen
        fields = ('stock','qty','sold_price','discount')

InvoiceGenFormset = modelformset_factory(InvoiceGen, form=InvoiceGenForm, fields=('stock','qty','sold_price','discount'), extra=15)
