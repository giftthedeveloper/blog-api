from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'username', 'full_name', 'profile_picture', 'bio', 'date_of_birth')