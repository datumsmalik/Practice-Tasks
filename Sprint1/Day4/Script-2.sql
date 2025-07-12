CREATE TABLE dummy_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    orders JSONB,
    street VARCHAR(200),
    city VARCHAR(100),
    zipcode VARCHAR(20)
);

select *
from dummy_data d 

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    product VARCHAR(100),
    price INT
);

INSERT INTO customers (name, city) VALUES
('Alice Johnson', 'New York'),
('Bob Smith', 'Los Angeles'),
('Charlie Lee', 'Chicago');

INSERT INTO orders (customer_id, product, price) VALUES
(1, 'Laptop', 1200),
(1, 'Mouse', 25),
(2, 'Keyboard', 45);

-- Get all rows
SELECT * FROM customers;

select name,city
from customers c 

--alaising
select name as customer_name
from customers c 

select *
from customers c 
where city= 'New York'


--joins ki taraf ate hain

SELECT 
    c.name,
    o.product,
    o.price
FROM 
    customers c
left JOIN 
    orders o 
ON 
    c.id = o.customer_id;


SELECT 
    customer_id ,
    SUM(price) AS total_spent
FROM 
    orders
GROUP BY 
    customer_id
HAVING
	SUM(price)>1000;
	



