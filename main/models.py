from django.db import models

# Create your models here.
class Loaner(models.Model):
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)   
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Loaner'
        verbose_name_plural = 'Loaners'

class Payment(models.Model):
    loaner = models.ForeignKey(Loaner, on_delete=models.CASCADE, related_name='payments')
    remaining = models.DecimalField(max_digits=10, decimal_places=0 ,default=0)
    recieved = models.DecimalField(max_digits=10, decimal_places=0 ,default=0)
    payment_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.loaner.name} → {self.recieved} on {self.payment_date}"
