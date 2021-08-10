from django.contrib.gis.db import models as gmodels
from django.db import models
from django.urls import reverse
from django.utils import timezone
from submission.misc_functions import image_name


class Species(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Submission(gmodels.Model):

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
    user = gmodels.ForeignKey("core.User", on_delete=models.CASCADE)
    description = gmodels.TextField(blank=True)
    approx_bats = gmodels.PositiveIntegerField()
    submission_time = gmodels.DateTimeField(default=timezone.now)
    rejected_time = gmodels.DateTimeField(blank=True, null=True)
    review = gmodels.TextField(blank=True)
    photo_taken_time = gmodels.DateTimeField()
    location = gmodels.PointField()
    species = models.ManyToManyField(Species, related_name="submission", blank=True)

    objects = gmodels.Manager()

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x

    def __str__(self):
        return str(self.pk) + self.user.username

    def get_all_species_string(self):
        return ", ".join(str(specie.name) for specie in self.species.all())

    def __str__(self):
        return str(self.pk) + " " + self.get_status_display()

    def get_absolute_url(self):
        return reverse("submission:detail", kwargs={'pk': self.pk})

    def is_under_review(self):
        if self.status == self.UNDER_REVIEW:
            return True
        return False

    def delete(self, *args, **kwargs):
        self.images.all().delete()
        super(Submission, self).delete(*args, **kwargs)


class SubmissionImage(models.Model):
    submission = models.ForeignKey(
        "Submission", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_name)

    def delete(self, *args, **kwargs):
        if self.image:  # If image isn't empty, delete image from storage
            storage, path = self.image.storage, self.image.path
            super(SubmissionImage, self).delete(*args, **kwargs)
            storage.delete(path)
        else:
            super(SubmissionImage, self).delete(*args, **kwargs)
