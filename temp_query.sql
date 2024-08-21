SELECT
    department_name,
    COUNT(manager_id) AS managers
FROM public.departments
GROUP BY department_name
HAVING COUNT(manager_id) > 1;
