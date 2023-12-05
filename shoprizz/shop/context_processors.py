from django.shortcuts import render, redirect
from . models import Category, Product


def get_category_list(request):
    get_category_list = Category.objects.all()

    return {'get_category_list': get_category_list}
