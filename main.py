from users import append_Table_Users
import requests
import time
import os

print("=-="*12)
print("""
Bem-vindo(a) ao sistema GoldLife
""")
print("=-="*12)
time.sleep(3)
notAfraid = False
while notAfraid is False:
    user = str(input("""Usuário: """))
    try:
        while notAfraid is False:
            message = append_Table_Users([user])
            print("=-="*12)
            print("""[1] Usuários
[2] Clientes
[3] Estoque
[4] Pagamentos
[0] Sair""")
            print("=-="*12)
            option = input(str("""Digite um dos números entre colchetes para realizar uma operação na respectiva tabela: """))
            if option.upper().strip() in ["1", "2", "3", "4"]:
                while notAfraid is False:
                    print("=-="*12)
                    print("""[C] Create
[R] Read
[U] Update
[D] Delete
[0] Voltar""")
                    print("=-="*12)
                    crud = input(str("Digite uma das letras entre colchetes para realizar uma operação CRUD: "))
                    if option.upper().strip() == "1":
                        if crud.upper().strip() == "C":
                            while notAfraid is False:
                                createUserList = []
                                print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        document = input(str("CPF/CNPJ: ")).replace(".", "").replace("-", "").replace("/", "")
                                        document = int(document)
                                        break
                                    except:
                                        print("=-="*12)
                                        print("São permitidos apenas caracteres númericos e de formatação. Tente novamente.")
                                        print("=-="*12)
                                createUserList.append(str(document))
                                createUserList.append(input(str("Nome Completo: ")))
                                createUserList.append(input(str("Email: ")))
                                apiList = {"user": user, "userAppend": createUserList}
                                message = requests.post("http://localhost:1000/users", json=apiList)
                                print("=-="*12)
                                print(message.text)
                                time.sleep(2)
                                break
                        elif crud.upper().strip() == "R":
                            while notAfraid is False:
                                print("=-="*12)
                                print("""[U] Relatório de um único usuário
[T] Relatório com todos usuários
[0] Voltar""")
                                print("=-="*12)
                                option1 = input(str("Digite a respectiva letra do relatório que você deseja: "))
                                if option1.upper().strip() in ["U", "T"]:
                                    print("=-="*12)
                                    email = input(str("Digite o email para envio do relatório: "))
                                    if option1.upper().strip() == "U":
                                        userConsult = input(str("Digite o código do usuário que deseja pesquisar: "))
                                        apiList = {"user": user, "emailReport": email, "userConsult": userConsult}
                                        message = requests.post("http://localhost:1000/users", json=apiList)
                                        print("=-="*12)
                                        print(message.text)
                                        time.sleep(2)
                                        break
                                    elif option1.upper().strip() == "T":
                                        apiList = {"user": user, "emailReport": email}
                                        message = requests.post("http://localhost:1000/users", json=apiList)
                                        print("=-="*12)
                                        print(message.text)
                                        time.sleep(2)
                                        break
                                elif option1.strip() == "0":
                                    break
                        elif crud.upper().strip() == "U":
                            while notAfraid is False:
                                updateUserList = []
                                print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        alterDocument = input(str("Digite o Código do usuário que deseja atualizar: ")).replace(".", "").replace("-", "").replace("/", "")
                                        alterDocument = int(alterDocument)
                                        try:
                                            message = append_Table_Users([str(alterDocument)])
                                        except:
                                            print("=-="*12)
                                            print("Este usuário não existe.")
                                            print("=-="*12)
                                            continue
                                        break
                                    except:
                                        print("=-="*12)
                                        print("São permitidos apenas caracteres númericos e de formatação. Tente novamente.")
                                        print("=-="*12)
                                updateUserList.append(str(alterDocument))
                                updateUserList.append(input(str("Nome Completo: ")))
                                updateUserList.append(input(str("Email: ")))
                                apiList = {"user": user, "userUpdate": updateUserList}
                                message = requests.post("http://localhost:1000/users", json=apiList)
                                print("=-="*12)
                                print(message.text)
                                time.sleep(2)
                                break
                        elif crud.upper().strip() == "D":
                            userPop = input(str("Digite o código do usuário que deseja deletar: "))
                            apiList = {"user": user, "userPop": userPop}
                            message = requests.post("http://localhost:1000/users", json=apiList)
                            print("=-="*12)
                            print(message.text)
                            time.sleep(2)
                        elif crud.strip() == "0":
                            break
                    elif option.upper().strip() == "2":
                        if crud.upper().strip() == "C":
                            while notAfraid is False:
                                createClientList = []
                                print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        document = input(str("CPF/CNPJ: ")).replace(".", "").replace("-", "").replace("/", "")
                                        document = int(document)
                                        break
                                    except:
                                        print("=-="*12)
                                        print("São permitidos apenas caracteres númericos e de formatação. Tente novamente.")
                                        print("=-="*12)
                                createClientList.append(str(document))
                                createClientList.append(input(str("Nome Completo: ")))
                                createClientList.append(input(str("Email: ")))
                                createClientList.append(input(str("Telefone: ")))
                                createClientList.append(input(str("Logradouro: ")))
                                apiList = {"user": user, "client": createClientList}
                                message = requests.post("http://localhost:2000/clients", json=apiList)
                                print("=-="*12)
                                print(message.text)
                                time.sleep(2)
                                break
                        elif crud.upper().strip() == "R":
                            while notAfraid is False:
                                print("=-="*12)
                                print("""[U] Relatório de um único cliente
[T] Relatório com todos clientes
[0] Voltar""")
                                print("=-="*12)
                                option2 = input(str("Digite a respectiva letra do relatório que você deseja: "))
                                if option2.upper().strip() in ["U", "T"]:
                                    print("=-="*12)
                                    email = input(str("Digite o email para envio do relatório: "))
                                    if option2.upper().strip() == "U":
                                        clientConsult = input(str("Digite o código do cliente que deseja pesquisar: "))
                                        apiList = {"user": user, "emailReport": email, "CPF/CNPJ": clientConsult}
                                        message = requests.post("http://localhost:2000/clients", json=apiList)
                                        print("=-="*12)
                                        print(message.text)
                                        time.sleep(2)
                                        break
                                    elif option2.upper().strip() == "T":
                                        apiList = {"user": user, "emailReport": email}
                                        message = requests.post("http://localhost:2000/clients", json=apiList)
                                        print("=-="*12)
                                        print(message.text)
                                        time.sleep(2)
                                        break
                                    elif option2.strip() == "0":
                                        break
                        elif crud.upper().strip() == "U":
                            while notAfraid is False:
                                updateClientList = []
                                print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        alterDocument = input(str("Digite o Código do cliente que deseja atualizar: ")).replace(".", "").replace("-", "").replace("/", "")
                                        alterDocument = int(alterDocument)
                                        break
                                    except:
                                        print("=-="*12)
                                        print("São permitidos apenas caracteres númericos e de formatação. Tente novamente.")
                                        print("=-="*12)
                                updateClientList.append(str(alterDocument))
                                updateClientList.append(input(str("Nome Completo: ")))
                                updateClientList.append(input(str("Email: ")))
                                updateClientList.append(input(str("Telefone: ")))
                                updateClientList.append(input(str("Logradouro: ")))
                                apiList = {"user": user, "updateClient": updateClientList}
                                message = requests.post("http://localhost:2000/clients", json=apiList)
                                print("=-="*12)
                                print(message.text)
                                time.sleep(2)
                                break
                        elif crud.upper().strip() == "D":
                            userPop = input(str("Digite o código do cliente que deseja deletar: "))
                            apiList = {"user": user, "CPF/CNPJ": userPop}
                            message = requests.post("http://localhost:2000/clients", json=apiList)
                            print("=-="*12)
                            print(message.text)
                            time.sleep(2)
                        elif crud.strip() == "0":
                            break
                    elif option.upper().strip() == "3":
                        if crud.upper().strip() == "C":
                            while notAfraid is False:
                                createStockItemList = []
                                print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        createStockItemList.append(int(input("Codigo do produto: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Código produto deve ser um valor numérico inteiro, tente novamente.")
                                        print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        createStockItemList.append(int(input("Codigo de venda: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Código venda deve ser um valor numérico inteiro, tente novamente.")
                                        print("=-="*12)
                                createStockItemList.append(input(str("Nome produto: ").replace(" ", "_")))
                                while notAfraid is False:
                                    try:
                                        createStockItemList.append(float(input("Quantidade: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Quantidade deve ser um valor numérico, tente novamente.")
                                        print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        createStockItemList.append(float(input("Valor total: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Valor total deve ser um valor numérico, tente novamente.")
                                        print("=-="*12)
                                createStockItemList.append(input(str("Descrição: ")))
                                apiList = {"user": user, "productAppend": createStockItemList}
                                message = requests.post("http://localhost:3000/stock", json=apiList)
                                print("=-="*12)
                                print(message.text)
                                time.sleep(2)
                                break
                        elif crud.upper().strip() == "R":
                            email = input(str("Digite o email para envio do relatório: "))
                            apiList = {"user": user, "emailReport": email}
                            message = requests.post("http://localhost:3000/stock", json=apiList)
                            print("=-="*12)
                            print(message.text)
                            time.sleep(2)
                            continue
                        elif crud.upper().strip() == "U":
                            updateStockItemList = []
                            while notAfraid is False:
                                try:
                                    updateStockItemList.append(int(input("Codigo de venda: ")))
                                    break
                                except:
                                    print("=-="*12)
                                    print("Código venda deve ser um valor numérico inteiro, tente novamente.")
                                    print("=-="*12)
                            while notAfraid is False:
                                try:
                                    updateStockItemList.append(float(input("Quantidade: ")))
                                    break
                                except:
                                    print("=-="*12)
                                    print("Quantidade deve ser um valor numérico, tente novamente.")
                                    print("=-="*12)
                            while notAfraid is False:
                                try:
                                    updateStockItemList.append(float(input("Valor total: ")))
                                    break
                                except:
                                    print("=-="*12)
                                    print("Valor total deve ser um valor numérico, tente novamente.")
                                    print("=-="*12)
                            apiList = {"user": user, "updateStock": updateStockItemList}
                            message = requests.post("http://localhost:3000/stock", json=apiList)
                            print("=-="*12)
                            print(message.text)
                            time.sleep(2)
                            break
                        elif crud.upper().strip() == "D":
                            while notAfraid is False:
                                try:
                                    productDeleteList = []
                                    productDeleteList.append(int(input("Digite o código de venda do produto que deseja deletar: ")))
                                    break
                                except:
                                    print("=-="*12)
                                    print("Código venda deve ser um valor numérico inteiro, tente novamente.")
                                    print("=-="*12)
                            apiList = {"user": user, "productDelete": productDeleteList}
                            message = requests.post("http://localhost:3000/stock", json=apiList)
                            print("=-="*12)
                            print(message.text)
                            time.sleep(2)
                        elif crud.strip() == "0":
                            break
                    elif option.upper().strip() == "4":
                        if crud.upper().strip() == "C":
                            while notAfraid is False:
                                createPaymentList = []
                                kitList = []
                                print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        document = input(str("Código do cliente (CPF/CNPJ): ")).replace(".", "").replace("-", "").replace("/", "")
                                        document = int(document)
                                        createPaymentList.append(str(document))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("São permitidos apenas caracteres númericos e de formatação. Tente novamente.")
                                        print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        kitList.append(int(input("Codigo de venda do 1º item do kit: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Código venda deve ser um valor numérico inteiro, tente novamente.")
                                        print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        kitList.append(int(input("Codigo de venda do 2º item do kit: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Código venda deve ser um valor numérico inteiro, tente novamente.")
                                        print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        kitList.append(int(input("Codigo de venda do 3º item do kit: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Código venda deve ser um valor numérico inteiro, tente novamente.")
                                        print("=-="*12)
                                createPaymentList.append(kitList)
                                while notAfraid is False:
                                    try:
                                        createPaymentList.append(int(input("Nº de kits do pedido: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Quantidade deve ser um valor numérico inteiro, tente novamente.")
                                        print("=-="*12)
                                while notAfraid is False:
                                    try:
                                        createPaymentList.append(float(input("Valor de venda: ")))
                                        break
                                    except:
                                        print("=-="*12)
                                        print("Valor total deve ser um valor numérico, tente novamente.")
                                        print("=-="*12)
                                createPaymentList.append(input(str("Tipo pagamento: ")))
                                createPaymentList.append(input(str("Data do pagamento: ")))
                                apiList = {"user": user, "paymentAppend": createPaymentList}
                                message = requests.post("http://localhost:4000/payments", json=apiList)
                                print("=-="*12)
                                print(message.text)
                                time.sleep(2)
                                break
                        elif crud.upper().strip() == "R":
                            email = input(str("Digite o email para envio do relatório: "))
                            apiList = {"user": user, "emailReport": email}
                            message = requests.post("http://localhost:4000/payments", json=apiList)
                            print("=-="*12)
                            print(message.text)
                            time.sleep(2)
                            continue
                        elif crud.upper().strip() == "U":
                            while notAfraid is False:
                                updatePaymentList = []
                                updatePaymentList.append(str(input("Nº do pedido: ")))
                                updatePaymentList.append(input(str("Tipo pagamento: ")))
                                updatePaymentList.append(input(str("Data do pagamento: ")))
                                apiList = {"user": user, "paymentUpdate": updatePaymentList}
                                message = requests.post("http://localhost:4000/payments", json=apiList)
                                print("=-="*12)
                                print(message.text)
                                time.sleep(2)
                                break
                        elif crud.upper().strip() == "D":
                            paymentDelete = input(str("Digite o código de venda do produto que deseja deletar: "))
                            apiList = {"user": user, "paymentDelete": paymentDelete}
                            message = requests.post("http://localhost:4000/payments", json=apiList)
                            print("=-="*12)
                            print(message.text)
                            time.sleep(2)
                        elif crud.strip() == "0":
                            break
                    else:
                        continue
            elif option.upper().strip() == "0":
                os._exit(0)
            else:
                continue
    except:
        print("=-="*12)
        print("Este usuário não existe. Tente novamente.")
        print("=-="*12)
        continue
print("=-="*12)