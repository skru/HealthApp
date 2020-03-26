from django.db import models

# Create your models here.

class NHSCondition(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	url = models.URLField()

	class Meta:
		ordering = ['title']

	def __str__(self):
		return self.title

class NHSConditionKeyword(models.Model):
	title = models.CharField(max_length=255)
	condition = models.ManyToManyField(NHSCondition)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return self.title
