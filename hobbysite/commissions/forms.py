from django import forms
from .models import Commission, Job, JobApplication


class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'status', ]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job', ]

    def __init__(self, *args, **kwargs):
        commission = kwargs.pop('commission', None)
        super().__init__(*args, **kwargs)
        if commission:
            self.fields['job'].queryset = Job.objects.filter(commission=commission)
