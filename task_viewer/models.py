from django.db import models

class Check(models.Model):
	name = models.CharField(max_length = 100)

	def __unicode__(self):
		return self.name

class Date(models.Model):
	date = models.DateTimeField()
	check = models.ForeignKey(Check)

	def __unicode__(self):
		return self.date
# Create your models here.
