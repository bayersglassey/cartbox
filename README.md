
# CartBox

## Intro

A minimalist e-commerce system + analytics engine.

The two basic use cases are:

* Dump a set of external data into a fresh CartBox instance, then analyze it

* Feed a steady stream of live data to a CartBox instance, and query it for realtime analytics

There is an ultra-minimalist e-commerce interface for testing purposes,
but the idea is to populate the database from an external source using
(for example) a REST API.


## The E-Commerce Model

* *Categories* have a title and a set of *products*

* *Products* have a SKU, title, and *category*

* *Users* have a username and a set of *orders*

* *Orders* have a *user* and a set of *items*

* *Order items* have a *product* and belong to an *order*,
and know whether they were "suggested" or not

The idea with the "suggested" tag is to have your external e-commerce
system send live data to CartBox, then query the anaytics engine to
populate a "Suggested Products" widget.
CartBox can then track whether order items were added via that widget,
allowing you to improve the quality of the suggestions, and verify
that CartBox is helping users find products of interest.


## The Analytics Model

The analytics engine is designed to efficiently answer questions such
as "how many orders contain SKU 4011", and "how many orders contain
the pair of SKUs 4011 and 210027".

From those numbers, it's easy to derive statistics such as
"probability that an order contains SKU 4011 given that it
contains SKU 210027".

Each question is a "predicate": a true/false statement about
one of the objects in the e-commerce model (such as an order).
For each predicate, we can store a "counter": a database object
which counts the number of orders satisfying that predicate.

For instance, there can be a database object which counts "number of orders
containing SKU 4011", and another which counts "number of orders containing
SKUs 4011 and 210027".

Counters are only created as needed, so if there are no orders
containing a given SKU, then no counters are created for it.

In order to generate more kinds of statistic, we just need to implement
more kinds of counter - for instance, we could implement a counter
for "number of order items with SKU X which were placed in an order
containing 5 or more items".


## The E-Commerce Interface

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

    GET /api/stats/?user=10&sku1=4011&sku2=210027

    200 OK
    {
        "total_sku1": 30,
        "total_sku2": 20,
        "total_both": 5
    }

...from this, we can say that among orders which contain SKU 4011,
there is a 5/30 = 17% chance of also containing SKU 210027.
Similarly, among orders which contain SKU 210027, there is a
5/20 = 25% chance of also containing SKU 4011.

Get suggestions:

    GET /api/suggestions/?user=10&sku1=4011&limit=3

    200 OK
    {
        "total_sku1": 30,
        "suggestions": [
            {
                "sku2": "210027",
                "total_both": 5
            },
            {
                "sku2": "4554",
                "total_both": 2
            },
            {
                "sku2": "4035",
                "total_both": 1
            }
        ]
    }

...from this, we can say that among orders which contain SKU 4011,
there is a 5/30 = 17% chance of also containing SKU 210027, a
2/30 = 7% chance of also containing SKU 4554, and a 1/30 = 3% chance
of also containing SKU 4035.


## How to Deploy

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
