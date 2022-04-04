from rest_framework import serializers
from magiceightball.models import MotionPicture


class MotionPictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = MotionPicture
        fields = (
            'tconst',
            'rating',
            'votes',
            'type',
            'title',
            'year',
            'runtime',
            'genres',
        )
