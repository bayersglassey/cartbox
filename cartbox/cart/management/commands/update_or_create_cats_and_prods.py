
from django.core.management.base import BaseCommand, CommandError

from cart.default_data import update_or_create_cats_and_prods


class Command(BaseCommand):

    help = (
        "Updates or creates the default set of Product and "
        "Category objects.")

    def handle(self, *args, **options):
        update_or_create_cats_and_prods()
