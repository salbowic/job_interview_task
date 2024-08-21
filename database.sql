-- Create schemas
CREATE SCHEMA public;
CREATE SCHEMA sales;
CREATE SCHEMA analytics;

-- Create tables in the public schema
CREATE TABLE public.employees (
    employee_id INTEGER PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    age INTEGER,
    department_id INTEGER,
    hire_date DATE,
    FOREIGN KEY (department_id) REFERENCES public.departments(department_id)
);

CREATE TABLE public.departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES public.employees(employee_id)
);

CREATE TABLE public.salaries (
    employee_id INTEGER PRIMARY KEY,
    salary_amount DECIMAL,
    effective_date DATE,
    FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id)
);

-- Create tables in the sales schema
CREATE TABLE sales.orders (
    order_id INTEGER PRIMARY KEY,
    order_date DATE,
    customer_id INTEGER,
    sales_rep_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES sales.customers(customer_id),
    FOREIGN KEY (sales_rep_id) REFERENCES sales.sales_reps(sales_rep_id)
);

CREATE TABLE sales.customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR,
    contact_number VARCHAR
);

CREATE TABLE sales.sales_reps (
    sales_rep_id INTEGER PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    region VARCHAR
);

CREATE TABLE sales.products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR,
    price DECIMAL
);

-- Create tables in the analytics schema
CREATE TABLE analytics.sales_reports (
    report_id INTEGER PRIMARY KEY,
    report_date DATE,
    total_sales DECIMAL,
    region VARCHAR
);

CREATE TABLE analytics.customer_metrics (
    metric_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    lifetime_value DECIMAL,
    average_order_value DECIMAL,
    FOREIGN KEY (customer_id) REFERENCES sales.customers(customer_id)
);

CREATE TABLE analytics.product_performance (
    performance_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sales_quantity INTEGER,
    revenue_generated DECIMAL,
    FOREIGN KEY (product_id) REFERENCES sales.products(product_id)
);
