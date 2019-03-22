from django.views.generic import FormView
from django import forms

from cart.models import Category

from .models import SKUInOrderCounter, SKUPairInOrderCounter
from .stats import StatsMixin, Stats



class CounterForm(forms.Form):
    sku = forms.CharField(label="SKU", required=False)
    cat = forms.ModelChoiceField(label="Category", required=False,
        queryset=Category.objects.all())
    suggested = forms.BooleanField(label="Product was suggested",
        required=False)

class CounterView(StatsMixin, FormView):
    form_class = CounterForm
    template_name = 'analytics/counters.html'

    def form_valid(self, form):
        request = self.request
        user = request.user

        cleaned_data = form.cleaned_data
        sku = cleaned_data['sku']
        category = cleaned_data['cat']
        cat = category and category.id
        suggested = cleaned_data['suggested']

        # 1-SKU counters
        sku_in_order_counters = self.get_sku_in_order_counters(
            user.id, sku, cat, suggested)

        # 2-SKU counters
        sku_pair_in_order_counters = (
            self.get_sku_pair_in_order_counters_for_sku(
                user.id, sku, cat, suggested))

        # context
        context = self.get_context_data(form=form)
        context['sku_in_order_counters'] = sku_in_order_counters
        context['sku_pair_in_order_counters'] = (
            sku_pair_in_order_counters)

        return self.render_to_response(context)



class StatsForm(forms.Form):
    sku1 = forms.CharField(label="SKU 1", required=False)
    sku2 = forms.CharField(label="SKU 2", required=False)
    cat1 = forms.ModelChoiceField(label="Category 1", required=False,
        queryset=Category.objects.all())
    cat2 = forms.ModelChoiceField(label="Category 2", required=False,
        queryset=Category.objects.all())
    suggested1 = forms.BooleanField(label="Product 1 was suggested",
        required=False)
    suggested2 = forms.BooleanField(label="Product 2 was suggested",
        required=False)


class StatsView(FormView):
    form_class = StatsForm
    template_name = 'analytics/stats.html'

    def form_valid(self, form):
        request = self.request
        user = request.user

        # get cleaned data
        cleaned_data = form.cleaned_data
        sku1 = cleaned_data['sku1']
        sku2 = cleaned_data['sku2']
        category1 = cleaned_data['cat1']
        category2 = cleaned_data['cat2']
        cat1 = category1 and category1.id
        cat2 = category2 and category2.id
        suggested1 = cleaned_data['suggested1']
        suggested2 = cleaned_data['suggested2']

        # get stats
        stats = Stats(user.id, sku1, sku2, cat1, cat2,
            suggested1, suggested2)

        # context
        context = self.get_context_data(form=form)
        context['total1'] = stats.total1
        context['total2'] = stats.total2
        context['total_both'] = stats.total_both
        context['both_over_total1'] = stats.both_over_total1
        context['both_over_total2'] = stats.both_over_total2
        context['sku1_in_order_counters'] = stats.sku1_in_order_counters
        context['sku2_in_order_counters'] = stats.sku2_in_order_counters
        context['sku_pair_in_order_counters'] = stats.sku_pair_in_order_counters
        context['suggestions'] = stats.suggestions

        return self.render_to_response(context)
