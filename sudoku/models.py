from django.db import models

# Create your models here.
class Sudoku(models.Model):
    answer = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    time = models.DateTimeField()

    def __str__(self):
        return self.answer + ',' + self.question