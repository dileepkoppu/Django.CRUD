from typing import ValuesView
from rest_framework import serializers

from .models import cuboid


class cuboidSerializer(serializers.ModelSerializer):
    class Meta:
        model = cuboid
        fields = ('id','length','breadth','height','area','volume','created_by','created_at','updated_at')
        ValuesView =('created_by',)