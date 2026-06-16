## suppliers
- id: Unique identifier, auto-generated
- name: Supplier's business name
- contact_info: Phone number or email to reach them

## product_categories
- id
- name: Category name (e.g. makeup, candy, gifts)
- supplier_id: Who supplies this category → suppliers
- description: Optional details about the category

## products
- id
- name: Product name
- category_id: Which category it belongs to → product_categories
- price: Sale price
- qr_code: QR or barcode used to scan the product

## sales
- id
- discount: Discount applied to the whole sale, defaults to 0
- total_price: Final amount charged to the customer
- date: When the sale happened
- time: Exact time

## sale_details
- id: Unique identifier, auto-generated
- sale_id: Which sale this detail belongs to → sales
- product_id: Which product was sold → products
- quantity: Units sold of this product
- price: Price of the product at the moment of the sale

## users
- id
- username: Login name for the app
- password: Encrypted access password

## employees
- id
- name: Full name of the employee
- salary: Monthly or hourly salary
- phone: Optional contact number

## time_working
- id
- employee_id: Which employee this record belongs to → employees
- date: The work day being registered
- hours_worked: Total hours worked that day

## expenses
- id
- name: Short description of the expense
- type_id: Category of expense → expense_types
- amount: How much was spent
- date: When the expense occurred

## expense_types
- id
- name: Type name (e.g. supplies, utilities, rent)
- description: Optional details about this expense type

## Relationships
- suppliers → product_categories: one supplier can have many categories
- product_categories → products: one category can have many products
- products → sale_details: one product can appear in many sale details
- sales → sale_details: one sale can have many products
- employees → time_working: one employee can have many work day records
- expense_types → expenses: one type can have many expenses