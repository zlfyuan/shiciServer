from .models import User, FeedBack
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'age', 'email']
        # read_only_fields = ['id', 'user', 'unlike', 'like']


class FeedBackSerializers(ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ["feedback_content"]
