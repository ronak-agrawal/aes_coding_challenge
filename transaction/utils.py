from rest_framework import serializers
from transaction.models import *
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class TransactionSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    line_items = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['company', 'branch', 'department', 'transaction_num', 'transaction_status', 'Remarks', 'line_items']

    def get_company(self, obj):
        return obj.company.name

    def get_branch(self, obj):
        return obj.branch.short_name

    def get_department(self, obj):
        return obj.department.name

    def get_line_items(self, obj):
        items = TransactionLineItem.objects.select_related('transaction', 'article', 'colour').filter(transaction=obj)
        return TransactionLineItemSerializer(items, many=True).data


class TransactionLineItemSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    colour = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()

    class Meta:
        model = TransactionLineItem
        fields = ['article', 'colour', 'date', 'quantity', 'rate', 'unit', 'inventory']

    def get_article(self, obj):
        return obj.article.name

    def get_colour(self, obj):
        return obj.colour.name

    def get_inventory(self, obj):
        inv = InventoryItem.objects.select_related('article', 'colour', 'company').filter(lineitem=obj)
        return InventorySerializer(inv, many=True).data


class InventorySerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    colour = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = ['article', 'colour', 'company', 'gross_quantity', 'net_quantity', 'unit']

    def get_article(self, obj):
        return obj.article.name

    def get_colour(self, obj):
        return obj.colour.name

    def get_company(self, obj):
        return obj.company.name


def addtransaction(request):
    company = request.data.get('company')
    branch = request.data.get('branch')
    department = request.data.get('department')
    status = request.data.get('status')
    remarks = request.data.get('remarks')

    if status not in ['PENDING', 'COMPLETED', 'CLOSE']:
        status = 'PENDING'
    try:
        Transaction.objects.create(company_id=company, branch_id=branch, department_id=department,
                                   transaction_status=status,
                                   Remarks=remarks)
    except:
        raise ValidationError('error in creating transaction')


def addlineitem(request):
    transaction = request.data.get('transaction')
    article = request.data.get('article')
    colour = request.data.get('colour')
    date = request.data.get('date')
    quantity = request.data.get('quantity')
    rate = request.data.get('rate')
    unit = request.data.get('unit')

    try:
        tli = TransactionLineItem.objects.create(transaction_id=transaction, article_id=article,
                                                 unit=unit, colour_id=colour, date=date, quantity=quantity, rate=rate)
        if tli.color.article != tli.article:
            tli.delete()
            raise ValidationError('colour has no link to article')
    except Exception as e:
        raise ValidationError(str(e))


def addinventoryitem(request):
    lineitem = request.data.get('lineitem')
    company = request.data.get('company')
    article = request.data.get('article')
    colour = request.data.get('colour')
    gross_quantity = request.data.get('gross_quantity')
    net_qunatity = request.data.get('net_qunatity')
    unit = request.data.get('unit')

    try:
        item = InventoryItem.objects.create(lineitem_id=lineitem, article_id=article,
                                            unit=unit, colour_id=colour, net_quantity=net_qunatity,
                                            gross_quantity=gross_quantity,
                                            company_id=company)
        if item.color.article != item.article:
            item.delete()
            raise ValidationError('colour has no link to article')
    except Exception as e:
        raise ValidationError(e)


def deletetransaction(request):
    id = request.data.get('transactionid')
    try:
        transaction = get_object_or_404(Transaction, id=id)
    except:
        raise ValidationError('Invalid Transaction id')
    transaction.delete()
