from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(InterestRate)
admin.site.register(LoanApplication)
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(SavingsGoal)