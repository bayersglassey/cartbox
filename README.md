# CartBox

E-commerce made simple!

Pure HTML, no CSS or Javascript. Just as God intended.

Comes equipped with a powerful (?) analytics system.


# How to deploy

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
