import sqlite3
from validator import completaCPFouCNPJ
from flask import Flask
from datetime import datetime


#Connecting with the database
def databaseConnection():
    connection = sqlite3.connect('GoldLifeDB.db', check_same_thread=False)
    conn = connection.cursor()
    return conn


#Function to create the respective module table if not exists
def create_Table_Clients():
    conn = databaseConnection()
    conn.execute("CREATE TABLE IF NOT EXISTS clients(CPF_CNPJ integer, Nome_Completo text, Email text, Telefone text, Logradouro text, Nº_Pedidos_Feitos integer, Nº_Pedidos_Concluidos integer, Data_Cadastro text)")
    return
create_Table_Clients()


#Function to consult a table check if the user already exists
def consult_Tables(table, id, consultClients):
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM {table} WHERE {id} = ?", consultClients)
    rows = conn.fetchall()
    if len(rows) == 0:
        message = True
    else:
        message = False
    return message


#Function to consult a table and return the result
def return_Tables(table, id, consultClients):
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM {table} WHERE {id} = ?", consultClients)
    rows = conn.fetchall()

    return rows


#Function to append data from API to the respective module table
def append_Table_Clients(appendClients):
    #Connect to database and check if the data already exists before appending
    conn = databaseConnection()

    #Check if the user code is valid
    appendClients[0] = completaCPFouCNPJ(appendClients[0].replace(".", "").replace("-", "").replace("/", ""))

    #Build the query to append the client in the databse
    appendClients.append(0)
    appendClients.append(0)
    appendClients.append(datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))
    conn.execute("INSERT INTO clients (CPF_CNPJ, Nome_Completo, Email, Telefone, Logradouro, Nº_Pedidos_Feitos, Nº_Pedidos_Concluidos, Data_Cadastro) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", appendClients)

    #Saving the data
    conn.connection.commit()
    message = "Usuario cadastrado com sucesso!"
    return message


#Function to consult all clients
def all_Clients():
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM clients")
    rows = conn.fetchall()

    return rows


#Function to delete a specific client from the database
def delete_Client(popList):
    conn = databaseConnection()
    conn.execute("DELETE FROM clients WHERE CPF_CNPJ = ?", popList)
    #Saving the data
    conn.connection.commit()
    message = "Usuario deletado com sucesso!"

    return message