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
    template_name = 'commissions_detail.html'
    context_object_name = 'commission'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
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
        ctx['jobs'] = jobs
        ctx['total_manpower'] = total_manpower
        ctx['open_manpower'] = open_manpower
        return ctx
    

class CommissionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'commissions_form.html'

    def get(self, request):
        return render(request, self.template_name, {
            "commission_form": CommissionForm(),
            "job_form": JobForm(),
        })

    def post(self, request):
        commission_form = CommissionForm()
        job_form = JobForm()

        if 'add_commission' in request.POST:
            commission_form = CommissionForm(request.POST)
            if commission_form.is_valid():
                commission = commission_form.save(commit=False)
                commission.author = request.user.profile  # assumes FK to Profile
                commission.save()
                return redirect('commissions:commission-create')  

        elif 'add_job' in request.POST:
            job_form = JobForm(request.POST)
            if job_form.is_valid():
                job = job_form.save(commit=False)
                latest_commission = Commission.objects.filter(author=request.user.profile).last()
                if latest_commission:
                    job.commission = latest_commission
                    job.save()
                    return redirect('commissions:commission-create')
                else:
                    job_form.add_error(None, "No commission found to link this job to.")

        return render(request, self.template_name, {
            "commission_form": commission_form,
            "job_form": job_form,
        })


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions_form.html'

