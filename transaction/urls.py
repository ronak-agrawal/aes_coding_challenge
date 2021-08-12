from transaction.views import *
from django.urls import path
transaction_urls = [
    path('addtransaction/',AddTransaction.as_view(),name='AddTransaction'),
    path('addtransactionlineitem/',AddTransactionLineItem.as_view(),name='AddTransactionLineItem'),
    path('addinventoryitem/',AddInventoryItem.as_view(),name='AddInventoryItem'),
    path('deletetransaction/',DeleteTransaction.as_view(),name='DeleteTransaction'),
    path('viewtransaction/',ViewTransaction.as_view(),name='ViewTransaction'),
]
