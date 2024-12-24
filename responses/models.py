from datetime import datetime, timedelta
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db import models

from quiz.models import Users, Questions, Variants, Test


class Result(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='results_user')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results_test')
    balls = models.IntegerField(default=0, blank=True, null=True)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.end_time is None:
            self.end_time = now() + timedelta(minutes=20)

        if not isinstance(self.start_time, datetime):
            raise ValidationError('start_time must be a valid datetime object.')
        if not isinstance(self.end_time, datetime):
            raise ValidationError('end_time must be a valid datetime object.')

        time_taken = self.end_time - self.start_time
        if time_taken > timedelta(minutes=30):
            self.delete()
            raise ValidationError(
                "Vaqtingoz 30daqiqadan ko'payib ketti!"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}: {self.test}'

    @property
    def time(self):
        return self.end_time - self.start_time


class ResultItm(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='items_result')
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='items_question')
    answer = models.ForeignKey(Variants, on_delete=models.CASCADE, related_name='items_answer')

    def save(self, *args, **kwargs):
        if self.answer.is_true:
            self.result.balls += 1
            if self.result.test.degree == 'easy':
                self.result.balls += self.result.balls * 2
            if self.result.test.degree == 'normal':
                self.result.balls += self.result.balls * 3
            if self.result.test.degree == 'hard':
                self.result.balls += self.result.balls * 5

            self.result.user.ball += self.result.balls
            self.result.user.save()

            self.result.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.result} - {self.question} - {self.answer}'
