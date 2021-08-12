The Setup
Create a virtual environment, python 3.6+.
Install dependencies mentioned in requirements.txt file
To check if its working run : => python manage.py runserver
To apply in-built migrations: => python manage.py migrate
To populate masters, run: => python manage.py populate_masters
Your code goes in the transaction directory
The question
Objective:

To create APIs for a transaction.

Requirements:

Tech Stack - Django, Python 3.6+

For creation of APIs - Can use Django Rest Framework.

PART A: Models

Transaction

Fields

Unique Id - auto_generated primary field

Company - linked to CompanyLedgerMaster - display CompanyLedgerMaster name in response

Branch - linked to BranchMaster - display BranchMaster short_name in response

Department - linked to DepartmentMaster- display DepartmentMaster name in response

Transaction Number - unique for each transaction

Format - TRN/{COUNT}/{YEAR}

Count here should reset to 1 for every year.

Transaction Status - Choice Field. Could be PENDING/COMPLETED/CLOSE

Remarks - Char field. Is optional

Transaction Line Item Details

Each transaction can have multiple item details

Fields

Unique Id - auto_generated primary field

Article - linked to ArticleMaster- display ArticleMaster name in response

Colour - linked to ColorMaster - display ColorMaster name in response

Required on date - A date-time field

Quantity - Decimal Field.

Rate per unit - Integer Field

Unit - Choice Field.Can be KG/METRE

Inventory Item

Each above line item consists of multiple inventory items.

Fields

Unique Id - auto_generated primary field

Article - linked to ArticleMaster- display ArticleMaster name in response

Colour - linked to ColorMaster - display ColorMaster name in response

Company -linked to CompanyLedgerMaster - display CompanyLedgerMaster Name in response

Gross Quantity - Decimal field.

Net Quantity - Decimal field.

Unit - Choice Field.Can be KG/METRE

PART B: APIs to create

Add a transaction document with its line items.

Add line items once a transaction is created.

Add multiple inventory items to line items.

Delete a transaction, cant be deleted if inventory is created.

View a transaction with all its line items and their inventory items.

PART C: Validations (Optional)

Two line items in a transaction cant have same combination of article and colour.

Colour chosen should have a link with chosen article.

All response should be in a format:

{ "data": {}, "message": "", "status": <SOME HTTP STATUS CODE> }

Here,

If the response is successful, it should be returned in the "data" field ;

"message" tells us error in case of any.

"status" is an http response status code.
