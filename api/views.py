from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import CustomUser, Account, Transaction, Budget, Expense, SavingsGoal, LoanApplication
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from .pagination import CustomPagination
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from .serializers import DepositSerializer, WithdrawalSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .serializers import LoanApplicationSerializer, LoanApprovalSerializer, InterestRateSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import LoanApplication
from .serializers import LoanApplicationSerializer
from .models import Budget, Expense, SavingsGoal
from .serializers import BudgetSerializer, ExpenseSerializer, SavingsGoalSerializer

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = StaffRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Staff created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffLoginAPIView(APIView):
    permission_classes = [AllowAny]
 
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
           
            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == CustomUser.STAFF:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Login successful',
                    'token': token.key,
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class StaffLoanApprovalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def post(self, request):
        pass

class StaffUserBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            accounts = Account.objects.filter(user=user)
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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
                access_token = AccessToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'access': str(access_token),
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            target_account_id = serializer.validated_data['target_account_id']
            
            source_account = get_object_or_404(Account, user=request.user)

            try:
                target_account = Account.objects.get(id=target_account_id)
            except Account.DoesNotExist:
                return Response({'error': 'Target account does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            if source_account.balance >= amount:
                with transaction.atomic():
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()

                    Transaction.objects.create(account=source_account, transaction_type=Transaction.WITHDRAWAL, amount=amount)
                    Transaction.objects.create(account=target_account, transaction_type=Transaction.DEPOSIT, amount=amount)

                return Response({'message': 'Fund transfer successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InterestRateCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def post(self, request):
        serializer = InterestRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Interest rate created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InterestRateUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def put(self, request, pk):
        interest_rate = get_object_or_404(InterestRate, pk=pk)
        serializer = InterestRateSerializer(interest_rate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Interest rate updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        interest_rate = get_object_or_404(InterestRate, pk=pk)
        interest_rate.delete()
        return Response({'message': 'Interest rate deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class InterestListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interest_rates = InterestRate.objects.all()
        serializer = InterestRateSerializer(interest_rates, many=True)
        return Response(serializer.data)

class LoanApplicationCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Loan application submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanApprovalAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaffUser]

    def post(self, request, loan_application_id):
        try:
            loan_application = LoanApplication.objects.get(pk=loan_application_id)
            if request.user.role == CustomUser.STAFF:
                loan_application.staff_approver = request.user
                loan_application.status = 'Approved'  # Update the status as approved
                loan_application.save()
                return Response({'message': 'Loan approved successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'You are not authorized to approve/cancel this loan'}, status=status.HTTP_403_FORBIDDEN)
        except LoanApplication.DoesNotExist:
            return Response({'detail': 'Loan application not found'}, status=status.HTTP_404_NOT_FOUND)

class UserLoanApplicationListView(ListAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return LoanApplication.objects.filter(user=user)

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


class ViewAccountStatement(ListAPIView):
    serializer_class = ViewStatementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
 
 
    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.filter(account__user=user).order_by('-timestamp')
        return queryset
 
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ViewStatementSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ViewStatementSerializer(queryset, many=True)
        return Response(serializer.data)
   