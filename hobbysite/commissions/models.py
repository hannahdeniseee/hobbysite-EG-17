"""
This is the models file to specify the fields, ordering, and related methods
for the different models used in the Commissions app.
"""

from django.db import models
from django.db.models import Case, When, IntegerField
from django.urls import reverse
from user_management.models import Profile


class CommissionQuerySet(models.QuerySet):
    """
    Used for custom ordering of commissions.
    """
    def ordered_by_status(self):
        custom_order = ['open', 'full', 'completed', 'discontinued']
        return self.annotate(
            status_priority=Case(
                *[When(status=val, then=idx) for idx, val in enumerate(
                    custom_order)],
                output_field=IntegerField()
            )
        ).order_by('status_priority', '-created_on')


class Commission(models.Model):
    """
    Model for a commission.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('full', 'Full'),
        ('completed', 'Completed'),
        ('discontinued', 'Discontinued')
    ]
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='commission'
    )
    description = models.TextField(null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = CommissionQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission-detail',
                       kwargs={'pk': self.pk})


class Job(models.Model):
    """
    Model for a job.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('full', 'Full')
    ]
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='job'
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-status', '-manpower_required', 'role']

    def __str__(self):
        return self.role


class ApplicationQuerySet(models.QuerySet):
    """
    Used for custom ordering of applications.
    """
    def ordered_by_status(self):
        custom_order = ['pending', 'accepted', 'rejectd',]
        return self.annotate(
            status_priority=Case(
                *[When(status=val, then=idx) for idx, val in enumerate(
                    custom_order)],
                output_field=IntegerField()
            )
        ).order_by('status_priority', '-applied_on')


class JobApplication(models.Model):
    """
    Model for a job application.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applicant'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='job'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    applied_on = models.DateTimeField(auto_now_add=True)
    objects = ApplicationQuerySet.as_manager()

    def __str__(self):
        return f'{self.job.role} - {self.applicant.display_name}'
