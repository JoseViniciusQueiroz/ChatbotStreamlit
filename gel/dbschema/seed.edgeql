# =====================
# GERENTES
# =====================

insert Gerente {
    cpfPessoa := "11111111111",
    nomePessoa := "Carlos Silva",
    senhaPessoa := "123",
    emailGerente := "carlos@empresa.com",
    formacaoGerente := Formacao.superior
};

insert Gerente {
    cpfPessoa := "22222222222",
    nomePessoa := "Ana Souza",
    senhaPessoa := "123",
    emailGerente := "ana@empresa.com",
    formacaoGerente := Formacao.medio
};

# =====================
# AREAS
# =====================

insert Area {
    nomeArea := "Financeiro",
    gerente := (
        select Gerente
        filter .cpfPessoa = "11111111111"
    )
};

insert Area {
    nomeArea := "Tecnologia",
    gerente := (
        select Gerente
        filter .cpfPessoa = "22222222222"
    )
};

# =====================
# PRODUTOS
# =====================

insert Produto {
    nomeProduto := "Notebook",
    areas := (
        select Area filter .nomeArea = "Tecnologia"
    )
};

insert Produto {
    nomeProduto := "Calculadora",
    areas := (
        select Area filter .nomeArea = "Financeiro"
    )
};

# =====================
# EMPREGADOS
# =====================

insert Empregado {
    cpfPessoa := "33333333333",
    nomePessoa := "João Pedro",
    senhaPessoa := "123",
    matriculaEmpregador := "EMP001",
    telefone := {"61999999999", "61888888888"},
    endereco := (
        insert Endereco {
            rua := "Rua A",
            cep := "70000000",
            numero := 10
        }
    ),
    areas := (
        select Area filter .nomeArea = "Tecnologia"
    )
};

insert Empregado {
    cpfPessoa := "44444444444",
    nomePessoa := "Maria Clara",
    senhaPessoa := "123",
    matriculaEmpregador := "EMP002",
    telefone := {"61777777777"},
    endereco := (
        insert Endereco {
            rua := "Rua B",
            cep := "71000000",
            numero := 20
        }
    ),
    areas := (
        select Area filter .nomeArea = "Financeiro"
    )
};

# =====================
# NOTAS FISCAIS
# =====================



insert NotaFiscal {
    empregado := (
        select Empregado
        filter .matriculaEmpregador = "EMP002"
    ),
    data := <cal::local_date>"2026-04-20",

    itens := {
        (insert ItemNota {
            produto := (
                select Produto
                filter .nomeProduto = "Calculadora"
                limit 1
            ),
            qtdVenda := 3,
            precoUnid := <decimal>50.0
        })
    }
};

update NotaFiscal
filter .empregado.matriculaEmpregador = "EMP002"
set {
    itens += (
        insert ItemNota {
            produto := (
                select Produto
                filter .nomeProduto = "Notebook"
                limit 1
            ),
            qtdVenda := 1,
            precoUnid := <decimal>100.0
        }
    )
};