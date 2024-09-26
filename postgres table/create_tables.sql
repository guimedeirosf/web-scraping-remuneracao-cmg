DROP TABLE FatoPagamento;
DROP TABLE DimFuncionario;
DROP TABLE DimLotacao;
DROP TABLE DimCargo;
DROP TABLE DimTipoAdmissao;
DROP TABLE DimLocalidade;
DROP TABLE DimTipoPagamento;

CREATE TABLE DimLotacao (
    LotacaoID SERIAL PRIMARY KEY,
    Lotacao VARCHAR(100) NOT NULL 
    --Movimentacao VARCHAR(100)  
);



CREATE TABLE DimCargo (
    CargoID SERIAL PRIMARY KEY,
    Cargo VARCHAR(100) NOT NULL,  
    Funcao VARCHAR(100)  
);

CREATE TABLE DimTipoAdmissao (
    TipoAdmissaoID SERIAL PRIMARY KEY,
    TipoAdmissao VARCHAR(100) NOT NULL,  
    Estabilidade BOOLEAN  
);



CREATE TABLE DimTipoPagamento (
    TipoPagamentoID SERIAL PRIMARY KEY,
    TipoPagamento VARCHAR(50) NOT NULL  
);

CREATE TABLE DimLocalidade (
    LocalidadeID SERIAL PRIMARY KEY,
    Cidade VARCHAR(100) NOT NULL,  
    Estado VARCHAR(50) NOT NULL,  
    Pais VARCHAR(50) NOT NULL 
);

CREATE TABLE DimFuncionario (
    FuncionarioID SERIAL PRIMARY KEY,
    Matricula VARCHAR(50) UNIQUE NOT NULL,  
    Nome VARCHAR(100) NOT NULL,
    DataAdmissao DATE NOT NULL,  
    TipoAdmissaoID INT REFERENCES DimTipoAdmissao(TipoAdmissaoID),  -- Chave para DimTipoAdmissao
    CargoID INT REFERENCES DimCargo(CargoID),  -- Chave para DimCargo
    LotacaoID INT REFERENCES DimLotacao(LotacaoID)   -- Chave para DimTipoAdmissao
);


CREATE TABLE FatoPagamento (
    PagamentoID SERIAL PRIMARY KEY,
    FuncionarioID INT REFERENCES DimFuncionario(FuncionarioID), -- Chave para DimFuncionario
    Decreto VARCHAR(100),  
    SalarioBase DECIMAL(10, 2), 
    TotalProventos DECIMAL(10, 2),  
    TotalDescObrigatorios DECIMAL(10, 2),  
    TipoPagamentoID INT REFERENCES DimTipoPagamento(TipoPagamentoID),  -- Chave para DimTipoPagamento
    LocalidadeID INT REFERENCES DimLocalidade(LocalidadeID),  -- Chave para DimLocalidade
    Ano INT NOT NULL,  
    Mes INT NOT NULL 
);

