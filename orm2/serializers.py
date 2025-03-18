from rest_framework import serializers
from .models import Business
class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model=Business
        #fields='__all__'
       # fields = '__all__'
        fields = ['id','name', 'revenue', 'profit', 'employees', 'country']
    def validate_revenue(self, value):
        if value < 0:
            raise serializers.ValidationError("Revenue cannot be negative.")
        return value

    def validate_profit(self, value):
        if value < 0:
            raise serializers.ValidationError("Profit cannot be negative.")
        return value

    def validate_employees(self, value):
        if value < 0:
            raise serializers.ValidationError("Number of employees cannot be negative.")
        return value
    
