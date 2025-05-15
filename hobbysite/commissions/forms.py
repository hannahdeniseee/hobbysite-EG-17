"""
This is the forms file to specify the different types of forms
used in the Commissions app.
"""

from django import forms
from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    """
    Form for creating and updating a new commission.

    It only includes fields for title, description, and status
    because the other fields are automatically set. The css for
    this form is also set here.
    """
    class Meta:
        model = Commission
        fields = ['title', 'description', 'status', ]


class JobForm(forms.ModelForm):
    """
    Form for creating a new job per commission. Only commissions
    by the logged-in user are accessible.
    """
    class Meta:
        model = Job
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['commission'].queryset = Commission.objects.filter(
                author=user.profile)


class JobApplicationForm(forms.ModelForm):
    """
    Form for creating a new job application.

    It has no fields because its fields are automatically
    determined by the HTML post values.
    """
    class Meta:
        model = JobApplication
        fields = []
