from servers import databaseConnection
from datetime import datetime


#Function to consult a table and check if the user already exists
def consult_Tables(table, id, consultList):
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM {table} WHERE {id} = ?", consultList)
    rows = conn.fetchall()
    if len(rows) == 0:
        message = True
    else:
        message = rows
    return message


#Function to consult a table and return the result
def consult_Payments():
    conn = databaseConnection()
    conn.execute(f"SELECT * FROM payments")
    rows = conn.fetchall()

    return rows


#Function to update the status of a payment
def update_Table_Payments(updatePaymentsList):
    message = consult_Tables("payments", "Numero_Pedido", [updatePaymentsList[0]])
    if message is True:
        message = "Erro. Verifique o numero do pedido inserido e tente novamente."
    else:
        #Updating the database with the request data
        conn = databaseConnection()
        query = f"UPDATE payments SET Forma_Pagamento = '{updatePaymentsList[1]}', Data_Pagamento = '{updatePaymentsList[2]}' WHERE Numero_Pedido = '{updatePaymentsList[0]}'"
        conn.execute(query)
        conn.connection.commit()
        message = "Operacao realizada com sucesso!"

    return message


#Function to update stock after a sale register
def low_Stock(updateList):
    conn = databaseConnection()

    #Storing all products from the request
    conn.execute(f"SELECT * FROM stock WHERE Codigo_Venda = {str(updateList[1][0])}")
    update1 = conn.fetchall()
    conn.execute(f"SELECT * FROM stock WHERE Codigo_Venda = {str(updateList[1][1])}")
    update2 = conn.fetchall()
    conn.execute(f"SELECT * FROM stock WHERE Codigo_Venda = {str(updateList[1][2])}")
    update3 = conn.fetchall()

    #Check if the request matches the KIT
    if len(update1) == 0 and len(update2) == 0 and len(update3) == 0:
        message = "Verifique o codigo dos produtos vendidos e tente novamente."
        return message
    ok = True if update1[0][0] != update2[0][0] and update1[0][0] != update3[0][0] and update2[0][0] != update3[0][0] else False
    if ok is True:
        #Making the calculation before updating stock and checking the query to build
        quantityUpdateTobacco = "-" + str(updateList[2] * 0.02)
        quantityUpdate = "-" + str(updateList[2])
        if "TABACO" in update1[0][2].upper():
            if update1[0][3] - float(quantityUpdateTobacco.replace("-", "")) < 0:
                message = "Estoque insuficiente."
                return message
        elif "TABACO" not in update1[0][2].upper():
            if update1[0][3] - float(quantityUpdate.replace("-", "")) < 0:
                message = "Estoque insuficiente."
                return message
        if "TABACO" in update2[0][2].upper():
            if update2[0][3] - float(quantityUpdateTobacco.replace("-", "")) < 0:
                message = "Estoque insuficiente."
                return message
        elif "TABACO" not in update2[0][2].upper():
            if update2[0][3] - float(quantityUpdate.replace("-", "")) < 0:
                message = "Estoque insuficiente."
                return message
        if "TABACO" in update3[0][2].upper():
            if update3[0][3] - float(quantityUpdateTobacco.replace("-", "")) < 0:
                message = "Estoque insuficiente."
                return message
        elif "TABACO" not in update3[0][2].upper():
            if update3[0][3] - float(quantityUpdate.replace("-", "")) < 0:
                message = "Estoque insuficiente."
                return message
        if "TABACO" in update1[0][2].upper():
            query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {updateList[1][0]}){quantityUpdateTobacco} WHERE Codigo_Venda = {updateList[1][0]}"
            conn.execute(query)
            conn.connection.commit()
        else:
            query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {updateList[1][0]}){quantityUpdate} WHERE Codigo_Venda = {updateList[1][0]}"
            conn.execute(query)
            conn.connection.commit()
        if "TABACO" in update2[0][2].upper():
            query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {updateList[1][1]}){quantityUpdateTobacco} WHERE Codigo_Venda = {updateList[1][1]}"
            conn.execute(query)
            conn.connection.commit()
        else:
            query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {updateList[1][1]}){quantityUpdate} WHERE Codigo_Venda = {updateList[1][1]}"
            conn.execute(query)
            conn.connection.commit()
        if "TABACO" in update3[0][2].upper():
            query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {updateList[1][2]}){quantityUpdateTobacco} WHERE Codigo_Venda = {updateList[1][2]}"
            conn.execute(query)
            conn.connection.commit()
        else:
            query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {updateList[1][2]}){quantityUpdate} WHERE Codigo_Venda = {updateList[1][2]}"
            conn.execute(query)
            conn.connection.commit()
        message = True
    else:
        message = "Solicitacao de venda invalida, os kits nao podem conter um ou mais produtos de mesma origem."

    return message


