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

from django.views.decorators.http import require_POST

@require_POST
def vote_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    action = request.POST.get('action')
    if action == 'like':
        quote.likes = F('likes') + 1
    elif action == 'dislike':
        quote.dislikes = F('dislikes') + 1
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    quote.save(update_fields=['likes', 'dislikes'])
    quote.refresh_from_db()
    return JsonResponse({'likes': quote.likes, 'dislikes': quote.dislikes})