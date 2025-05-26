# modules/utils.py
def validar_campos_obrigatorios(dados):
    campos_obrigatorios = [
        "NIF", "Nome", "Email", "Data_Nascimento",
        "Profissão", "Empresa", "Telefone", "Morada"
    ]
    erros = []
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            erros.append(f"Campo obrigatório '{campo}' não preenchido.")
    return erros