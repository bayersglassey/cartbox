from django.views.generic import FormView
from django.db.models import Q
from django import forms

from cart.models import Category

from .models import ItemPlacedSample, ItemsPlacedTogetherSample


class SampleViewMixin:

    def get_item_placed_samples(self, user, sku, cat, suggested):
        """Returns samples for given item"""
        filter = {'user': user}
        if sku: filter['sku'] = sku
        if cat: filter['cat'] = cat
        if suggested: filter['suggested'] = suggested
        return ItemPlacedSample.objects.filter(**filter)

    def get_items_placed_together_samples_item1(
            self, user, sku, cat, suggested):
        """Returns samples where given item appears as item1"""
        filter = {'user': user}
        if sku: filter['sku1'] = sku
        if cat: filter['cat1'] = cat
        if suggested: filter['suggested1'] = suggested
        return ItemsPlacedTogetherSample.objects.filter(**filter)

    def get_items_placed_together_samples_item2(
            self, user, sku, cat, suggested):
        """Returns samples where given item appears as item2"""
        filter = {'user': user}
        if sku: filter['sku2'] = sku
        if cat: filter['cat2'] = cat
        if suggested: filter['suggested2'] = suggested
        return ItemsPlacedTogetherSample.objects.filter(**filter)

    def get_items_placed_together_samples_item1_or_item2(
            self, user, sku, cat, suggested):
        """Returns samples where given item appears as item1 or item2"""
        samples = self.get_items_placed_together_samples_item1(
            user, sku, cat, suggested)
        samples |= self.get_items_placed_together_samples_item2(
            user, sku, cat, suggested)
        return samples

    def get_items_placed_together_samples_ordered(
            self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):
        """Returns samples with given item1 and item2 (in that order)"""
        filter = {'user': user}
        if sku1: filter['sku1'] = sku1
        if sku2: filter['sku2'] = sku2
        if cat1: filter['cat1'] = cat1
        if cat2: filter['cat2'] = cat2
        if suggested1: filter['suggested1'] = suggested1
        if suggested2: filter['suggested2'] = suggested2
        return ItemsPlacedTogetherSample.objects.filter(**filter)

    def get_items_placed_together_samples(
            self, user, sku1, sku2, cat1, cat2,
            suggested1, suggested2):
        """Returns samples where given item1 and item2 appear (in either
        order)"""
        samples = self.get_items_placed_together_samples_ordered(
            user, sku1, sku2, cat1, cat2, suggested1, suggested2)
        samples |= self.get_items_placed_together_samples_ordered(
            user, sku2, sku1, cat2, cat1, suggested2, suggested1)
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
