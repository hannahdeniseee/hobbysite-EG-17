from django.shortcuts import render

from .models import Commission, Comment


def commissions_list(request):
    commissions = Commission.objects.all()
    ctx = {
        "commissions": commissions
    }
    return render(request, 'commissions_list.html', ctx)


def commissions_detail(request, pk):
    commission = Commission.objects.get(pk=pk)
    comments = commission.comments.all()
    ctx = {
        "commission": commission,
        "comments": comments
    }
    return render(request, 'commissions_detail.html', ctx)
