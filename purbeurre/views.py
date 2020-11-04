#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from .models.products import Products
from .models.favorites import Favorites
from .models.categories import Categories


def index(request):
    """
    Display homepage with search forms
    """
    form = SearchForm()
    return render(request, 'index.html', locals())


def legal_information(request):
    """
    Display legal information about the website
    """
    form = SearchForm()
    return render(request, 'legal_information.html', locals())


def search_results(request, product='', *args):
    """
    Search for a product written in the search form by a user
    """
    form = SearchForm(request.GET)
    current_user = request.user
    nutriscore_scale = list(('b', 'c', 'd', 'e'))

    if form.is_valid():
        name = form.cleaned_data['name']
        nutriscore = form.cleaned_data['nutriscore']
        category = form.cleaned_data['category']

        if nutriscore and category:
            index = nutriscore_scale.index(nutriscore)
            # get all the nustricores with value equal or superior than the one selected
            accepted_nutriscore = nutriscore_scale[:index + 1]
            cat = Categories.objects.get(name=category)
            product_list = Products.objects. \
                filter(name__icontains=name, category=cat.id, nutriscore__in=accepted_nutriscore)
        elif nutriscore and not category:
            index = nutriscore_scale.index(nutriscore)
            # get all the nustricores with value equal or superior than the one selected
            accepted_nutriscore = nutriscore_scale[:index + 1]
            product_list = Products.objects. \
                filter(name__icontains=name, nutriscore__in=accepted_nutriscore)
        elif not nutriscore and category:
            cat = Categories.objects.get(name=category)
            product_list = Products.objects. \
                filter(name__icontains=name, category=cat.id)
        else:
            product_list = Products.objects. \
                filter(name__icontains=name)

        # if user is authenticated, get his favorites, else, pass
        try:
            for item in product_list:
                # for each product to display, check if the user added it to its favs
                # in order to display whether the product has already been saved or not
                favorites = Favorites.objects.filter(user=User.objects.get
                (id=current_user.id),
                                                     substitute=item.id) \
                    .prefetch_related('user', 'substitute')
                if favorites:
                    item.is_favorite = True
                else:
                    item.is_favorite = False

        except User.DoesNotExist:
            pass

        paginator = Paginator(product_list, 9)  # 9 products in each page
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            products = paginator.page(paginator.num_pages)

    return render(request, 'purbeurre/search_results.html', locals())


@login_required
def save_product(request, product):
    """
    Get user's product to register and check if
    it's not already in his favorites
    """
    product_to_save = Products.objects.get(name=product)
    current_user = request.user

    if request.method == 'POST':

        # verify if this product is already saved by the user and tag it as
        # favorite in Products table
        product = Favorites.objects.filter(substitute=product_to_save,
                                           user=User.objects.get
                                           (id=current_user.id))
        if not product:
            validated_product = Favorites(substitute=product_to_save,
                                          user=User.objects.get
                                          (id=current_user.id))
            validated_product.save()
            message = messages.add_message(request, messages.SUCCESS,
                                           'Produit sauvegardé',
                                           fail_silently=True)
    return redirect(request.META['HTTP_REFERER'], locals())


@login_required
def saved_products(request):
    """
    Display user's saved products
    """
    form = SearchForm()
    current_user = request.user
    favorites = Favorites.objects.filter(user=current_user.id)
    list_favorites = []
    # for each product saved by a user, added it to list in order to display it
    for i in favorites:
        favorite = Products.objects.get(name=i.substitute)
        list_favorites.append(favorite)

    paginator = Paginator(list_favorites, 9)  # 9 products in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request, 'purbeurre/saved_products.html', locals())


@login_required
def delete_saved_product(request):
    """
    Remove a given product from favorites
    """
    if request.method == 'POST':
        prod_name = request.POST.get('delete_product')
        prod_to_delete = Products.objects.get(name=prod_name)
        current_user = request.user
        # delete the product from favorites table for the user,
        # display success message
        Favorites.objects.get(substitute=prod_to_delete,
                              user=current_user.id).delete()
        message = messages.add_message(request, messages.SUCCESS,
                                       'Produit supprimé',
                                       fail_silently=True)
        return redirect('/saved_products', locals())
    return render(request, 'purbeurre/saved_products.html', locals())


def search_substitutes(request, product):
    """
    Search substitutes for a given product
    """
    form = SearchForm()
    current_user = request.user

    page = request.GET.get('page', 1)
    research = Products.objects.get(name=product)
    # filter product from the same category with better nutriscore
    nutriscore_scale = list(('a', 'b', 'c', 'd', 'e'))
    index = nutriscore_scale.index(research.nutriscore)
    better_nutriscore = nutriscore_scale[:index]
    product_list = Products.objects.filter(nutriscore__in=better_nutriscore,
                                           category=research.category)
    # if user is authenticated, get his favorites, else, pass
    try:
        # for each product to display, check if the user added it to its favs
        # in order to display whether the product has already been saved or not
        for item in product_list:
            favorites = Favorites.objects.filter(user=User.objects.get
            (id=current_user.id),
                                                 substitute=item.id).prefetch_related('user', 'substitute')
            if favorites:
                item.is_favorite = True
            else:
                item.is_favorite = False
    except User.DoesNotExist:
        pass

    # paginate
    paginator = Paginator(product_list, 9)  # 9 products in each page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)

    return render(request, 'purbeurre/substitutes.html', locals())


def product_description(request, product):
    """
    Display nutritional information for a
    given product
    """
    form = SearchForm()
    product_description = Products.objects.get(name=product)
    return render(request, 'purbeurre/product_page.html', locals())
