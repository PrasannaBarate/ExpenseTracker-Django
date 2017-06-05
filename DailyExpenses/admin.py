from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
	list_display = ('expense_date', 'expense_detail', 'expense_amount', 'user')