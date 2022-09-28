from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class SpentModel(models.Model):
    title = models.CharField(max_length=50)
    amount = models.IntegerField()
    price_for_unit = models.FloatField()
    time_buyed = models.TimeField(auto_now_add=True)
    day_buyed = models.DateField(auto_now_add=True)
    category = models.ForeignKey('Categories', on_delete=models.PROTECT, default=1)
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('deletespending', kwargs={"spending_pk": self.pk})

    def __str__(self):
        return self.title


class Categories(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse('spendings', kwargs={'cat_name': self.title})

    def __str__(self):
        return self.title

    @staticmethod
    def get_defoult_cats_list():
        default_cats = ['Food', 'Clothes', 'Tech', 'Other']
        amount_of_cats = len(default_cats)
        forcreation = {
            'amount_of_cats':amount_of_cats,
            'default_cats':default_cats,
        }
        return default_cats


class UserFromTg(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tguserid = models.CharField(max_length=60)
