import random
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Quote

def random_quote(request):
    total_weight = Quote.objects.aaggregate(sum=Sum("weight"))['sum'] or 0
    if total_weight ==0:
        return render(request, 'quotes/empty.html')
    rnd = random.uniform(0, total_weight)
    cumulative = 0
    selected = None
    for quote in Quote.objects.all():
        cumulative += quote.weight
        if rnd <= cumulative:
            quote.view_count = F('view_count') + 1
            quote.save(update_fields=['view_count'])
            quote.refresh_from_db()
            selected = quote
            break
    return render(request, 'quotes/random.html',{'quote': selected})