from datetime import date
from django.db import models

from utils.models import TimeStamps
from users.models import User


class Restaurant(TimeStamps):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    address = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='restaurants', blank=True)


class MenuManager(models.Manager):
    def today_results(self):
        return self.filter(date=date.today()).annotate(result=models.Count('votes'))


class Menu(TimeStamps):
    objects = MenuManager()

    date = models.DateField()
    dishes = models.TextField()

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='menus')

    class Meta:
        unique_together = ('date', 'restaurant')


class Vote(TimeStamps):
    employee = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='votes')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE,
                             related_name='votes')

    class Meta:
        unique_together = ('employee', 'menu')
