import sqlparse
import subprocess
from langchain.prompts import PromptTemplate
import csv

generation_template = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Generate a SQL query to answer this question: `{user_question}`
If the question does not match any existing tables or columns, return the word 'error' without generating a SQL query.

DDL statements:
{ddl_statements}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The following SQL query best answers the question `{user_question}`:
"""


verification_template = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Verify if this SQL query correctly answers the question: {user_question}.
SQL query: {sql_query}
If yes, return the same query. If not return corrected query.

DDL statements:
{ddl_statements}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The following SQL query best answers the question `{user_question}`:
```sql
"""


generation_prompt = PromptTemplate(template=generation_template, input_variables=["user_question", "ddl_statements"])
verification_prompt = PromptTemplate(template=verification_template, input_variables=["user_question", "sql_query", "ddl_statements"])


def is_sql_query_valid(sql_query):
    """
    Checks if the SQL query is valid based on the content of the query.
    Returns True if valid, False if an error is detected.
    """
    if "error" in sql_query.lower():
        return False

    return True


def read_ddl_from_file(file_path):
    """
    Reads the DDL statements from a file.
    """
    with open(file_path, 'r') as file:
        ddl_statements = file.read()
    return ddl_statements


def get_sql_query_from_llm(prompt, llm, user_question, ddl_statements):
    """
    Generates an SQL query using the language model.
    """
    llm_chain = prompt | llm
    raw_llm_answer = llm_chain.invoke({"user_question": user_question, "ddl_statements": ddl_statements})
    return raw_llm_answer.strip()
    
    
def is_query_correct(sql_query):
    """
    Validates and fixes a SQL query using sqlfluff. Returns True if the query is correct after fixing,
    otherwise returns False.
    """

    # Write the SQL query to a temporary file
    with open("temp_query.sql", "w") as f:
        f.write(sql_query)
    
    # Run sqlfluff fix on the temporary file
    try:
        fix_result = subprocess.run(
            ["sqlfluff", "fix", "temp_query.sql", "--dialect", "ansi"],
            capture_output=True,
            text=True
        )
        
        # Run sqlfluff lint on the fixed file
        lint_result = subprocess.run(
            ["sqlfluff", "lint", "temp_query.sql", "--dialect", "ansi"],
            capture_output=True,
            text=True
        )
        
        if lint_result.returncode == 0:
            # If lint passes, return True
            return True
        else:
            # If lint fails, check for errors and return False
            output_lines = lint_result.stderr.splitlines()
            errors = [line for line in output_lines if "error" in line.lower()]
            
            if errors:
                print("Errors found in the SQL query:")
                print("\n".join(errors))
            
            return False
    
    except Exception as e:
        print(f"Error running sqlfluff: {e}")
        return False
    
    
def verify_and_correct_sql(llm, sql_query, user_question, ddl_statements):
    """
    Verifies and corrects an SQL query if necessary.
    """
    if not is_query_correct(sql_query):
        llm_chain = verification_prompt | llm
        raw_llm_answer = llm_chain.invoke({"user_question": user_question, "sql_query": sql_query, "ddl_statements": ddl_statements})
        sql_query = raw_llm_answer.strip()
        
        # Run sqlfluff fix on the temporary file
        try:
            fix_result = subprocess.run(
                ["sqlfluff", "fix", "temp_query.sql", "--dialect", "ansi"],
                capture_output=True,
                text=True
            )
            
            with open("temp_query.sql", "r") as f:
                sql_query = f.read()
        
        except Exception as e:
            print(f"Error running sqlfluff: {e}")
            
        return sql_query
    
    else:
        return sql_query
    
    
def text_to_sql_pipe(llm, user_question, ddl_file_path="database.sql"):
    """
    LLM pipeline that converts a user's question to an SQL query and verifies it.
    """
    # Read the DDL statements from the .sql file
    ddl_statements = read_ddl_from_file(ddl_file_path)
    
    # Generate the initial SQL query
    sql_query = get_sql_query_from_llm(generation_prompt, llm, user_question, ddl_statements)
    
    if is_sql_query_valid(sql_query):
        # Verify and potentially correct the SQL query
        final_sql_query = verify_and_correct_sql(llm, sql_query, user_question, ddl_statements)
        
        return final_sql_query
    
    else:
        return "The query does not match any existing tables. Please check the table names or columns and try again."
    
    
def save_queries_to_csv(llm, queries, filename):
    """
    Saves the text queries and their corresponding SQL results to a CSV file.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Text Query", "Generated SQL Query"])
        
        for text_query in queries:
            # Generate SQL query from text query
            generated_sql = text_to_sql_pipe(llm, text_query)
            
            # Write the text query and the generated SQL query to the CSV
            writer.writerow([text_query, generated_sql])