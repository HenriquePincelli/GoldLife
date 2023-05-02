#Function to check if it's CPF(True)/CNPJ(False)
def isCPF(document: str) -> bool:
    TAMANHO_CPF = 11

    # Make the corrections on document length
    if len(document) < 11:
        correction = 11 - len(document)
        document = ("0" * correction) + document

    if len(document) != TAMANHO_CPF:
        return False

    if document in (c * TAMANHO_CPF for c in "1234567890"):
        return False

    cpf_reverso = document[::-1]
    for i in range(2, 0, -1):
        cpf_enumerado = enumerate(cpf_reverso[i:], start=2)
        dv_calculado = sum(map(lambda x: int(x[1]) * x[0], cpf_enumerado)) * 10 % 11
        if cpf_reverso[i - 1:i] != str(dv_calculado % 10):
            return False

    return True


def completeCPF(document):
    correction = 11 - len(document)
    documento = ("0" * correction) + document

    return documento


def completeCNPJ(document):
    correction = 14 - len(document)
    documento = ("0" * correction) + document

    return documento
    

def completaCPFouCNPJ(document):
    if isCPF(document):
        result = completeCPF(document)
    else:
        result = completeCNPJ(document)
    return result