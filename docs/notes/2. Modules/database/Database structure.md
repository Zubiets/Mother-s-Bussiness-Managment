## Suppliers
Stores who provides products and who you may owe money to (loans).

## categories
Groups products into sections like makeup, candy, gifts. Each category has one supplier.

## products
The items sold in the store. Linked to a category and identified by a QR/barcode.

## sales
The general record of a transaction — total charged, discount, date and time.

## sale_details
Breaks down each sale into the individual products purchased, with quantity and price at that moment.

## users
Login credentials for accessing the app.

## employees
Basic staff information — name, salary and contact info.

## time_working
Daily attendance log per employee, tracking time in/out and any extra payment for that day.

## expenses
Money spent by the store, categorized and dated.

## loans
Money borrowed from a supplier, including how many installments and when it was paid.

## installments_dates
Tracks the due date of each individual installment of a loan.

## Relationships
- suppliers → categories, loans
- categories → products, expenses
- products → sale_details
- sales → sale_details
- employees → time_working
- loans → installments_dates
