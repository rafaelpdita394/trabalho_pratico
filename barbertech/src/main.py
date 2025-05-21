import os

USUARIOS_FILE = 'usuarios.txt'
SERVICOS_FILE = 'servicos.txt'

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")

def carregar_usuarios():
    usuarios = []
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(',')
                if len(partes) == 3:
                    nome, senha, tipo = partes
                    usuarios.append({"nome": nome, "senha": senha, "tipo": tipo})
    return usuarios

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
        for u in usuarios:
            f.write(f"{u['nome']},{u['senha']},{u['tipo']}\n")

def cadastrar_usuario():
    limpar_tela()
    print("=== Cadastro de Usuário ===")
    nome = input("Nome: ").strip()
    senha = input("Senha: ").strip()
    tipo = input("Tipo (gerente/funcionario): ").strip().lower()
    if tipo not in ('gerente', 'funcionario'):
        print("Tipo inválido!")
        pausar()
        return
    usuarios = carregar_usuarios()
    if any(u['nome'] == nome for u in usuarios):
        print("Usuário já existe!")
        pausar()
        return
    usuarios.append({"nome": nome, "senha": senha, "tipo": tipo})
    salvar_usuarios(usuarios)
    print("Usuário cadastrado com sucesso!")
    pausar()

def login():
    usuarios = carregar_usuarios()
    print("=== Login ===")
    nome = input("Nome: ").strip()
    senha = input("Senha: ").strip()
    for u in usuarios:
        if u['nome'] == nome and u['senha'] == senha:
            return u
    print("Usuário ou senha inválidos!")
    pausar()
    return None

def carregar_servicos():
    servicos = []
    if os.path.exists(SERVICOS_FILE):
        with open(SERVICOS_FILE, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(',')
                if len(partes) == 4:
                    codigo, nome, preco, quantidade = partes
                    try:
                        servicos.append({
                            "codigo": int(codigo),
                            "nome": nome,
                            "preco": float(preco),
                            "quantidade": int(quantidade)
                        })
                    except ValueError:
                        continue
    return servicos

def salvar_servicos(servicos):
    with open(SERVICOS_FILE, 'w', encoding='utf-8') as f:
        for s in servicos:
            f.write(f"{s['codigo']},{s['nome']},{s['preco']},{s['quantidade']}\n")

def cadastrar_servico():
    limpar_tela()
    print("=== Cadastro de Serviço ===")
    try:
        codigo = int(input("Código: ").strip())
        nome = input("Nome: ").strip()
        preco = float(input("Preço: ").strip())
        quantidade = int(input("Quantidade: ").strip())
    except ValueError:
        print("Entrada inválida!")
        pausar()
        return
    servicos = carregar_servicos()
    if any(s['codigo'] == codigo for s in servicos):
        print("Código já cadastrado!")
        pausar()
        return
    servicos.append({"codigo": codigo, "nome": nome, "preco": preco, "quantidade": quantidade})
    salvar_servicos(servicos)
    print("Serviço cadastrado com sucesso!")
    pausar()

def listar_servicos():
    limpar_tela()
    print("=== Lista de Serviços ===")
    servicos = carregar_servicos()
    if not servicos:
        print("Nenhum serviço cadastrado.")
    else:
        for s in servicos:
            print(f"Código: {s['codigo']} | Nome: {s['nome']} | Preço: R${s['preco']:.2f} | Quantidade: {s['quantidade']}")
    pausar()

def excluir_servico():
    limpar_tela()
    print("=== Excluir Serviço ===")
    try:
        codigo = int(input("Informe o código do serviço a ser excluído: ").strip())
    except ValueError:
        print("Código inválido!")
        pausar()
        return
    servicos = carregar_servicos()
    novos_servicos = [s for s in servicos if s['codigo'] != codigo]
    if len(novos_servicos) == len(servicos):
        print("Serviço não encontrado!")
    else:
        salvar_servicos(novos_servicos)
        print("Serviço excluído com sucesso!")
    pausar()

def excluir_usuario():
    limpar_tela()
    print("=== Excluir Usuário ===")
    nome = input("Informe o nome do usuário a ser excluído: ").strip()
    usuarios = carregar_usuarios()
    novos_usuarios = [u for u in usuarios if u['nome'] != nome]
    if len(novos_usuarios) == len(usuarios):
        print("Usuário não encontrado!")
    else:
        salvar_usuarios(novos_usuarios)
        print("Usuário excluído com sucesso!")
    pausar()

def menu_principal(usuario):
    while True:
        limpar_tela()
        print(f"Bem-vindo(a), {usuario['nome']} ({usuario['tipo']})")
        print("\n1 - Cadastrar Serviço")
        print("2 - Listar Serviços")
        if usuario['tipo'] == 'gerente':
            print("3 - Cadastrar Usuário")
            print("4 - Excluir Serviço")
            print("5 - Excluir Usuário")
        print("0 - Sair")

        op = input("Escolha: ").strip()

        if op == '1':
            cadastrar_servico()
        elif op == '2':
            listar_servicos()
        elif op == '3' and usuario['tipo'] == 'gerente':
            cadastrar_usuario()
        elif op == '4' and usuario['tipo'] == 'gerente':
            excluir_servico()
        elif op == '5' and usuario['tipo'] == 'gerente':
            excluir_usuario()
        elif op == '0':
            break
        else:
            print("Opção inválida!")
            pausar()

def main():
    while True:
        limpar_tela()
        print("=== BarberTech - Sistema CRUD ===")
        print("1 - Login")
        print("2 - Cadastrar Usuário (primeiro acesso)")
        print("0 - Sair")
        op = input("Escolha: ").strip()

        if op == '1':
            usuario = login()
            if usuario:
                menu_principal(usuario)
        elif op == '2':
            cadastrar_usuario()
        elif op == '0':
            break
        else:
            print("Opção inválida!")
            pausar()

if __name__ == '__main__':
    main()