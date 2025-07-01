from django.db import models
from django.core.exceptions import ValidationError
class Source(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField()
    weight = models.PositiveIntegerField(default=1)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source', 'text')

    def clean(self):
        if self.source.quotes.exclude(pk=self.pk).count() >= 3:
            raise ValidationError(f'У источника "{self.source}" не может быть более трёх цитат.')

    def __str__(self):
        return f'"{self.text[:50]}…" — {self.source}'