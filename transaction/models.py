from datetime import date
from django.db import models


# Masters required in transaction models
class BranchMaster(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(blank=True, null=True, max_length=10)

    def __str__(self):
        return self.short_name


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gst_number = models.CharField(max_length=20, unique=True)
    supplier_status = models.BooleanField(default=False)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class ArticleMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    blend_pct = models.CharField(max_length=50)
    twists = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


class ColorMaster(models.Model):
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    remarks = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name


# Create your models here.


STATUS = (
    ("PENDING", "PENDING"),
    ("COMPLETED", "COMPLETED"),
    ("CLOSE", "CLOSE"),
)


class Transaction(models.Model):
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.PROTECT)
    branch = models.ForeignKey(BranchMaster, on_delete=models.PROTECT)
    department = models.ForeignKey(DepartmentMaster, on_delete=models.PROTECT)
    transaction_num = models.CharField(max_length=100, unique=True, blank=True, null=True)
    transaction_status = models.CharField(max_length=14, choices=STATUS, default="PENDING")
    Remarks = models.TextField(blank=True, null=True)

    def save(self, **kwargs):
        if not self.transaction_num:
            year = date.today().year
            count = Transaction.objects.filter(transaction_num__icontains=year).all().count()+1
            self.transaction_num = f'TRN/{count}/{year}'
        super().save(**kwargs)

    def __str__(self):
        return str(self.id) + '-' + self.company.name + '-' + self.branch.short_name + '-' + self.department.name


UNITS = (
    ("KG", "KG"),
    ("METRE", "METRE"),
)


class TransactionLineItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    colour = models.ForeignKey(ColorMaster, on_delete=models.PROTECT)
    date = models.DateTimeField()
    quantity = models.DecimalField(decimal_places=2, max_digits=5)
    rate = models.IntegerField()
    unit = models.CharField(max_length=15, choices=UNITS)

    def __str__(self):
        return str(self.id) + '-' + self.transaction.__str__() + '-' + self.article.name

    class Meta:
        unique_together = ["transaction", "article", "colour"]


class InventoryItem(models.Model):
    lineitem = models.ForeignKey(TransactionLineItem, on_delete=models.PROTECT)
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    colour = models.ForeignKey(ColorMaster, on_delete=models.PROTECT)
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.PROTECT)
    gross_quantity = models.DecimalField(decimal_places=2, max_digits=5)
    net_quantity = models.DecimalField(decimal_places=2, max_digits=5)
    unit = models.CharField(max_length=15, choices=UNITS)

    def __str__(self):
        return str(self.id) + '-' + self.lineitem.__str__()