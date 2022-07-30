from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse


from .models import Quote
from .forms import QuoteForm


def quote_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/quote_list.html', {'quotes': quotes})


def quote_detail(request, pk):
    pass


def quote_new(request):
    pass


def quote_edit(request, pk):
    pass


def quote_delete(request, pk):
    pass
