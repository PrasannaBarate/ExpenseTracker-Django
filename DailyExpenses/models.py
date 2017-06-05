from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Expense(models.Model):
	expense_date = models.DateField()
	expense_detail = models.CharField(null=True, max_length = 200, help_text="Enter expense details")
	expense_amount = models.FloatField(null=True, help_text ="Enter expense amount")
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	def get_absolute_url(self):
		return reverse('expense_details', args=[str(self.id)])
