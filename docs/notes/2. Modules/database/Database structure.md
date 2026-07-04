# Database Schema

## suppliers
Root table for the business's providers. Both product suppliers and loan
grantors are stored here, since in a small local business these are usually
the same people.
- name: supplier's business name
- contact_info: phone number or email to reach them

## categories
Groups products into store sections (makeup, candy, gifts, etc).
Each category belongs to one supplier, allowing the store to know
who provides each section. Also used to classify expenses.
- name: section name
- suppliers_id: who supplies this category → suppliers
- description: optional details about the category

## products
The store's item catalog available for sale. Each product belongs to a
category and is identified by its QR or barcode for the POS scanner.
- name: item name
- categories_id: section it belongs to → categories
- price: current sale price
- state: ACTIVE or INACTIVE — inactive products don't appear in the POS
  but are kept to preserve sales history integrity
- qr_code: code scanned by the reader, nullable if added manually

## sales
Records each complete sale transaction. Only stores the financial summary —
what was sold lives in sale_details.
- datetime: exact date and time of the sale, auto-generated
- total_price: final amount charged to the customer after discount
- discount: percentage discount applied to the whole sale, defaults to 0

## sale_details
Breaks down each sale into its individual products. Allows knowing exactly
which items were sold in each transaction and in what quantity.
- sale_id: sale this detail belongs to → sales
- product_id: item that was sold → products
- quantity: units sold of this product in this transaction

## users
Application access credentials. Password is always stored hashed,
never as plain text.
- username: login name
- password: hash-encrypted password

## employees
Store staff registry. Includes contact info and base salary used
to calculate daily payment in time_worked.
- name: employee's full name
- salary: hourly rate used to calculate each workday payment
- contact_info: employee's phone number
- state: ACTIVE or INACTIVE

## time_worked
Daily attendance log per employee. Allows calculating each workday's
payment based on hours worked and the employee's base salary.
- employee_id: employee this record belongs to → employees
- date: day worked
- time_in: clock-in time
- time_out: clock-out time
- payment: calculated pay based on hours worked and salary
- extra: additional payment for overtime or other concepts, defaults to 0
- state: UNPAID or PAID, tracks whether that day has been paid out

## expenses
Business expenditures classified by category. Covers merchandise purchases,
services, rent, and any other money outflow.
- name: short description of the expense
- categories_id: expense type by category → categories
- amount: amount spent
- datetime: date and time of the expense, auto-generated

## loans
Loans received from suppliers. Records the total amount and how many
installments it will be paid in — each installment lives in installments_details.
- suppliers_id: supplier who granted the loan → suppliers
- amount: total loan amount
- loan_date: date the money was received
- installments: total number of agreed installments
- state: ACTIVE or PAID

## installments_details
Details each individual installment of a loan with its due date and
whether it has been paid. Enables installment-by-installment tracking.
- loan_id: loan this installment belongs to → loans
- number: installment number (1, 2, 3...)
- date: due date for this installment
- state: UNPAID or PAID

## Relationships
- suppliers → categories: one supplier provides many categories
- suppliers → loans: one supplier can grant many loans
- categories → products: one category groups many products
- categories → expenses: one category classifies many expenses
- products → sale_details: one product appears in many sale details
- sales → sale_details: one sale contains many products
- employees → time_worked: one employee has many workday records
- loans → installments_details: one loan has many installments
