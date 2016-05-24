from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    course_number = models.IntegerField(default=None)
    course_title = models.CharField(max_length=30)
    course_long_name = models.CharField(max_length=50,default='')
    rotation_freeze = models.BooleanField(default=False)

    def __str__(self):
        return self.course_title + ' ' + self.course_long_name

class Group(models.Model):
    course = models.ForeignKey(Course)
    user=models.OneToOneField(User)
    password = models.CharField(max_length=8,default='')
    group_number = models.IntegerField(default=None)
    group_name = models.CharField(max_length=30)
    total_dollars = models.FloatField(default=0)
    interesting_dollars = models.FloatField(default=0.0)
    completeness_dollars = models.FloatField(default=0.0)
    gizmos_dollars = models.FloatField(default=0.0)
    group_members = models.CharField(max_length=200,default='')



    def __str__(self):
        return self.group_name


class Dollars(models.Model):
    group_1 = models.ForeignKey(Group)
    group_2 = models.CharField(max_length=30)
    interesting_dollars = models.FloatField(default=0.0)
    completeness_dollars = models.FloatField(default=0.0)
    gizmos_dollars = models.FloatField(default=0.0)

    def __str__(self):
        g1 = self.group_1.group_name
        g2 = Group.objects.get(group_name=self.group_2).group_name
        return g1 + '\t' + g2 + '\t' + str(self.interesting_dollars) + ' ' \
               + str(self.completeness_dollars) + ' ' + str(self.gizmos_dollars)

class Results(models.Model):
    course = models.ForeignKey(Course)
    group = models.CharField(max_length=30)
    interesting_dollars = models.FloatField(default=0.0)
    completeness_dollars = models.FloatField(default=0.0)
    gizmos_dollars = models.FloatField(default=0.0)
    total_dollars = models.FloatField(default=0.0)

    def get_total_dollars(self):
        self.total_dollars = self.interesting_dollars + self.completeness_dollars + self.gizmos_dollars
        return self.interesting_dollars + self.completeness_dollars + self.gizmos_dollars

class RotationLine(models.Model):
    round = models.IntegerField()
    table = models.IntegerField()
    first_team = models.CharField(max_length=30)
    other_team = models.CharField(max_length=30)

class Notes(models.Model):
    group = models.ForeignKey(Group)
    group_2 = models.CharField(max_length=30)
    notes = models.CharField(max_length=5000)