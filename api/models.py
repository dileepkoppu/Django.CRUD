from django.db import models
from django.contrib.auth.models import User



class cuboid(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    length=models.IntegerField(blank=False,null=False)
    breadth=models.IntegerField(blank=False,null=False)
    height=models.IntegerField(blank=False,null=False)
    area=models.IntegerField(blank=False,null=False)
    volume=models.IntegerField(blank=False,null=False)
    created_by = models.ForeignKey(User,to_field="username",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.created_by.username