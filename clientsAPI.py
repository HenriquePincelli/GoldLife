from flask import Flask, jsonify, request, json
from clients import consult_Tables, append_Table_Clients, return_Tables, all_Clients, delete_Client
from functions import makeFiles, sendEmail
import pandas


#Creating a server for the application
app = Flask(__name__)


@app.route("/clients", methods=["POST"])
def clientsAPI():
    #Catch the data from the request
    requestAPI = request.get_json()

    #Check if the user is in database
    result = consult_Tables("users", "Codigo_Usuario", [requestAPI["user"].replace(".", "").replace("-", "").replace("/", "")])
    if result is False:
        if "client" in requestAPI.keys():
            result = consult_Tables("clients", "CPF_CNPJ", [requestAPI["client"][0].replace(".", "").replace("-", "").replace("/", "")])
            if result is True:
                result = append_Table_Clients(requestAPI["client"])
            else:
                result = "Este cliente ja esta cadastrado."
        elif "emailReport" in requestAPI.keys() and "CPF/CNPJ" in requestAPI.keys():
            result = consult_Tables("clients", "CPF_CNPJ", [requestAPI["CPF/CNPJ"].replace(".", "").replace("-", "").replace("/", "")])
            if result is True:
                result = "Este cliente nao esta cadastrado."
            else:
                reportOption = "Cliente"
                result = return_Tables("clients", "CPF_CNPJ", [requestAPI["CPF/CNPJ"].replace(".", "").replace("-", "").replace("/", "")])
        elif "emailReport" in requestAPI.keys():
            reportOption = "Clientes"
            result = all_Clients()
        elif "CPF/CNPJ" in requestAPI.keys():
            result = consult_Tables("clients", "CPF_CNPJ", [requestAPI["CPF/CNPJ"].replace(".", "").replace("-", "").replace("/", "")])
            if result is True:
                result = "Este cliente nao esta cadastrado."
            else:
                result = delete_Client([requestAPI["CPF/CNPJ"].replace(".", "").replace("-", "").replace("/", "")])
        else:
            result = "Por gentileza, verifique os parametros fornecidos e tente novamente."
    else:
        result = "Este usuario nao existe. Verifique suas credenciais."
        return result

    try:
        df = pandas.DataFrame(result)
        df = df.set_axis(["CPF_CNPJ", "Nome_Completo", "Email", "Telefone", "Logradouro", "Nº Pedidos Feitos", "Nº Pedidos Concluídos", "Data_Cadastro"], axis='columns')
        reportName = makeFiles(1, df)
        sendEmail(1, reportOption, reportName, requestAPI["emailReport"])    
        return jsonify(json.dumps(result))
    except ValueError:
        return jsonify(json.dumps(result))
        

#Parameters of the local server
app.run(port=5000, host="localhost", debug=True)