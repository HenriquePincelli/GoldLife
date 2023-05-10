import sqlite3


#Connecting with the database
def databaseConnection():
    connection = sqlite3.connect('GoldLifeDB.db', check_same_thread=False)
    conn = connection.cursor()
    return conn


#Function to create users table if not exists
def create_Table_Users():
    conn = databaseConnection()
    conn.execute("CREATE TABLE IF NOT EXISTS users(Codigo_Usuario INTEGER PRIMARY KEY, Nome_Completo TEXT NOT NULL, Email TEXT NOT NULL, Data_Criacao TEXT NOT NULL)")
    return
create_Table_Users()


#Function to create clients table if not exists
def create_Table_Clients():
    conn = databaseConnection()
    conn.execute("CREATE TABLE IF NOT EXISTS clients(CPF_CNPJ INTEGER PRIMARY KEY, Nome_Completo TEXT NOT NULL, Email TEXT NOT NULL, Telefone TEXT NOT NULL, Logradouro TEXT NOT NULL, Nº_Pedidos_Feitos INTEGER, Nº_Pedidos_Concluidos INTEGER, Data_Cadastro TEXT NOT NULL)")
    return
create_Table_Clients()


#Function to create stock table if not exists
def create_Table_Stock():
    conn = databaseConnection()
    conn.execute("CREATE TABLE IF NOT EXISTS stock(Codigo_Produto INTEGER NOT NULL, Codigo_Venda INTEGER PRIMARY KEY, Nome_Produto TEXT NOT NULL, Quantidade REAL NOT NULL, Preco_Medio_Unitario REAL NOT NULL, Descricao TEXT NOT NULL)")
    return
create_Table_Stock()


#Function to update "Nº_Pedidos_Feitos" and "Nº_Pedidos_Concluídos" of stock table
def stock_Updator():
    conn = databaseConnection()
    conn.execute("SELECT * FROM clients")
    rows = conn.fetchall()
    for h in range (len(rows)):
        query = f"SELECT Data_Pagamento FROM payments WHERE CPF_CNPJ = {rows[h][0]}"
        conn.execute(query)
        result = conn.fetchall()
        cont = 0
        for p in range (len(result)):
            if result[p][0] != "-":
                cont += 1
        query = f"UPDATE clients SET Nº_Pedidos_Feitos = {len(result)}, Nº_Pedidos_Concluidos = {cont} WHERE CPF_CNPJ = {rows[h][0]}"
        conn.execute(query)
        conn.connection.commit()
    return
stock_Updator()


#Function to create stock table if not exists
def create_Table_Payments():
    conn = databaseConnection()
    conn.execute("CREATE TABLE IF NOT EXISTS payments(Numero_Pedido TEXT PRIMARY KEY, CPF_CNPJ INTEGER, Produtos TEXT NOT NULL, Quantidade REAL NOT NULL, Valor_Pedido REAL NOT NULL, Forma_Pagamento TEXT, Data_Pedido TEXT NOT NULL, Data_Pagamento TEXT, FOREIGN KEY(CPF_CNPJ) REFERENCES clients (CPF_CNPJ))")
    return
create_Table_Payments()