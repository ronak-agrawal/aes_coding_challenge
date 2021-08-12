# Create your views here.
from transaction.utils import *
from transaction.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK


def custom_response(data, message, status_code=None):
    if type(message) == ValidationError:
        message = message.args[0]
        status_code = HTTP_400_BAD_REQUEST
    else:
        message = str(message)

    return Response(
        {
            "data": data,
            "message": message,
            "status": status_code
        },
        status=status_code
    )


class AddTransaction(APIView):
    def post(self, request, *args, **kwargs):
        try:
            addtransaction(request)
        except Exception as e:
            return custom_response([], str(e), HTTP_400_BAD_REQUEST)
        return custom_response([], 'success', HTTP_200_OK)


class AddTransactionLineItem(APIView):
    def post(self, request, *args, **kwargs):
        try:
            addlineitem(request)
        except Exception as e:
            return custom_response([], str(e), HTTP_400_BAD_REQUEST)
        return custom_response([], 'success', HTTP_200_OK)


class AddInventoryItem(APIView):
    def post(self, request, *args, **kwargs):
        try:
            addinventoryitem(request)
        except Exception as e:
            return custom_response([], e, HTTP_400_BAD_REQUEST)
        return custom_response([], 'success', HTTP_200_OK)


class DeleteTransaction(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            deletetransaction(request)
        except Exception as e:
            return custom_response([], str(e), HTTP_400_BAD_REQUEST)
        return custom_response([], 'success', HTTP_200_OK)


class ViewTransaction(APIView):
    def get(self, request, *args, **kwargs):
        id = request.data.get('id')
        try:
            transaction = Transaction.objects.get(id=id)
        except:
            return custom_response([], 'error', HTTP_400_BAD_REQUEST)
        data = TransactionSerializer(transaction).data
        return custom_response(data, 'success', HTTP_200_OK)
