from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER = 'user'
    STAFF = 'staff'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username

class Account(models.Model):
    SAVINGS = 'savings'
    CURRENT = 'current'
    FIXED_DEPOSIT = 'fixed_deposit'
    RECURRING_DEPOSIT = 'recurring_deposit'

    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS, 'Savings'),
        (CURRENT, 'Current'),
        (FIXED_DEPOSIT, 'Fixed Deposit'),
        (RECURRING_DEPOSIT, 'Recurring Deposit'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.get_account_type_display()} Account for {self.user.username}"

class Transaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.timestamp}"
    
class LoanApplication(models.Model):
    LOAN_TYPE_CHOICES = [
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('car', 'Car Loan'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    staff_approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='loan_approvals')

    def __str__(self):
        return f"{self.loan_type} Application for {self.user.username}"
 
class LoanApproval(models.Model):
    loan_application = models.ForeignKey('LoanApplication', on_delete=models.CASCADE)
    new_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.loan_application} - {self.new_status}"

class InterestRate(models.Model):
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.interest_rate}% - {self.start_date} to {self.end_date}"
       
class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category} Budget for {self.user.username}"

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} Expense by {self.user.username} on {self.date}"

class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.goal_name} Savings Goal for {self.user.username}"
