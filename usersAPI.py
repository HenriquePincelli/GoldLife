from flask import Flask, jsonify, request, json
from users import consult_Table_Users, append_Table_Users, pop_Table_Users, update_Table_Users
from functions import make_Files, send_Email
from servers import create_Table_Users
import pandas


#Creating a server for the application
create_Table_Users()
app = Flask(__name__)


@app.route("/users", methods=["POST"])
def usersAPI():
    #Catch the data from the request
    requestAPI = request.get_json()

    #Check if the user is in database
    option = "Verificação de usuário"
    message = consult_Table_Users(option, [requestAPI["user"].replace(".", "").replace("-", "").replace("/", "")])
    if message == "Este usuario ja existe. Por gentileza, verifique os dados inseridos e tente novamente.":
        if "userAppend" in requestAPI.keys():
            result = append_Table_Users(requestAPI["userAppend"])
        elif "userUpdate" in requestAPI.keys():
            result = update_Table_Users(requestAPI["userUpdate"])
        elif "userPop" in requestAPI.keys():
            result = pop_Table_Users([requestAPI["userPop"]])
        elif "userConsult" in requestAPI.keys():
            result = consult_Table_Users("userConsult", [requestAPI["userConsult"]])
            if result == "Nenhum resultado encontrado.":
                message = "Por gentileza, verifique os parametros fornecidos e tente novamente."
        elif len(requestAPI) == 2:
            option = "Usuários"
            result = consult_Table_Users(option)
        else:
            message = "Por gentileza, verifique os parametros fornecidos e tente novamente."
    else:
        return message
    
    try:
        df = pandas.DataFrame(result)
        df = df.set_axis(["Codigo_Usuario", "Nome", "Email", "Data_Criacao"], axis='columns')
        reportName = make_Files(0, df)
        send_Email(0, option, reportName, requestAPI["emailReport"])    
        return jsonify(json.dumps(result))
    except ValueError:
        return jsonify(json.dumps(result))
        

#Parameters of the local server
app.run(port=1000, host="localhost", debug=True)