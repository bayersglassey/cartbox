from django.views.generic import FormView
from django import forms

from cart.models import Category

from .models import ItemPlacedSample, ItemsPlacedTogetherSample
from .stats import StatsMixin



class SampleSearchForm(forms.Form):
    sku = forms.CharField(label="SKU", required=False)
    cat = forms.ModelChoiceField(label="Category", required=False,
        queryset=Category.objects.all())
    suggested = forms.BooleanField(label="Product was suggested",
        required=False)

class SampleSearchView(StatsMixin, FormView):
    form_class = SampleSearchForm
    template_name = 'analytics/sample_search.html'

    def form_valid(self, form):
        request = self.request
        user = request.user

        cleaned_data = form.cleaned_data
        sku = cleaned_data['sku']
        category = cleaned_data['cat']
        cat = category and category.id
        suggested = cleaned_data['suggested']

        # 1-item samples
        item_placed_samples = self.get_item_placed_samples(
            user.id, sku, cat, suggested)

        # 2-item samples
        items_placed_together_samples = (
            self.get_items_placed_together_samples_item1_or_item2(
                user.id, sku, cat, suggested))

        # context
        context = self.get_context_data(form=form)
        context['item_placed_samples'] = item_placed_samples
        context['items_placed_together_samples'] = (
            items_placed_together_samples)

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


class StatsView(StatsMixin, FormView):
    form_class = StatsForm
    template_name = 'analytics/stats.html'

    def form_valid(self, form):
        request = self.request
        user = request.user

        cleaned_data = form.cleaned_data
        sku1 = cleaned_data['sku1']
        sku2 = cleaned_data['sku2']
        category1 = cleaned_data['cat1']
        category2 = cleaned_data['cat2']
        cat1 = category1 and category1.id
        cat2 = category2 and category2.id
        suggested1 = cleaned_data['suggested1']
        suggested2 = cleaned_data['suggested2']

        # 1-item samples
        item1_placed_samples = self.get_item_placed_samples(
            user.id, sku1, cat1, suggested1)
        item2_placed_samples = self.get_item_placed_samples(
            user.id, sku2, cat2, suggested2)

        # 2-item samples
        items_placed_together_samples = (
            self.get_items_placed_together_samples(
                user.id, sku1, sku2, cat1, cat2,
                suggested1, suggested2))

        # stats
        total1 = sum(sample.count for sample in item1_placed_samples)
        total2 = sum(sample.count for sample in item2_placed_samples)
        total_together = sum(sample.count
            for sample in items_placed_together_samples)

        def divide(x, y):
            if y == 0: return None
            return x / y

        # context
        context = self.get_context_data(form=form)
        context['total1'] = total1
        context['total2'] = total2
        context['total_together'] = total_together
        context['together_over_total1'] = divide(total_together, total1)
        context['together_over_total2'] = divide(total_together, total2)
        context['item1_placed_samples'] = item1_placed_samples
        context['item2_placed_samples'] = item2_placed_samples
        context['items_placed_together_samples'] = items_placed_together_samples

        return self.render_to_response(context)
