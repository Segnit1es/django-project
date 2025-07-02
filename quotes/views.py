import random
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Quote
from .forms import QuoteForm
from django.views.decorators.http import require_POST

def random_quote(request):
    total_weight = Quote.objects.aggregate(sum=Sum("weight"))['sum'] or 0
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



@require_POST
def vote_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    action = request.POST.get('action')
    if action == 'like':
        Quote.objects.filter(pk=pk).update(likes=F('likes') + 1)
    elif action == 'dislike':
        Quote.objects.filter(pk=pk).update(dislikes=F('dislikes') + 1)
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    quote.refresh_from_db(fields=['likes', 'dislikes'])
    return JsonResponse({
        'likes': quote.likes,
        'dislikes': quote.dislikes,
    })
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:random')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def top_quotes(request):
    top_list = Quote.objects.order_by('-likes')[:10]
    return render(request, 'quotes/top.html', {'top_list': top_list})