# Task

Create a an LLM pipeline that will transform any free text query into a SQL query, the key points of this task are:

* Create a valid representation of SQL tables allowing for semantic search that will match the top results to the given free text query

* Based on the table representation the LLM has to create a real SQL query, based on free text user query, that will allow for immediate usage

* LLM has to support creation of queries with different levels of complexity not only the simplest ones

* LLM has to support creating queries to fetch data from different database schemas

* When an error in LLM created sql query is encountered it should attempt to self correct
