from rest_framework import serializers
from .models import CustomeUser, DeansSessionAvailability, StudentBookedSession

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser
        fields = ('university_id', 'password', 'uuid_token', 'user', 'is_dean', 'is_student')
        

class DeansSessionAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeansSessionAvailability
        fields = ('id', 'session_status', 'session_date',)
        
class StudentBookedSessionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudentBookedSession
        fields = '__all__'
    

class PendingSessionSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = StudentBookedSession
        fields = ('id','student_name')
        
        
    def get_student_name(self, obj):
        return obj['student__user__username']