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
def create_Table_Users():
    conn = databaseConnection()
    conn.execute("CREATE TABLE IF NOT EXISTS users(Codigo_Usuario integer, Nome_Completo text, Email text, Data_Criacao text)")
    return
create_Table_Users()


#Function to append data from API to the respective module table
def append_Table_Users(appendUser):
    #Connect to database and check if the data already exists before appending
    conn = databaseConnection()
    conn.execute("SELECT * FROM users WHERE Codigo_Usuario = ?", [appendUser[0].replace(".", "").replace("-", "").replace("/", "")])
    rows = conn.fetchall()
    if len(rows) == 0:
        #Check if the user code is valid
        appendUser[0] = completaCPFouCNPJ(appendUser[0].replace(".", "").replace("-", "").replace("/", ""))
        appendUser.append(datetime.now().strftime("%d-%m-%Y_%H:%M:%S"))
        conn.execute("INSERT INTO users (Codigo_Usuario, Nome_Completo, Email, Data_Criacao) VALUES(?, ?, ?, ?)", appendUser)
        #Saving the data
        conn.connection.commit()
        message = "Usuario cadastrado com sucesso!"
    else:
        message = "Este usuario ja existe."

    return message


#Function to consult table users and check if the user already exists
def consult_Table_Users(option, consultUser=None):
    conn = databaseConnection()

    if option == "Usuários":
        conn.execute("SELECT * FROM users")
        rows = conn.fetchall()
        return rows
    conn.execute("SELECT * FROM users WHERE Codigo_Usuario = ?", consultUser)
    rows = conn.fetchall()
    if len(rows) == 0:
        if option == "userConsult":
            message = "Nenhum resultado encontrado."
        elif option == "Verificação de usuário":
            message = "Este usuario nao existe. Verifique suas credenciais."
        return message
    elif option == "userConsult":
        return rows
    elif option == "Verificação de usuário":
        message = "Este usuario ja existe. Por gentileza, verifique os dados inseridos e tente novamente."
        return message


#Function to remove a user from the database
def pop_Table_Users(popList):
    conn = databaseConnection()
    conn.execute("SELECT * FROM users WHERE Codigo_Usuario = ?", popList)
    rows = conn.fetchall()
    if len(rows) == 0:
        message = "Nao foi possivel deletar o usuario solicitado. Verifique os parametros fornecidos e tente novamente."
    else:
        conn.execute("DELETE FROM users WHERE Codigo_Usuario = ?", popList)
        #Saving the data
        conn.connection.commit()
        message = "Usuario deletado com sucesso!"

    return message