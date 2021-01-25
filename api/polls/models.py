from django.db import models
from django.contrib.auth.models import User
from crum import get_current_request


class Poll(models.Model):
    """ Poll model

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


class Choice(models.Model):
    """ Choice model

        Attributes:
            `poll: ForeignKey`
            `choice_text: CharField`

    Description:\n
        The model managed choices in db
    """
    poll = models.ForeignKey(
        Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField("Choice", max_length=100)

    class Meta:
        verbose_name_plural = "choices"

    def __str__(self):
        return "{}".format(self.choice_text)


class Vote(models.Model):
    """ Vote model

        Attributes:
            `choice:     ForeignKey`
            `poll:       ForeignKey`
            `voted_by:   ForeignKey`

        Constraints: 
            UniqueConstraint:
                `unique_vote = [choice, voted_by]`

    Description:\n
        The model managed user votes in db
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, verbose_name="user choice",
                               related_name='votes', on_delete=models.CASCADE)
    voted_by = models.ForeignKey(
        User, editable=False, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['poll', 'voted_by'], name='unique_vote'),
        ]

    def __str__(self):
        return "{} voted for {}".format(self.voted_by, self.choice)

    def save(self, *args, **kwargs):
        request = get_current_request()
        self.voted_by = request.user
        super(Vote, self).save(*args, **kwargs)
