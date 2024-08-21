SELECT
    e.first_name,
    e.last_name,
    d.department_name
FROM sales.departments AS d
INNER JOIN sales.employees AS e ON d.manager_id = e.employee_id;
