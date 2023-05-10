from validator import completaCPFouCNPJ
from datetime import datetime
from servers import databaseConnection, stock_Updator


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
    stock_Updator()
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
    message = "Cliente cadastrado com sucesso!"
    return message


#Function to consult all clients
def all_Clients():
    stock_Updator()
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM clients")
    rows = conn.fetchall()

    return rows


#Function to update the data of a client
def update_Client(updateList):
    conn = databaseConnection()
    code = updateList[0]
    conn.execute(f"UPDATE clients SET CPF_CNPJ = ?, Nome_Completo = ?, Email = ?, Telefone = ?, Logradouro = ? WHERE CPF_CNPJ = {code}", updateList)
    #Saving the data
    conn.connection.commit()
    message = "Cliente atualizado com sucesso!"

    return message


#Function to delete a specific client from the database
def delete_Client(popList):
    conn = databaseConnection()
    conn.execute("DELETE FROM clients WHERE CPF_CNPJ = ?", popList)
    #Saving the data
    conn.connection.commit()
    message = "Cliente deletado com sucesso!"

    return message