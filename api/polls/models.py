from django.db import models
from django.contrib.auth.models import User
from crum import get_current_request


class Poll(models.Model):
    """ Poll Model

        Attributes:
            `question`        CharField
            `created_by`      ForeignKey
            `pub_date`        DateTimeField
            `last_modified`   DateTimeField

    Description:\n
        The model managed polls in db
    """
    question = models.CharField("Question", max_length=100)
    created_by = models.ForeignKey(
        User, verbose_name="Created by",
        editable=False, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("Published on", auto_now_add=True)
    last_modified = models.DateTimeField("Last modified on", auto_now=True)

    class Meta:
        verbose_name_plural = "polls"

    def __str__(self):
        return "{}".format(self.question)

    def save(self, *args, **kwargs):
        request = get_current_request()
        self.created_by = request.user
        super(Poll, self).save(*args, **kwargs)
