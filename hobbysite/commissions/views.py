from django.shortcuts import render

from .models import Commission, Comment


def commissions_list(request):
    ctx = {
        "commissions": Commission.objects.all()
    }
    return render(request, 'commissions/commissions_list.html', ctx)


def commission_detail(request, pk):
    ctx = {
        "commission": Commission.objects.get(pk=pk),
    }
    return render(request, 'commissions/commissions_detail.html', ctx)