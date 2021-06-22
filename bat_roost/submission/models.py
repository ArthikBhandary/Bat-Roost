from django.db import models
from django.urls import reverse
from submission.misc_functions import image_name


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

    @staticmethod
    def is_valid_status(status):
        if status in ["AC", "RJ", "UR"]:
            return True
        return False

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
        return str(self.pk)+ " " + self.get_status_display()

    def get_absolute_url(self):
        return reverse("submission:detail",kwargs={'pk':self.pk})

    def is_under_review(self):
        if self.status == self.UNDER_REVIEW:
            return True
        return False



class SubmissionImage(models.Model):
    submission = models.ForeignKey("Submission", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_name)
    def delete(self, *args, **kwargs):
        if self.image: # If image isn't empty, delete image from storage
            storage, path = self.image.storage, self.image.path
            super(Recipe, self).delete(*args, **kwargs)
            storage.delete(path)
        else:
            super(Recipe, self).delete(*args, **kwargs)
