from django.shortcuts import render

from .forms import CommissionForm, JobForm, JobApplicationForm
from .models import Commission, Job, JobApplication
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions_list.html'
    context_object_name = 'commissions'


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commission_detail.html'
    context_object_name = 'commission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.object
        jobs = Job.objects.filter(
            commission=commission
        )
        accepted_applicants = JobApplication.objects.filter(
            status='accepted',
            job__in=jobs
        )
        total_manpower = 0
        total_accepted_applicants = len(accepted_applicants)
        for job in jobs:
            total_manpower += job.manpower_required
        open_manpower = total_manpower - total_accepted_applicants
        context['jobs'] = jobs
        context['total_manpower'] = total_manpower
        context['open_manpower'] = open_manpower
        return context
    

class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    

class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commission_form.html'



# def commissions_list(request):
#     commissions = Commission.objects.all()
#     ctx = {
#         "commissions": commissions
#     }
#     return render(request, 'commissions_list.html', ctx)


# def commissions_detail(request, pk):
#     commission = Commission.objects.get(pk=pk)
#     jobs = commission.job.all()
#     ctx = {
#         "commission": commission,
#         "jobs": jobs
#     }
#     return render(request, 'commissions_detail.html', ctx)