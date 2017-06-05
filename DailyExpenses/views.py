from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Expense
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime
from .forms import RenewDateForm, SearchExpenseByDate
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.


class ExpenseListView(LoginRequiredMixin, generic.ListView):
	model = Expense

class ExpenseDetailView(LoginRequiredMixin, generic.DetailView):
	model = Expense

class ExpensesByUserView(LoginRequiredMixin, generic.ListView):
	model = Expense
	template_name ='DailyExpenses/user_expense_list.html'

	def get_queryset(self):
		startdate = datetime.date.today()
		enddate = startdate - datetime.timedelta(days=8)
		return Expense.objects.filter(user = self.request.user).filter(
			expense_date__range = [enddate, startdate]).order_by('expense_date')

@permission_required('DailyExpenses.can_add_expense')
def renew_expense_date(request, pk):
	print (str(pk))
	expense = get_object_or_404(Expense, pk = pk)
	if request.method == 'POST':
		form = RenewDateForm(request.POST)
		if form.is_valid():
			expense.expense_date = form.cleaned_data['entered_date']
			expense.save()
			return HttpResponseRedirect(reverse('expense-by-user'))
	else:
		proposed_renewal_date = datetime.date.today()
		form = RenewDateForm(initial = {'date' : proposed_renewal_date,})

	return render(request, 'DailyExpenses/renew_date.html', {'form': form, 'expense': expense})

class UpdateExpense(LoginRequiredMixin, UpdateView):
	model = Expense
	fields = ['expense_detail', 'expense_amount']
	success_url = reverse_lazy('expense-by-user')
	def post(self, request, *args, **kwargs):
		if "skip" in request.POST:
			return HttpResponseRedirect(reverse('expense-by-user'))
		else:
			return super(UpdateExpense, self).post(request, *args, **kwargs)

class DeleteExpense(LoginRequiredMixin, DeleteView):
	model = Expense
	success_url = reverse_lazy('expense-by-user')
	def post(self, request, *args, **kwargs):
		if "Cancel" in request.POST:
			return HttpResponseRedirect(reverse('expense-by-user'))
		else:
			return super(DeleteExpense, self).post(request, *args, **kwargs)

class CreateExpense(LoginRequiredMixin, CreateView):
	model = Expense
	fields = ['expense_date', 'expense_detail', 'expense_amount']
	# initial = {'expense_date': datetime.date.today()}
	
	def get_initial(self):
		# current_site = Site.objects.get_current()
		print ("user" + str(self.request.user))
		self.initial = {'expense_date': datetime.date.today(), 'expense_amount' : 0.0}
		return self.initial
	
	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()        
		return HttpResponseRedirect(reverse('expense-by-user'))

@login_required
def get_expense_on_date(request):
	if request.method == 'GET':
		form = SearchExpenseByDate(request.GET)
		if form.is_valid():
			from_date = form.cleaned_data['start_date']
			to_date = form.cleaned_data['end_date']
			expense_list = Expense.objects.filter(user = request.user).filter(
				expense_date__range = [from_date, to_date]).order_by('-expense_date')
			return render(request, 'DailyExpenses/user_expense_list.html',
				{'form': form, 'expense_list': expense_list, 'get': 1})
		else:
			form = SearchExpenseByDate(initial = {'end_date' : datetime.date.today(),})
			return render(request, 'DailyExpenses/user_expense_list.html',
			 {'form': form,})
