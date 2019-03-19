
# CartBox

## Intro

A minimalist e-commerce system + analytics engine.

The two basic use cases are:

* Dump a set of external data into a fresh CartBox instance, then analyze it

* Feed a steady stream of live data to a CartBox instance, and query it for realtime analytics

There is an ultra-minimalist e-commerce interface for testing purposes,
but the idea is to populate the database from an external source using
(for example) a REST API.


## The Model

* *Categories* have a title and a set of *products*

* *Products* have a SKU, title, and *category*

* *Users* have a username and a set of *orders*

* *Orders* have a *user* and a set of *items*

* *Order items* have a *product* and belong to an *order*,
and know whether they were "suggested" or not

The idea with the "suggested" tag is to have your external e-commerce
send live data to CartBox, then query the anaytics engine to populate
a "Suggested Products" widget.
CartBox can track whether order items were added via that widget,
allowing you to improve the quality of the suggestions, and verify
that CartBox is helping users find products of interest.


## The e-commerce interface

E-commerce made simple! Pure HTML, no CSS or Javascript. Just as God intended.

(Just kidding. Use the API for goodness' sake.)


## The REST API

TODO: Implement with Django REST Framework.
It should work something like this:

List all orders:

    GET /api/orders/

Add an order:

    POST /api/orders/
    {
        "user": 10,
        "items": [
            {
                "product": "4011"
            },
            {
                "product": "4035"
            },
            {
                "product": "210027"
            }
        ]
    }

Get statistics:

    GET /api/stats/?user=10&sku1=4011&sku2=210027&suggested=true

    200 OK
    {
        "total_sku1": 30,
        "total_sku2": 20,
        "total_both": 5
    }


## How to deploy

It's a standard Django project.

From repo's root directory, in a fresh virtualenv,

    cd cartbox
    pip install requirements.txt
    echo "DEBUG=True" >local_settings.py
    ./manage.py migrate
    ./manage.py runserver

...should do the trick. Default categories & products are included:

    ./manage.py shell
    >>> from cart.default_data import update_or_create_cats_and_prods
    >>> update_or_create_cats_and_prods()

Now open localhost:8000 in your browser and buy buy buy!..

Or point your external source at localhost:8000/api/ and start sending data.
