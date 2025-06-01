from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class Quote(models.Model):
    text = models.TextField(blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    tags = models.CharField(default="", max_length=100, blank=False, null=False)
    page = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} - {self.author}"
    
    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
        ordering = ['-created_at']

class Log(models.Model):
    message = models.TextField(blank=False, null=False)
    status = models.CharField(max_length=20, choices=[
        ('START_LIST', 'Info'),
        ('PAGE', 'Info'),
        ('ERROR', 'Error'),
        ('END_LIST', 'Info'),
        ('ERROR_CREATING', 'Error'),
    ], default='INFO')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} - {self.created_at}"
    
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ['-created_at']

class Schedule(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=False, blank=False, null=False, default=(datetime.now() + timedelta(days=1)))
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ], default='PENDING')

    def __str__(self):
        return f"{self.name} - {self.date} - {self.status}"
    
    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        ordering = ['-date']
