from django.db import models
from django.urls import reverse
from submission.misc_functions import image_name
# Create your models here.

class Submission(models.Model):

    class Meta:
        ordering = ["-submission_time"]
        
    REJECTED = 'RJ'
    ACCEPTED = 'AC'
    UNDER_REVIEW = 'UR'
    STATUS_CHOICES = [
        (REJECTED, "Rejected"),
        (ACCEPTED, "Accepted"),
        (UNDER_REVIEW, "Under Review"),
    ]

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=UNDER_REVIEW,
    )
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    approx_bats = models.PositiveIntegerField()
    submission_time = models.DateTimeField(auto_now_add=True)
    rejected_time = models.DateTimeField(blank=True, null=True)
    photo_taken_time = models.DateTimeField()
    # longitude = models.DecimalField(max_digits=12,decimal=8)
    # latitude = models.DecimalField(max_digits=12,decimal=8)
    # TODO
    # latitude and longitude will probably be replaced with pointfield
    def __str__(self):
        return self.get_status_display()
    def get_absolute_url(self):
        return reverse("submission:detail",kwargs={'pk':self.pk})


class SubmissionImage(models.Model):
    submission = models.ForeignKey("Submission", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_name)
