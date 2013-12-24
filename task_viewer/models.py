from django.db import models

class Check(models.Model):
	name = models.CharField(max_length = 100)

	def __unicode__(self):
		return self.name

class Date(models.Model):
	date = models.DateTimeField()
	check = models.ForeignKey(Check)

	def __unicode__(self):
		return str(self.date)

class Task(models.Model):
	task = models.CharField(max_length = 100)
	check = models.ForeignKey(Check)

	def __unicode__(self):
		return self.task

class Result(models.Model):
	date = models.ForeignKey(Date)
	task = models.ForeignKey(Task)
	status = models.IntegerField(default = 0)
