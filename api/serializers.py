from rest_framework import serializers
from .models import CustomUser, Transaction

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'password', 'role', 'phone_number','address', 'aadhar_number', 'pan_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


from .models import Account

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

# from .models import LoanApplication

# class LoanApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LoanApplication
#         fields = ['id', 'loan_type', 'amount', 'status']


from .models import LoanApplication, LoanApproval, InterestRate
from django.core.mail import send_mail
from django.conf import settings

# class InterestRateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InterestRate
#         fields = '__all__'

# class LoanApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LoanApplication
#         fields = ['loan_type', 'amount', 'status', 'applied_date']

#     def validate_amount(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Loan amount must be greater than zero.")
#         elif value < 50000:
#             raise serializers.ValidationError("Loan amount must be at least 50000.")
#         return value

#     # def validate_duration_months(self, value):
#     #     if value <= 0:
#     #         raise serializers.ValidationError("Loan duration must be greater than zero.")
#     #     return value

#     def create(self, validated_data):
#         loan_application = super().create(validated_data)

#         # Send email notification
#         send_mail(
#             'Loan Application Notification',
#             f'Your loan application for {loan_application.loan_type} has been submitted successfully.',
#             settings.EMAIL_HOST_USER,  # Sender's email
#             [loan_application.user.email],  # Recipient's email
#             fail_silently=True,
#         )

#         return loan_application

# class LoanApprovalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LoanApproval
#         fields = ['loan_application', 'new_status']

#     def create(self, validated_data):
#         loan_approval = super().create(validated_data)

#         # Send email notification
#         loan_application = validated_data['loan_application']
#         send_mail(
#             'Loan Approval Notification',
#             f'Your loan application for {loan_application.loan_type} has been {validated_data["new_status"].lower()}.',
#             settings.EMAIL_HOST_USER,  # Sender's email
#             [loan_application.user.email],  # Recipient's email
#             fail_silently=True,
#         )

#         return loan_approval

from decimal import Decimal

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['loan_type', 'amount', 'status', 'applied_date']

    def create(self, validated_data):
        loan_application = super().create(validated_data)

        # Send email notification
        send_mail(
            'Loan Application Notification',
            f'Your loan application for {loan_application.loan_type} has been submitted successfully.',
            settings.EMAIL_HOST_USER,  # Sender's email
            [loan_application.user.email],  # Recipient's email
            fail_silently=True,
        )

        return loan_application

class LoanApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApproval
        fields = ['loan_application', 'new_status']

    def create(self, validated_data):
        loan_approval = super().create(validated_data)

        # Update loan application status
        loan_application = validated_data['loan_application']
        new_status = validated_data['new_status']
        loan_application.status = new_status
        loan_application.save()

        # Send email notification
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


from .models import Budget, Expense, SavingsGoal

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
