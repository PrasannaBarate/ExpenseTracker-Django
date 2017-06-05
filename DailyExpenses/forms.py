from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class RenewDateForm(forms.Form):
    entered_date = forms.DateField(help_text="Enter a date correctly.")

    def clean_renewal_date(self):
        data = self.cleaned_data['entered_date']

        # #Check date is not in past. 
        # if data < datetime.date.today():
        #     raise ValidationError(_('Invalid date - renewal in past'))

        # #Check date is in range librarian allowed to change (+4 weeks).
        # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        # # Remember to always return the cleaned data.
        return data

class SearchExpenseByDate(forms.Form):
    start_date = forms.DateField(help_text="Start date.", label = "From")
    end_date = forms.DateField(help_text="End date.", label = "To")

    def clean_renewal_date(self):
        data = self.cleaned_data['start_date']

        # #Check date is not in past. 
        # if data < datetime.date.today():
        #     raise ValidationError(_('Invalid date - renewal in past'))

        # #Check date is in range librarian allowed to change (+4 weeks).
        # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        # # Remember to always return the cleaned data.
        return data