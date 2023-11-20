from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus
import streamlit as st

st.header("Adventure database chatbot")

os.environ['OPENAI_API_KEY'] = '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'


#database connection details
DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'DESKTOP-OBV68ET\SQLEXPRESS'
DATABASE_NAME = 'AdventureWorks2014'

conn = f'DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};trusted_connection=yes'

#setting up a connection to the sql db useing sql alchemy and pyodbc driver
quoted = quote_plus(conn)  #encoding the Url
target_connection = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted) #connecting to a MS SQL using pyodbc driver
engine = create_engine(target_connection)   # creating engine to connecting to Sql server


# creating a structred way to interact with SQl db
database = SQLDatabase(engine)    #classing and passing the engine


#connecting with llm
llm=OpenAI(temperature=0)
toolkit = SQLDatabaseToolkit(db=database, llm=llm) #for retreiving the tables from  db we are using SQlDBtk


# After creating LLM model Now initialize the create_sql_agent which is designed to interact with SQL Database,
# The agent is equipped with toolkit to connect to your SQL database and read both the metadata
# and content of the tables.
agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit, #this containds methods for processing natural language queries
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, ##reacting to natural Lan descriptions and getting sql quries
)


#   creating prompt
prompt=st.text_input('Enter the question')

#responsible for handling user input $ displaying the results generated by the agent executor
if st.button('Apply'):
    final=agent_executor.run(prompt) # the agent executor is instructed to run with prompt
    st.text(final) # generated responses are stored in final variable
