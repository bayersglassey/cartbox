
# CartBox

## Intro

A minimalist e-commerce system + analytics engine.

The two basic use cases are:

* Dump a set of external data into a fresh CartBox instance, then analyze it

* Feed a steady stream of live data to a CartBox instance, and query it for realtime analytics

There is an ultra-minimalist e-commerce web app interface for testing purposes,
but the idea is to populate the database from an external source using
(for example) a REST API.


## Screenshot

![Shop](/screenshots/shop.png)


## The E-Commerce Model

* _Categories_ have a title and a set of _products_

* _Products_ have a SKU, title, and _category_

* _Users_ have a username and a set of _orders_

* _Orders_ have a _user_ and a set of _items_

* _Order items_ have a _product_ and belong to an _order_,
and know whether they were "suggested" or not

The idea with the "suggested" tag is to have your external e-commerce
system send live data to CartBox, then query the analytics engine to
populate a "Suggested Products" widget.
CartBox can then track whether order items were added via that widget,
allowing you to improve the quality of the suggestions, and verify
that CartBox is helping users find products of interest.


## The Analytics Model (Counters)

The analytics engine is designed to efficiently answer questions such
as "how many orders contain SKU 4011", and "how many orders contain
the pair of SKUs 4011 and 210027".

From those numbers, it's easy to derive statistics such as
"probability that an order contains SKU 4011 given that it
contains SKU 210027".

Each question is a "predicate": a true/false statement about
one of the objects in the e-commerce model (such as an order).
For each predicate, we can store a "counter": a database object
which keeps track of the orders satisfying its predicate.

For instance, there can be a counter for "orders containing SKU 4011",
and another for "orders containing SKUs 4011 and 210027".
Counters are only created as needed, so if there are no orders
containing a given SKU, then no counters are created for it.

Counters allow the implementation of analytics algorithms defined
in terms of mathematical sets.
The usual operations on sets, such as union and intersection, can be
implemented as database queries.

A counter may keep track of its orders by maintaining an actual
list of database IDs, or by simply maintaining a running count
(a single integer), depending on the analytics requirements.


## But Does it Scale?..

Assume a simple setup with 2 types of counter:

* sku counter - "orders containing SKU X"

* sku-pair counter - "orders containing SKUs X and Y"

Let n_skus be the number of SKUs (products) in the database.

What is the maximum number of each type of counter which would be
created in the database?

* Max # sku counters: n_skus (one counter for each SKU)

* Max # sku-pair counters: (n_skus² - n_skus) / 2
(one counter for each unordered pair of SKUs)

The worst case scenario is that an order is placed with one of each SKU.
Then the maximum number of both kinds of counter are created.

The best case scenario is that every order consists of 1 item,
with all orders' items having the same SKU.
Then there is 1 sku counter created, and 0 sku-pair counters,
no matter how many orders are placed!

So, the number of orders in the database by itself tells us nothing
about the number of counters.
In general, orders with fewer items, and orders sharing similar sets
of SKUs, are good because then fewer counters are required.


## A Basic "Suggested Products" Algorithm

Assume we have the following type of counter:

* sku-pair counter - "orders containing SKUs X and Y"

Then for any SKU X, we can generate a list of "also purchased" SKUs
by finding all sku-pair counters containing X.
The "also purchased" list should be sorted so that counters with higher
order counts come first.

Then a simple algorithm for finding 5 "suggested products" given SKU X is
to use the products corresponding to its first 5 "also purchased" SKUs.
(This algorithm could be used for a "Suggested Products" widget on that
product's page on an e-commerce site.)

This algorithm can be extended to sets of products (e.g. carts) by taking
the "also purchased" lists of all products in the set, and combining them,
sorting the resulting list by highest order count.
(This algorithm could be used for a "Suggested Products" widget shown
during the checkout process of an e-commerce site.)

These algorithms can be tweaked in many ways, for instance by adding a
weight to each product which affect how it is sorted in "suggested
product" lists.


## The E-Commerce Web App

E-commerce made simple! Pure HTML, no Javascript - just as God intended.

(Just kidding. Use the API for goodness' sake.)


## The REST API

Under construction!
It should work something like this:

List all orders:

    GET /api/orders/

Add an order:

    POST /api/orders/
    {
        "user": 10,
        "items": [
            {
                "sku": "4011"
            },
            {
                "sku": "4035"
            },
            {
                "sku": "210027"
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

    ./manage.py update_or_create_cats_and_prods

Now open localhost:8000 in your browser and buy buy buy!..

Or point your external source at localhost:8000/api/ and start sending data.
