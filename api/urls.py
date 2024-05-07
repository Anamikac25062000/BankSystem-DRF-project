# from django.urls import path
# from .views import *
# from .views import AccountListCreateAPIView, AccountDetailAPIView, DepositAPIView, WithdrawalAPIView, TransferAPIView, LoanApplicationListCreateAPIView, LoanApplicationDetailAPIView

# urlpatterns = [
#     path('register/', UserRegistrationAPIView.as_view(), name='register'),
#     path('login/', LoginAPIView.as_view(), name='login'),
#     path('accounts/', AccountListCreateAPIView.as_view(), name='account-list-create'),
#     path('accounts/<int:pk>/', AccountDetailAPIView.as_view(), name='account-detail'),
#     path('deposit/', DepositAPIView.as_view(), name='deposit'),
#     path('withdraw/', WithdrawalAPIView.as_view(), name='withdraw'),
#     path('transfer/', TransferAPIView.as_view(), name='transfer'),
#     path('loan-applications/', LoanApplicationListCreateAPIView.as_view(), name='loan-application-list-create'),
#     path('loan-applications/<int:pk>/', LoanApplicationDetailAPIView.as_view(), name='loan-application-detail'),
#     path('budget/', BudgetListCreateAPIView.as_view(), name='budget-create'),
#     path('expense/', ExpenseListCreateAPIView.as_view(), name='expense-create'),
#     path('savings-goal/', SavingsGoalListCreateAPIView.as_view(), name='savings-goal-create'),
# ]


from django.urls import path
from .views import (
    UserRegistrationAPIView,
    LoginAPIView,
    AccountListCreateAPIView,
    AccountDetailAPIView,
    DepositAPIView,
    WithdrawalAPIView,
    TransferAPIView,
    InterestRateCreateAPIView,
    InterestRateUpdateDestroyAPIView,
    InterestListAPIView,
    LoanApplicationCreateAPIView,
    LoanApprovalAPIView,
    UserLoanApplicationListView,
    BudgetListCreateAPIView,
    ExpenseListCreateAPIView,
    SavingsGoalListCreateAPIView,
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('accounts/', AccountListCreateAPIView.as_view(), name='account-list-create'),
    path('accounts/<int:pk>/', AccountDetailAPIView.as_view(), name='account-detail'),
    path('deposit/', DepositAPIView.as_view(), name='deposit'),
    path('withdraw/', WithdrawalAPIView.as_view(), name='withdraw'),
    path('transfer/', TransferAPIView.as_view(), name='transfer'),
    path('interest-rates/create/', InterestRateCreateAPIView.as_view(), name='interest-rate-create'),
    path('interest-rates/<int:pk>/', InterestRateUpdateDestroyAPIView.as_view(), name='interest-rate-update-destroy'),
    path('interest-rates/', InterestListAPIView.as_view(), name='interest-rate-list'),
    path('loan-applications/create/', LoanApplicationCreateAPIView.as_view(), name='loan-application-create'),
    # path('loan-applications/list/', LoanApplicationListAPIView.as_view(), name='loan-application-list'),
    path('loan-approvals/', LoanApprovalAPIView.as_view(), name='loan-approval'),
    path('user-loan-applications/', UserLoanApplicationListView.as_view(), name='user-loan-application-list'),
    path('budget/', BudgetListCreateAPIView.as_view(), name='budget-create'),
    path('expense/', ExpenseListCreateAPIView.as_view(), name='expense-create'),
    path('savings-goal/', SavingsGoalListCreateAPIView.as_view(), name='savings-goal-create'),
]
