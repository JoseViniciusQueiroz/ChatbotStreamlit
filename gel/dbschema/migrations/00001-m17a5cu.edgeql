CREATE MIGRATION m17a5cu3syfted2rqq24vx6ond2fndlsms42tnfmjnwp7sgc422atq
    ONTO initial
{
  CREATE SCALAR TYPE default::Formacao EXTENDING enum<primario, medio, superior>;
  CREATE FUTURE no_linkful_computed_splats;
  CREATE TYPE default::Pessoa {
      CREATE REQUIRED PROPERTY cpfPessoa: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY nomePessoa: std::str;
      CREATE REQUIRED PROPERTY senhaPessoa: std::str;
  };
  CREATE TYPE default::Gerente EXTENDING default::Pessoa {
      CREATE REQUIRED PROPERTY emailGerente: std::str;
      CREATE REQUIRED PROPERTY formacaoGerente: default::Formacao;
  };
  CREATE TYPE default::Area {
      CREATE LINK gerente: default::Gerente;
      CREATE REQUIRED PROPERTY nomeArea: std::str;
  };
  CREATE TYPE default::Endereco {
      CREATE PROPERTY cep: std::str;
      CREATE PROPERTY numero: std::int16;
      CREATE PROPERTY rua: std::str;
  };
  CREATE TYPE default::Empregado EXTENDING default::Pessoa {
      CREATE MULTI LINK areas: default::Area;
      CREATE REQUIRED LINK endereco: default::Endereco;
      CREATE REQUIRED PROPERTY matriculaEmpregador: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED MULTI PROPERTY telefone: std::str;
  };
  CREATE TYPE default::Produto {
      CREATE MULTI LINK areas: default::Area;
      CREATE REQUIRED PROPERTY nomeProduto: std::str;
  };
  CREATE TYPE default::ItemNota {
      CREATE REQUIRED LINK produto: default::Produto;
      CREATE REQUIRED PROPERTY precoUnid: std::decimal;
      CREATE REQUIRED PROPERTY qtdVenda: std::int16;
  };
  CREATE TYPE default::NotaFiscal {
      CREATE REQUIRED LINK empregado: default::Empregado;
      CREATE MULTI LINK itens: default::ItemNota;
      CREATE REQUIRED PROPERTY data: std::cal::local_date;
  };
};
