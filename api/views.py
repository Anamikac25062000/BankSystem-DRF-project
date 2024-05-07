from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
           
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                user.save()  
                # Generate access token
                access_token = AccessToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'access': str(access_token),
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

from rest_framework import generics, permissions
from .models import Account, Transaction
from .serializers import AccountSerializer

class AccountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
       


from .serializers import DepositSerializer, WithdrawalSerializer

class DepositAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            return Response({'message': 'Deposit successful', 'balance': account.balance}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawalAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            account = Account.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                return Response({'message': 'Withdrawal successful', 'balance': account.balance}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import TransferSerializer
from django.db import transaction

class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            target_account_id = serializer.validated_data['target_account_id']
            
            source_account = get_object_or_404(Account, user=request.user)

            try:
                # Ensure the target account exists
                target_account = Account.objects.get(id=target_account_id)
            except Account.DoesNotExist:
                return Response({'error': 'Target account does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            if source_account.balance >= amount:
                # Perform transfer within a transaction
                with transaction.atomic():
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()

                    # Create transaction records
                    Transaction.objects.create(account=source_account, transaction_type=Transaction.WITHDRAWAL, amount=amount)
                    Transaction.objects.create(account=target_account, transaction_type=Transaction.DEPOSIT, amount=amount)

                return Response({'message': 'Fund transfer successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# from .models import LoanApplication
# from .serializers import LoanApplicationSerializer

# class LoanApplicationListCreateAPIView(generics.ListCreateAPIView):
#     queryset = LoanApplication.objects.all()
#     serializer_class = LoanApplicationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class LoanApplicationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = LoanApplication.objects.all()
#     serializer_class = LoanApplicationSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

from rest_framework import generics
from .models import LoanApplication, LoanApproval, InterestRate
from .serializers import (
    InterestRateSerializer,
    LoanApplicationSerializer,
    LoanApprovalSerializer
)
from .permissions import IsAdminOrStaffUser, IsCustomerUser
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal

# class InterestRateCreateAPIView(generics.CreateAPIView):
#     queryset = InterestRate.objects.all()
#     serializer_class = InterestRateSerializer
#     permission_classes = [IsAdminOrStaffUser]

# class InterestRateUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = InterestRate.objects.all()
#     serializer_class = InterestRateSerializer
#     permission_classes = [IsAdminOrStaffUser]

# class InterestListAPIView(generics.ListAPIView):
#     queryset = InterestRate.objects.all()
#     serializer_class = InterestRateSerializer
#     permission_classes = [IsCustomerUser]

#     def get_queryset(self):
#         return InterestRate.objects.all()

# class LoanApplicationCreateAPIView(generics.CreateAPIView):
#     queryset = LoanApplication.objects.all()
#     serializer_class = LoanApplicationSerializer
#     permission_classes = [IsCustomerUser]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.validated_data['user'] = request.user

#         loan_type = serializer.validated_data['loan_type']

#         amount = Decimal(serializer.validated_data['amount'])
#         # duration_years = Decimal(serializer.validated_data['duration_months']) / Decimal('12')

#         try:
#             interest_rate_obj = InterestRate.objects.get(loan_type=loan_type)
#             interest_rate = Decimal(interest_rate_obj.rate) / Decimal('100')  # Convert to Decimal and percentage
#         except InterestRate.DoesNotExist:
#             interest_rate = Decimal('0.10')  # Default interest rate of 10%

#         monthly_interest_rate = interest_rate / Decimal('12')

#         total_payments = duration_years * Decimal('12')

#         # Calculate monthly payment (EMI)
#         monthly_payment = (amount * monthly_interest_rate) / (Decimal('1') - (Decimal('1') + monthly_interest_rate) ** -total_payments)

#         # Calculate total amount payable after loan term
#         total_amount_payable = monthly_payment * total_payments

#         # Save the loan application
#         self.perform_create(serializer)

#         # Retrieve the saved loan application instance
#         loan_application = serializer.instance

#         # Send email notification
#         send_mail(
#             'Loan Application Notification',
#             f'Your loan application for {loan_application.loan_type} has been submitted successfully.',
#             settings.EMAIL_HOST_USER,  # Sender's email
#             [loan_application.user.email],  # Recipient's email
#             fail_silently=True,
#         )

#         return Response({
#             "loan_details": {
#                 "Loan Amount": f"Rs {amount}",
#                 "Tenure": f"{duration_years} years",
#                 "Interest Rate": f"{interest_rate * 100}%",
#                 "Total Amount Payable After Loan Term": f"Rs {total_amount_payable}",
#                 "Monthly Payment (EMI)": f"Rs {monthly_payment}",
#                 "Applied Date": loan_application.applied_date.strftime("%Y-%m-%d %H:%M:%S"),
#                 "Status": loan_application.status,
#             },
#             "message": "Loan application created successfully."
#         }, status=status.HTTP_201_CREATED)


# class LoanApplicationListAPIView(generics.ListAPIView):
#     serializer_class = LoanApplicationSerializer
#     permission_classes = [IsCustomerUser]

#     def get_queryset(self):
#         # Retrieve the authenticated user
#         user = self.request.user
#         # Filter loan applications based on the user
#         return LoanApplication.objects.filter(user=user)


# class LoanApprovalAPIView(generics.CreateAPIView):
#     queryset = LoanApproval.objects.all()
#     serializer_class = LoanApprovalSerializer
#     permission_classes = [IsAdminOrStaffUser]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Update loan application status
#         loan_application = serializer.validated_data['loan_application']
#         new_status = serializer.validated_data['new_status']
#         loan_application.status = new_status
#         loan_application.save()

#         # Create loan approval instance
#         loan_approval = serializer.save()

#         # Send email notification
#         send_mail(
#             'Loan Approval Notification',
#             f'Your loan application for {loan_application.loan_type} has been {new_status.lower()}.',
#             settings.EMAIL_HOST_USER,
#             [loan_application.user.email],
#             fail_silently=True,
#         )

#         return Response({'message': 'Loan status updated and notification sent'}, status=status.HTTP_201_CREATED)


# class UserLoanApplicationListView(generics.ListAPIView):
#     serializer_class = LoanApplicationSerializer
#     permission_classes = [IsAdminOrStaffUser]

#     def get_queryset(self):
#         return LoanApplication.objects.all()


class LoanApplicationCreateAPIView(generics.CreateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsCustomerUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['user'] = request.user

        loan_type = serializer.validated_data['loan_type']
        amount = Decimal(serializer.validated_data['amount'])

        try:
            interest_rate_obj = InterestRate.objects.get(loan_type=loan_type)
            interest_rate = Decimal(interest_rate_obj.rate) / Decimal('100')  # Convert to Decimal and percentage
        except InterestRate.DoesNotExist:
            interest_rate = Decimal('0.10')  # Default interest rate of 10%

        total_amount_payable = amount + (amount * interest_rate)

        # Save the loan application
        self.perform_create(serializer)

        # Retrieve the saved loan application instance
        loan_application = serializer.instance

        # Send email notification
        send_mail(
            'Loan Application Notification',
            f'Your loan application for {loan_application.loan_type} has been submitted successfully.',
            settings.EMAIL_HOST_USER,  # Sender's email
            [loan_application.user.email],  # Recipient's email
            fail_silently=True,
        )

        return Response({
            "loan_details": {
                "Loan Amount": f"Rs {amount}",
                "Interest Rate": f"{interest_rate * 100}%",
                "Total Amount Payable": f"Rs {total_amount_payable}",
                "Applied Date": loan_application.applied_date.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": loan_application.status,
            },
            "message": "Loan application created successfully."
        }, status=status.HTTP_201_CREATED)


class LoanApprovalAPIView(generics.CreateAPIView):
    queryset = LoanApproval.objects.all()
    serializer_class = LoanApprovalSerializer
    permission_classes = [IsAdminOrStaffUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update loan application status
        loan_application = serializer.validated_data['loan_application']
        new_status = serializer.validated_data['new_status']
        loan_application.status = new_status
        loan_application.save()

        # Create loan approval instance
        loan_approval = serializer.save()

        # Send email notification
        send_mail(
            'Loan Approval Notification',
            f'Your loan application for {loan_application.loan_type} has been {new_status.lower()}.',
            settings.EMAIL_HOST_USER,
            [loan_application.user.email],
            fail_silently=True,
        )

        return Response({'message': 'Loan status updated and notification sent'}, status=status.HTTP_201_CREATED)


class UserLoanApplicationListView(generics.ListAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAdminOrStaffUser]

    def get_queryset(self):
        return LoanApplication.objects.all()


class InterestRateCreateAPIView(generics.CreateAPIView):
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer
    permission_classes = [IsAdminOrStaffUser]


class InterestRateUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer
    permission_classes = [IsAdminOrStaffUser]


class InterestListAPIView(generics.ListAPIView):
    queryset = InterestRate.objects.all()
    serializer_class = InterestRateSerializer
    permission_classes = [IsCustomerUser]

    def get_queryset(self):
        return InterestRate.objects.all()



from .models import Budget, Expense, SavingsGoal
from .serializers import BudgetSerializer, ExpenseSerializer, SavingsGoalSerializer

class BudgetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SavingsGoalListCreateAPIView(generics.ListCreateAPIView):
    queryset = SavingsGoal.objects.all()
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
