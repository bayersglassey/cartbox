from django.views.generic import FormView
from django.db.models import Q
from django import forms

from cart.models import Category

from .models import ItemPlacedSample, ItemsPlacedTogetherSample


class SampleSearchForm(forms.Form):
    sku = forms.CharField(label="SKU", required=False)
    cat = forms.ModelChoiceField(label="Category", required=False,
        queryset=Category.objects.all())

class SampleSearchView(FormView):
    form_class = SampleSearchForm
    template_name = 'analytics/sample_search.html'
    def form_valid(self, form):
        request = self.request
        user = request.user

        cleaned_data = form.cleaned_data
        sku = cleaned_data['sku']
        cat = cleaned_data['cat'].id

        # 1-item samples
        item_placed_samples = ItemPlacedSample.objects.filter(
            user=user.id)
        if sku:
            item_placed_samples = item_placed_samples.filter(sku=sku)
        if cat:
            item_placed_samples = item_placed_samples.filter(cat=cat)

        # 2-item samples
        items_placed_together_samples = (
            ItemsPlacedTogetherSample.objects.filter(
                user=user.id))
        if sku:
            items_placed_together_samples = (
                items_placed_together_samples.filter(
                    Q(sku1=sku)|Q(sku2=sku)))
        if cat:
            items_placed_together_samples = (
                items_placed_together_samples.filter(
                    Q(cat1=cat)|Q(cat2=cat)))

        context = self.get_context_data(form=form)
        context['item_placed_samples'] = item_placed_samples
        context['items_placed_together_samples'] = (
            items_placed_together_samples)

        return self.render_to_response(context)
