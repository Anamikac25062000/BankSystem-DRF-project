from rest_framework import serializers
from .models import *
from django.utils import timezone
from decimal import Decimal
from .models import Budget, Expense, SavingsGoal, LoanApplication, LoanApproval, Account

"""
Serializes user registration data for creating a new user account.
"""
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'password', 'role', 'phone_number','address', 'aadhar_number', 'pan_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

"""
Serializes user update data for updating user account details.
"""
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'address', 'aadhar_number', 'pan_number']
        read_only_fields = ['email', 'role', 'username', 'aadhar_number', 'pan_number'] 

"""
Serializes staff registration data for creating a new staff account.
"""
class StaffRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username','role', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'address', 'aadhar_number', 'pan_number']

    def create(self, validated_data):
        staff = CustomUser.objects.create(**validated_data)
        return staff

"""
Serializes user login data for authentication.
"""
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

"""
Serializes account data.
"""
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_type', 'balance']

"""
Serializes deposit amount for a transaction.
"""
class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

"""
Serializes transfer amount for a transaction.
"""
class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

"""
Serializes transfer amount for a transaction.
"""
class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    target_account_id = serializers.IntegerField()

"""
Serializes loan application data.
"""
class LoanApplicationSerializer(serializers.ModelSerializer):
    staff_approver = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = LoanApplication
        fields = ['user', 'loan_type', 'amount', 'status', 'applied_date', 'staff_approver']

"""
Serializes the approval of a loan application.
"""
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

"""
Serializes budget data.
"""
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'category', 'amount']

"""
Serializes expense data.
"""
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date']

"""
Serializes savings goal data.
"""
class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = ['id', 'goal_name', 'target_amount', 'current_amount', 'achieved']

"""
Serializes transaction data for viewing account statements.
"""
class ViewStatementSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", default_timezone=timezone.get_current_timezone())
 
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type','timestamp',]
 
 