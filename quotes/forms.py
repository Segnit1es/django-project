from django import forms
from django.core.exceptions import ValidationError
from .models import Quote, Source

class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(
        max_length=200,
        label='Источник',
        help_text='Введите название фильма/книги. Если нет — создадим новый.'
    )

    class Meta:
        model = Quote
        fields = ['text', 'source_name', 'weight']

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if Quote.objects.filter(text__iexact=text).exists():
            raise ValidationError('Такая цитата уже существует.')
        return text

    def clean_source_name(self):
        name = self.cleaned_data['source_name'].strip()
        if not name:
            raise ValidationError('Это поле обязательно.')
        source, created = Source.objects.get_or_create(name__iexact=name, defaults={'name': name})
        if source.quotes.count() >= 3:
            raise ValidationError(f'У источника «{source.name}» уже три цитаты.')
        self.cleaned_data['source_obj'] = source
        return name

    def save(self, commit=True):
        self.instance.source = self.cleaned_data['source_obj']
        return super().save(commit=commit)