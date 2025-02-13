from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    api_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Block(models.Model):
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="blocks"
    )
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="blocks"
    )
    block_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(null=True, blank=True)
    stored_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("currency", "block_number")

    def __str__(self):
        return f"{self.currency.name} - {self.block_number}"
