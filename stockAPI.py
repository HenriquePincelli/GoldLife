from flask import Flask, jsonify, request, json
from stock import consult_Stock, consult_Tables, append_Table_Stock, delete_Stock, update_Stock
from functions import make_Files, send_Email
from servers import create_Table_Stock
import pandas


#Creating a server for the application
create_Table_Stock()
app = Flask(__name__)


@app.route("/stock", methods=["POST"])
def stockAPI():
    #Catch the data from the request
    requestAPI = request.get_json()

    #Check if the user is in database
    result = consult_Tables("users", "Codigo_Usuario", [requestAPI["user"].replace(".", "").replace("-", "").replace("/", "")])
    if result is True:
        result = "Este usuario nao existe. Verifique suas credenciais."
        return result
    else:
        if "productAppend" in requestAPI.keys():
            result = append_Table_Stock(requestAPI["productAppend"])
        elif "emailReport" in requestAPI.keys():
            result = consult_Stock()
            if len(result) == 0:
                result = "O estoque esta vazio."
            else:
                reportOption = "Estoque"
        elif "updateStock" in requestAPI.keys():
            result = update_Stock(requestAPI["updateStock"])
        elif "productDelete" in requestAPI.keys():
            result = delete_Stock(requestAPI["productDelete"])
        else:
            result = "Verifique os parametros inseridos e tente novamente."

    try:
        df = pandas.DataFrame(result)
        df = df.set_axis(["Codigo_Produto", "Codigo_Venda", "Nome_Produto", "Quantidade", "Preco_Medio_Unitario", "Descricao"], axis='columns')
        reportName = make_Files(2, df)
        send_Email(2, reportOption, reportName, requestAPI["emailReport"])    
        return jsonify(json.dumps(result))
    except ValueError:
        return jsonify(json.dumps(result))


#Parameters of the local server
app.run(port=3000, host="localhost", debug=True)