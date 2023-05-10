from flask import Flask, jsonify, request, json
from payments import consult_Tables, consult_Payments, append_Table_Payments, delete_Table_Payments, update_Table_Payments
from functions import make_Files, send_Email
from servers import create_Table_Payments
import pandas


#Creating a server for the application
create_Table_Payments()
app = Flask(__name__)


@app.route("/payments", methods=["POST"])
def paymentsAPI():
    #Catch the data from the request
    requestAPI = request.get_json()

    #Check if the user is in database
    result = consult_Tables("users", "Codigo_Usuario", [requestAPI["user"].replace(".", "").replace("-", "").replace("/", "")])
    if result is True:
        result = "Este usuario nao existe. Verifique suas credenciais."
        return result
    else:
        if "paymentAppend" in requestAPI.keys():
            result = append_Table_Payments(requestAPI["paymentAppend"])
        elif "emailReport" in requestAPI.keys():
            result = consult_Payments()
            if len(result) == 0:
                result = "O estoque esta vazio."
            else:
                reportOption = "Pagamentos"
        elif "paymentUpdate" in requestAPI.keys():
            result = update_Table_Payments(requestAPI["paymentUpdate"])
        elif "paymentDelete" in requestAPI.keys():
            result = delete_Table_Payments(requestAPI["paymentDelete"])
        else:
            result = "Verifique os parametros inseridos e tente novamente."

    try:
        df = pandas.DataFrame(result)
        df = df.set_axis(["Numero_Pedido", "CPF_CNPJ", "Produtos", "Quantidade", "Valor_Pedido", "Forma_Pagamento", "Data_Pedido", "Data_Pagamento"], axis='columns')
        reportName = make_Files(3, df)
        send_Email(3, reportOption, reportName, requestAPI["emailReport"])    
        return jsonify(json.dumps(result))
    except ValueError:
        return jsonify(json.dumps(result))


#Parameters of the local server
app.run(port=4000, host="localhost", debug=True)