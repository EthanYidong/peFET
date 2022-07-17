from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, default="AnonymousUser")
    email = models.CharField(max_length=100, unique=True)
    password = models.BinaryField(max_length=60)
    tutorial_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Participant(models.Model):
    NOT_SUBMITTED = 'N'
    SUBMITTED = 'Y'
    STATUS_CHOICES = [
        (NOT_SUBMITTED, 'Not Submitted'),
        (SUBMITTED, 'Submitted'),
    ]

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=NOT_SUBMITTED,
    )
    last_email_sent = models.DateTimeField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UploadedFetImage(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    original_image = models.ImageField(upload_to='uploads/fet/')
    extracted_image = models.ImageField(upload_to='upload/extracted/', blank=True, null=True)

    def __str__(self):
        return self.participant.name
