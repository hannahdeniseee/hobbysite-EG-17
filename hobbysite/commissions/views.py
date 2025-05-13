from django.shortcuts import render

from .models import Commission, Job


def commissions_list(request):
    commissions = Commission.objects.all()
    ctx = {
        "commissions": commissions
    }
    return render(request, 'commissions_list.html', ctx)


def commissions_detail(request, pk):
    commission = Commission.objects.get(pk=pk)
    jobs = commission.job.all()
    ctx = {
        "commission": commission,
        "jobs": jobs
    }
    return render(request, 'commissions_detail.html', ctx)