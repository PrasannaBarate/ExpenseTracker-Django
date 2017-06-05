from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.ExpensesByUserView.as_view(), name='expense-by-user'),
  url(r'^expense-details/(?P<pk>\d+)$', views.ExpenseDetailView.as_view(), name='expense_details'),
  # url(r'^expense-by/$', views.ExpensesByUserView.as_view(), name='expense-by-user')
]

urlpatterns += [
	url(r'^expense-details/(?P<pk>[-\w]+)/renew/$', views.renew_expense_date, name='renew-expense'),
	url(r'^expense-details/get/$', views.get_expense_on_date, name='get-expense'),
	url(r'^expense/create/$', views.CreateExpense.as_view(), name='expense-create'),
	url(r'^expense/(?P<pk>\d+)/update/$', views.UpdateExpense.as_view(), name='expense_update'),
	url(r'^expense/(?P<pk>\d+)/delete/$', views.DeleteExpense.as_view(), name='expense_delete'),

]
