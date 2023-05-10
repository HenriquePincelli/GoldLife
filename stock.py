from servers import databaseConnection


#Function to consult a table and check if the user already exists
def consult_Tables(table, id, consultClients):
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM {table} WHERE {id} = ?", consultClients)
    rows = conn.fetchall()
    if len(rows) == 0:
        message = True
    else:
        message = rows
    return message


#Function to consult a table and return the result
def consult_Stock():
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM stock")
    rows = conn.fetchall()

    return rows


#Function to append data from API to the respective module table
def append_Table_Stock(appendProduct):
    #Connect to database and check if the data already exists before appending
    conn = databaseConnection()

    #Check if "Nome_Produto" was used before
    check = consult_Tables("stock", "Nome_Produto", [appendProduct[2].replace(" ", "")])
    try:
        if check[0][2].upper().replace(" ", "") == appendProduct[2].upper().replace(" ", ""):
            message = "Este nome ja esta em uso."
            return message
    except TypeError:
        #Check if the product already exists in the database
        check = consult_Tables("stock", "Codigo_Venda", [appendProduct[1]])

        #Build the query to append the product in the database
        if check is True:
            appendProduct[2] = appendProduct[2].replace(" ", "")
            if appendProduct[2].upper().find("TABACO") != -1:
                appendProduct[4] = appendProduct[4]/(appendProduct[3]/0.02)
            else:
                appendProduct[4] = appendProduct[4]/appendProduct[3]
            #Saving the data
            conn.execute("INSERT INTO stock (Codigo_Produto, Codigo_Venda, Nome_Produto, Quantidade, Preco_Medio_Unitario, Descricao) VALUES(?, ?, ?, ?, ?, ?)", appendProduct)
            conn.connection.commit()
            message = "Produto cadastrado com sucesso!"
        else:
            message = "Este codigo de venda ja esta cadastrado. Por favor verifique."

    return message


#Function to delete a specific product from the database
def delete_Stock(popList):
    #Connect to database and check if the data already exists before deleting
    conn = databaseConnection()

    #Check if the product already exists in the database
    check = consult_Tables("stock", "Codigo_Venda", popList)

    if check is True:
        message = "Nao foi possivel encontrar nenhum produto compativel com o codigo informado."
    else:
        #Saving the data
        conn.execute("DELETE FROM stock WHERE Codigo_Venda = ?", popList)
        conn.connection.commit()
        message = "Produto deletado com sucesso!"

    return message


#Function to update a specific product from the database
def update_Stock(updateList):
    #Connect to database and check if the data already exists before deleting
    conn = databaseConnection()

    #Check if the product already exists in the database
    check = consult_Tables("stock", "Codigo_Venda", [updateList[0]])

    if check is True:
        message = "Nao foi possivel encontrar nenhum produto compativel com o codigo informado."
    else:
        #Saving the data
        updateList[1] = "+" + str(updateList[1]) if updateList[1] >= 0 else updateList[1]
        updateList[1] = str(updateList[1]) if float(updateList[1]) < 0 else updateList[1]
        rows = consult_Tables("stock", "Codigo_Venda", [updateList[0]])
        if float(updateList[1]) == 0:
            message = "0 nao e um valor valido para esta operacao :("
            return message
        price = (float(rows[0][4]) + (float(updateList[2]) / (float(updateList[1].replace("+", "").replace("-", "")) / 0.02))) / 2 if rows[0][2].upper().find("TABACO") != -1 else (float(rows[0][4]) + float(updateList[2]) / float(updateList[1].replace("+", "").replace("-", ""))) / 2
        query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {updateList[0]}){updateList[1]}, Preco_Medio_Unitario = {price} WHERE Codigo_Venda = {updateList[0]}"
        conn.execute(query)
        conn.connection.commit()
        message = "Operacao realizada com sucesso!"

    return message