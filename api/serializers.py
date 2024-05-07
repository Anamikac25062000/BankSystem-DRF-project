from rest_framework import serializers
from .models import *
from django.utils import timezone
from .models import Account
from .models import LoanApplication, LoanApproval
from decimal import Decimal
from .models import Budget, Expense, SavingsGoal

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'password', 'role', 'phone_number','address', 'aadhar_number', 'pan_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class StaffRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'address', 'aadhar_number', 'pan_number']

    def create(self, validated_data):
        staff = CustomUser.objects.create_staff(**validated_data)
        return staff

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_type', 'balance']

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    target_account_id = serializers.IntegerField()

class LoanApplicationSerializer(serializers.ModelSerializer):
    staff_approver = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = LoanApplication
        fields = ['loan_type', 'amount', 'status', 'applied_date', 'staff_approver']

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApproval
        fields = ['loan_application', 'new_status']

    def create(self, validated_data):
        loan_approval = super().create(validated_data)
        loan_application = validated_data['loan_application']
        new_status = validated_data['new_status']
        loan_application.status = new_status
        loan_application.save()

        send_mail(
            'Loan Approval Notification',
            f'Your loan application for {loan_application.loan_type} has been {new_status.lower()}.',
            settings.EMAIL_HOST_USER,
            [loan_application.user.email],
            fail_silently=True,
        )

        return loan_approval

class InterestRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestRate
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'category', 'amount']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date']

class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = ['id', 'goal_name', 'target_amount', 'current_amount', 'achieved']

class ViewStatementSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", default_timezone=timezone.get_current_timezone())
 
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type','timestamp',]
 
 