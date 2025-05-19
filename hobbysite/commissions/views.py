"""
This is the views file to create and specify the views for the Commissions app.
This includes the list view, detail view, create view, and
update view for commissions.
"""

from django.shortcuts import render
from .forms import CommissionForm, JobForm, JobApplicationForm
from .models import Commission, Job, JobApplication
from user_management.models import Profile
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class CommissionListView(ListView):
    """
    Displays a list of all commissions.
    """
    model = Commission
    template_name = 'commissions_list.html'
    context_object_name = 'commissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            created_commissions = Commission.objects.filter(
                author=user.profile).ordered_by_status()
            job_applications = JobApplication.objects.filter(
                applicant=user.profile
            )
            applied_commissions = []
            other_commissions = []
            for application in job_applications:
                applied_commissions.append(application.job.commission)
            for commission in Commission.objects.ordered_by_status():
                if ((commission not in created_commissions) and
                   (commission not in applied_commissions)):
                    other_commissions.append(commission)

            context['created_commissions'] = created_commissions
            context['applied_commissions'] = applied_commissions
            context['other_commissions'] = other_commissions
        else:
            all_commissions = Commission.objects.ordered_by_status()
            context['all_commissions'] = all_commissions
        return context


class CommissionDetailView(DetailView):
    """
    Displays the content of each commission and its jobs.

    Allows the user to apply to open jobs.
    """
    model = Commission
    template_name = 'commissions_detail.html'
    context_object_name = 'commission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.object
        user = self.request.user
        if user.is_authenticated:
            user_profile = user.profile
        else:
            user_profile = None

        jobs = Job.objects.filter(
            commission=commission
        )
        accepted_applicants = JobApplication.objects.filter(
            status='accepted',
            job__in=jobs
        )
        total_manpower = 0
        total_open_manpower = 0
        job_current_manpower = []
        all_jobs_full = True
        for job in jobs:
            total_manpower += job.manpower_required
            accepted_applicants_job = accepted_applicants.filter(
                job=job)
            accepted_manpower = accepted_applicants_job.count()
            open_manpower = job.manpower_required - accepted_manpower
            total_open_manpower += open_manpower
            job_appliable = True
            if accepted_manpower == job.manpower_required:
                job_appliable = False
                job.status = 'full'
                job.save()
            job_current_manpower.append((job, open_manpower, job_appliable))
            if open_manpower > 0:
                all_jobs_full = False
        if all_jobs_full and commission.status == 'open':
            commission.status = 'full'
            commission.save()
        context['jobs'] = jobs
        context['total_manpower'] = total_manpower
        context['total_open_manpower'] = total_open_manpower
        context['job_current_manpower'] = job_current_manpower
        context['is_owner'] = commission.author == user_profile
        context['can_apply'] = (
            not all_jobs_full and
            commission.author != user_profile
        )
        if context['can_apply']:
            context['form'] = JobApplicationForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        commission = self.object

        if not request.user.is_authenticated:
            return redirect('accounts:login')

        try:
            applicant = request.user.profile
        except Profile.DoesNotExist:
            messages.error(
                request, "You need a profile to apply."
            )
            return redirect('accounts:register')

        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.commission = commission
            job_application.applicant = applicant
            job_id = request.POST.get('job')
            try:
                job = Job.objects.get(id=job_id)
            except Job.DoesNotExist:
                messages.error(request, "The selected job does not exist.")
                return redirect('commissions:commission-detail',
                                pk=self.object.pk)
            if JobApplication.objects.filter(
                applicant=applicant,job=job).exists():
                messages.error(request, "You've already applied to this job.")
                return redirect('commissions:commission-detail',
                                pk=self.object.pk)
            job_application.job = job
            job_application.save()

            accepted_applicants = JobApplication.objects.filter(
                status='accepted',
                job=job
            )
            if accepted_applicants.count() >= job.manpower_required:
                job.status = 'full'
                job.save()

            job.save()
            commission.save()

            return redirect('commissions:commission-detail',
                            pk=self.object.pk)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CommissionCreateView(LoginRequiredMixin, CreateView):
    """
    Displays the create form for adding a new commission.

    Allows creation of jobs for commissions created by the user.
    """
    template_name = 'commissions_form.html'

    def get(self, request):
        commission_form = CommissionForm()
        job_form = JobForm(user=request.user)
        return render(request, self.template_name, {
            "commission_form": commission_form,
            "job_form": job_form,
        })

    def post(self, request):
        commission_form = CommissionForm()
        job_form = JobForm()

        if 'add_commission' in request.POST:
            commission_form = CommissionForm(request.POST)
            if commission_form.is_valid():
                commission = commission_form.save(commit=False)
                commission.author = request.user.profile
                commission.save()
                return redirect(commission.get_absolute_url())

        elif 'add_job' in request.POST:
            job_form = JobForm(request.POST, user=request.user)
            if job_form.is_valid():
                job = job_form.save(commit=False)
                job.save()
                if job.manpower_required > 0 and job.status == "open":
                    job.commission.status = "open"
                    job.commission.save()
                return redirect(job.commission.get_absolute_url())
            else:
                job_form.add_error(None,
                                   "There was a problem creating the job.")

        return render(request, self.template_name, {
            "commission_form": commission_form,
            "job_form": job_form,
        })


class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Displays the update form for editing a commission.
    """
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions_update.html'
    context_object_name = 'commission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        commission = self.object
        jobs = Job.objects.filter(commission=commission)

        job_applications = []
        for job in jobs:
            applications = JobApplication.objects.filter(
                job=job).ordered_by_status()
            job_applications.append((job, applications))

        context['job_applications'] = job_applications
        return context
    
    def dispatch(self, request, *args, **kwargs):
        commission = self.get_object()
        if commission.author.user != request.user:
            raise PermissionDenied("You are not allowed to edit this.")
        return super().dispatch(request, *args, **kwargs)
