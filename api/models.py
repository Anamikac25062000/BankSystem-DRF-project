from django.contrib.auth.models import AbstractUser
from django.db import models

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
    phone_number = models.CharField(max_length=10, blank=True, null=True)  # Assuming max length for phone number
    address = models.TextField(blank=True, null=True)  # Assuming address can be multiline
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)  # Assuming Aadhar number length
    pan_number = models.CharField(max_length=10, blank=True, null=True)  # Assuming PAN number length

    def __str__(self):
        return self.username


from django.conf import settings

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
    

# class LoanApplication(models.Model):
#     PERSONAL = 'personal'
#     HOME = 'home'
#     CAR = 'car'
#     EDUCATION = 'education'

#     LOAN_TYPE_CHOICES = [
#         (PERSONAL, 'Personal Loan'),
#         (HOME, 'Home Loan'),
#         (CAR, 'Car Loan'),
#         (EDUCATION, 'Education Loan'),
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, default='pending')
#     # Add more fields as needed: interest rate, duration, etc.

#     def __str__(self):
#         return f"{self.get_loan_type_display()} Loan Application by {self.user.username}"


# class InterestRate(models.Model):
#     LOAN_TYPES = [
#         ('Personal Loan', 'Personal Loan'),
#         ('Home Loan', 'Home Loan'),
#         ('Car Loan', 'Car Loan'),
#         ('Education Loan', 'Education Loan'),
#         # Add more loan types as needed
#     ]

#     loan_type = models.CharField(max_length=100, choices=LOAN_TYPES, unique=True)
#     rate = models.DecimalField(max_digits=5, decimal_places=2)  # Interest rate in percentage

#     def __str__(self):
#         return f"{self.loan_type} Interest Rate: {self.rate}%"

# class LoanApplication(models.Model):
#     LOAN_TYPES = [
#         ('Personal Loan', 'Personal Loan'),
#         ('Home Loan', 'Home Loan'),
#         ('Car Loan', 'Car Loan'),
#         ('Education Loan', 'Education Loan'),
#         # Add more loan types as needed
#     ]

#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#         ('Rejected', 'Rejected'),
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_applications')
#     loan_type = models.CharField(max_length=100, choices=LOAN_TYPES)
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     # duration_months = models.IntegerField(default=0)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     applied_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.loan_type} Application"
    
# class LoanApproval(models.Model):
#     loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
#     approved_date = models.DateField(auto_now_add=True)
#     new_status = models.CharField(max_length=20, choices=LoanApplication.STATUS_CHOICES, default='Approved')

#     def __str__(self):
#         return f"{self.loan_application.user.username} - {self.loan_application.loan_type} Approval"


from decimal import Decimal

class InterestRate(models.Model):
    LOAN_TYPES = [
        ('Personal Loan', 'Personal Loan'),
        ('Home Loan', 'Home Loan'),
        ('Car Loan', 'Car Loan'),
        ('Education Loan', 'Education Loan'),
        # Add more loan types as needed
    ]

    loan_type = models.CharField(max_length=100, choices=LOAN_TYPES, unique=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)  # Interest rate in percentage

    def __str__(self):
        return f"{self.loan_type} Interest Rate: {self.rate}%"

class LoanApplication(models.Model):
    LOAN_TYPES = [
        ('Personal Loan', 'Personal Loan'),
        ('Home Loan', 'Home Loan'),
        ('Car Loan', 'Car Loan'),
        ('Education Loan', 'Education Loan'),
        # Add more loan types as needed
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_applications')
    loan_type = models.CharField(max_length=100, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.loan_type} Application"

class LoanApproval(models.Model):
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
    approved_date = models.DateField(auto_now_add=True)
    new_status = models.CharField(max_length=20, choices=LoanApplication.STATUS_CHOICES, default='Approved')

    def __str__(self):
        return f"{self.loan_application.user.username} - {self.loan_application.loan_type} Approval"


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
