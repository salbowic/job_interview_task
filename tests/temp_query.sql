SELECT
    e.first_name,
    e.last_name,
    d.department_name
FROM sales.employees AS e
INNER JOIN sales.departments AS d ON e.department_id = d.department_id;
