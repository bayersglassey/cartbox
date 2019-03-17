from django.views.generic import FormView
from django.db.models import Q
from django import forms
from django.core.exceptions import ValidationError

from cart.models import Category

from .models import ItemPlacedSample, ItemsPlacedTogetherSample


class SampleViewMixin:

    def get_item_placed_samples(self, user, sku, cat, suggested):
        samples = ItemPlacedSample.objects.filter(user=user)
        if sku:
            samples = samples.filter(sku=sku)
        if cat:
            samples = samples.filter(cat=cat)
        if suggested:
            samples = samples.filter(suggested=suggested)
        return samples

    def get_items_placed_together_samples_simple(
            self, user, sku, cat, suggested):
        samples = ItemsPlacedTogetherSample.objects.filter(user=user)
        if sku:
            samples = samples.filter(Q(sku1=sku)|Q(sku2=sku))
        if cat:
            samples = samples.filter(Q(cat1=cat)|Q(cat2=cat))
        if suggested:
            samples = samples.filter(
                Q(suggested1=suggested)|Q(suggested2=suggested))
        return samples

    def get_items_placed_together_samples(
            self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):
        samples = ItemsPlacedTogetherSample.objects.filter(user=user)
        if sku1:
            samples = samples.filter(sku1=sku1)
        if sku2:
            samples = samples.filter(sku2=sku2)
        if cat1:
            samples = samples.filter(cat1=cat1)
        if cat2:
            samples = samples.filter(cat2=cat2)
        if suggested1:
            samples = samples.filter(suggested1=suggested1)
        if suggested2:
            samples = samples.filter(suggested2=suggested2)
        return samples


class SampleSearchForm(forms.Form):
    sku = forms.CharField(label="SKU", required=False)
    cat = forms.ModelChoiceField(label="Category", required=False,
        queryset=Category.objects.all())
    suggested = forms.BooleanField(label="Product was suggested",
        required=False)

class SampleSearchView(SampleViewMixin, FormView):
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
            self.get_items_placed_together_samples_simple(
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
    def clean(self):
        cleaned_data = self.cleaned_data
        sku1 = cleaned_data['sku1']
        sku2 = cleaned_data['sku2']
        if sku1 and sku2 and sku1 >= sku2:
            raise ValidationError(
                "SKUs given in wrong order. {} >= {}"
                .format(repr(sku1), repr(sku2)))


class StatsView(SampleViewMixin, FormView):
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

        # context
        context = self.get_context_data(form=form)
        context['total1'] = total1
        context['total2'] = total2
        context['total_together'] = total_together
        context['together_over_total1'] = total_together / total1
        context['together_over_total2'] = total_together / total2
        context['item1_placed_samples'] = item1_placed_samples
        context['item2_placed_samples'] = item2_placed_samples
        context['items_placed_together_samples'] = items_placed_together_samples

        return self.render_to_response(context)