#Function to append data from API to the respective module table
def append_Table_Payments(appendPayment):
    #Creating a value to "Numero_Pedido" and "Data_Pedido" and appending in the "appendPayment" list
    appendPayment[0] = str(appendPayment[0].replace(".", "").replace("-", "").replace("/", ""))
    check = consult_Tables("clients", "CPF_CNPJ", [appendPayment[0]])
    if check is True:
        message = "Este cliente nao esta cadastrado. Antes de cadastrar um pagamento e preciso cadastrar o respectivo cliente."
        return message
    else:
        message = low_Stock(appendPayment)
        if message is True:
            conn = databaseConnection()
            conn.execute(f"SELECT * FROM payments WHERE CPF_CNPJ = {appendPayment[0]} ORDER BY Data_Pedido DESC;")
            rows = conn.fetchall()
            nRequest = appendPayment[0] + "|" + str(int(rows[0][0].split("|")[1]) + 1) if len(rows) != 0 else appendPayment[0] + "|1"
            appendPayment.insert(0, nRequest)
            dateRequest = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
            appendPayment.insert(6, dateRequest)
            appendPayment[2] = str(appendPayment[2])

            #Saving the data
            conn.execute("INSERT INTO payments(Numero_Pedido, CPF_CNPJ, Produtos, Quantidade, Valor_Pedido, Forma_Pagamento, Data_Pedido, Data_Pagamento) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", appendPayment)
            conn.connection.commit()
            message = nRequest
        
        return message


#Function to update stock after a sale delete
def up_Stock(updateList):
    conn = databaseConnection()

    #Storing all products from the request
    deleteID1 = updateList[0][2].replace("[", "").replace("]", "").replace(" ", "").split(",")[0]
    deleteID2 = updateList[0][2].replace("[", "").replace("]", "").replace(" ", "").split(",")[1]
    deleteID3 = updateList[0][2].replace("[", "").replace("]", "").replace(" ", "").split(",")[2]
    conn.execute(f"SELECT * FROM stock WHERE Codigo_Venda = {deleteID1}")
    delete1 = conn.fetchall()
    conn.execute(f"SELECT * FROM stock WHERE Codigo_Venda = {deleteID2}")
    delete2 = conn.fetchall()
    conn.execute(f"SELECT * FROM stock WHERE Codigo_Venda = {deleteID3}")
    delete3 = conn.fetchall()

    #Making the calculation before updating stock and checking the query to build
    quantityDeleteTobacco = "+" + str(updateList[0][3] * 0.02)
    quantityDelete = "+" + str(updateList[0][3])
    if "TABACO" in delete1[0][2].upper():
        query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {deleteID1}){quantityDeleteTobacco} WHERE Codigo_Venda = {deleteID1}"
        conn.execute(query)
        conn.connection.commit()
    else:
        query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {deleteID1}){quantityDelete} WHERE Codigo_Venda = {deleteID1}"
        conn.execute(query)
        conn.connection.commit()
    if "TABACO" in delete2[0][2].upper():
        query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {deleteID2}){quantityDeleteTobacco} WHERE Codigo_Venda = {deleteID2}"
        conn.execute(query)
        conn.connection.commit()
    else:
        query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {deleteID2}){quantityDelete} WHERE Codigo_Venda = {deleteID2}"
        conn.execute(query)
        conn.connection.commit()
    if "TABACO" in delete3[0][2].upper():
        query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {deleteID3}){quantityDeleteTobacco} WHERE Codigo_Venda = {deleteID3}"
        conn.execute(query)
        conn.connection.commit()
    else:
        query = f"UPDATE stock SET Quantidade = (SELECT Quantidade FROM stock WHERE Codigo_Venda = {deleteID3}){quantityDelete} WHERE Codigo_Venda = {deleteID3}"
        conn.execute(query)
        conn.connection.commit()
    message = True
    return message


#Function to delete a specific payment
def delete_Table_Payments(deletePayment):
    check = consult_Tables("payments", "Numero_Pedido", [deletePayment])
    if check is True:
        message = "Nenhum item correspondente encontrado."
        return message
    else:
        message = up_Stock(check)
        if message is True:
            #Deleting the data from payments table
            conn = databaseConnection()
            conn.execute("DELETE FROM payments WHERE Numero_Pedido = ?", [deletePayment])
            conn.connection.commit()
            message = "Registro de pagamento deletado com sucesso."
        else:
            message = "Erro desconhecido."
        return message