-- -----------------------------------------------------
-- Drop das tabelas existentes (se houver)
-- -----------------------------------------------------
DROP TABLE IF EXISTS Ingresso CASCADE;
DROP TABLE IF EXISTS Vestimenta CASCADE;
DROP TABLE IF EXISTS Genero_Artista_Banda CASCADE;
DROP TABLE IF EXISTS Atracao CASCADE;
DROP TABLE IF EXISTS Evento CASCADE;
DROP TABLE IF EXISTS Disco CASCADE;
DROP TABLE IF EXISTS Genero_Colecao CASCADE;
DROP TABLE IF EXISTS Artista_Banda_Colecao CASCADE;
DROP TABLE IF EXISTS Featuring CASCADE;
DROP TABLE IF EXISTS Genero_Musica CASCADE;
DROP TABLE IF EXISTS Videoclipe CASCADE;
DROP TABLE IF EXISTS Musica_Colecao CASCADE;
DROP TABLE IF EXISTS Musica_Playlist CASCADE;
DROP TABLE IF EXISTS Transacao CASCADE;
DROP TABLE IF EXISTS Produto CASCADE;
DROP TABLE IF EXISTS Loja CASCADE;
DROP TABLE IF EXISTS Seguidor_Artista CASCADE;
DROP TABLE IF EXISTS Avaliacao CASCADE;
DROP TABLE IF EXISTS Artista_Banda CASCADE;
DROP TABLE IF EXISTS Produtora CASCADE;
DROP TABLE IF EXISTS Colecao_Favorita CASCADE;
DROP TABLE IF EXISTS Colecao CASCADE;
DROP TABLE IF EXISTS Reacao CASCADE;
DROP TABLE IF EXISTS Escutando CASCADE;
DROP TABLE IF EXISTS Musica CASCADE;
DROP TABLE IF EXISTS Genero_Favorito CASCADE;
DROP TABLE IF EXISTS Genero CASCADE;
DROP TABLE IF EXISTS Playlist_Salva CASCADE;
DROP TABLE IF EXISTS Playlist CASCADE;
DROP TABLE IF EXISTS Amizade CASCADE;
DROP TABLE IF EXISTS Ouvinte CASCADE;
DROP TABLE IF EXISTS Local CASCADE;

-- -----------------------------------------------------
-- Criar ENUM types
-- -----------------------------------------------------
CREATE TYPE sexo_enum AS ENUM ('M', 'F', 'NB');
CREATE TYPE tipo_colecao_enum AS ENUM ('Album', 'EP', 'Single', 'Compilacao');
CREATE TYPE tipo_disco_enum AS ENUM ('CD', 'Vinil', 'Fita');
CREATE TYPE tamanho_enum AS ENUM ('PP', 'P', 'M', 'G', 'GG', 'XGG');
CREATE TYPE tipo_ingresso_enum AS ENUM ('Normal', 'Premium');

-- -----------------------------------------------------
-- Tabela Local
-- -----------------------------------------------------
CREATE TABLE Local (
  id_local INTEGER GENERATED ALWAYS AS IDENTITY,
  nome VARCHAR(45) NOT NULL,
  estado VARCHAR(45) NOT NULL,
  pais VARCHAR(45) NOT NULL,
  logradouro VARCHAR(45) NOT NULL,
  numero VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_local)
);

-- -----------------------------------------------------
-- Tabela Ouvinte
-- -----------------------------------------------------
CREATE TABLE Ouvinte (
  id_usuario INTEGER GENERATED ALWAYS AS IDENTITY,
  email VARCHAR(30)[] NOT NULL,
  senha VARCHAR(30) NOT NULL,
  username VARCHAR(30) NOT NULL UNIQUE,
  nome VARCHAR(30) NOT NULL,
  sobrenome VARCHAR(60) NOT NULL,
  sexo sexo_enum,
  data_nascimento DATE NOT NULL,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  id_local INTEGER NOT NULL REFERENCES Local (id_local),
  PRIMARY KEY (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Amizade
-- -----------------------------------------------------
CREATE TABLE Amizade (
  id_seguidor INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  id_seguindo INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  PRIMARY KEY (id_seguidor, id_seguindo)
);

-- -----------------------------------------------------
-- Tabela Playlist
-- -----------------------------------------------------
CREATE TABLE Playlist (
  id_playlist INTEGER GENERATED ALWAYS AS IDENTITY,
  nome VARCHAR(45) NOT NULL,
  descricao TEXT,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  id_ouvinte_criador INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  PRIMARY KEY (id_playlist)
);

-- -----------------------------------------------------
-- Tabela Playlist_Salva
-- -----------------------------------------------------
CREATE TABLE Playlist_Salva (
  ouvinte_id_usuario INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  playlist_id_playlist INTEGER NOT NULL REFERENCES Playlist (id_playlist),
  PRIMARY KEY (ouvinte_id_usuario, playlist_id_playlist)
);

-- -----------------------------------------------------
-- Tabela Genero
-- -----------------------------------------------------
CREATE TABLE Genero (
  id_genero INTEGER GENERATED ALWAYS AS IDENTITY,
  nome VARCHAR(60) NOT NULL UNIQUE,
  surgiu_em DATE NOT NULL,
  PRIMARY KEY (id_genero)
);

-- -----------------------------------------------------
-- Tabela Genero_Favorito
-- -----------------------------------------------------
CREATE TABLE Genero_Favorito (
  id_genero INTEGER NOT NULL REFERENCES Genero (id_genero),
  id_usuario INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  PRIMARY KEY (id_genero, id_usuario)
);

-- -----------------------------------------------------
-- Tabela Musica
-- -----------------------------------------------------
CREATE TABLE Musica (
  id_musica INTEGER GENERATED ALWAYS AS IDENTITY,
  letra TEXT,
  caminho_audio VARCHAR(500) NOT NULL UNIQUE,
  titulo VARCHAR(60) NOT NULL,
  PRIMARY KEY (id_musica)
);

-- -----------------------------------------------------
-- Tabela Escutando
-- -----------------------------------------------------
CREATE TABLE Escutando (
  id_usuario INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  id_musica INTEGER NOT NULL REFERENCES Musica (id_musica),
  PRIMARY KEY (id_usuario, id_musica)
);

-- -----------------------------------------------------
-- Tabela Reacao
-- -----------------------------------------------------
CREATE TABLE Reacao (
  id_usuario_ouvinte INTEGER NOT NULL,
  id_musica INTEGER NOT NULL,
  id_usuario_reagiu INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  emoji VARCHAR(1) NOT NULL,
  PRIMARY KEY (id_usuario_ouvinte, id_musica, id_usuario_reagiu),
  FOREIGN KEY (id_usuario_ouvinte, id_musica) REFERENCES Escutando (id_usuario, id_musica)
);

-- -----------------------------------------------------
-- Tabela Colecao
-- -----------------------------------------------------
CREATE TABLE Colecao (
  id_colecao INTEGER GENERATED ALWAYS AS IDENTITY,
  caminho_capa VARCHAR(500) NOT NULL,
  duracao INTEGER NOT NULL,
  data_lancamento DATE NOT NULL,
  titulo VARCHAR(90) NOT NULL,
  tipo tipo_colecao_enum NOT NULL,
  PRIMARY KEY (id_colecao)
);

-- -----------------------------------------------------
-- Tabela Colecao_Favorita
-- -----------------------------------------------------
CREATE TABLE Colecao_Favorita (
  id_usuario INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  id_colecao INTEGER NOT NULL REFERENCES Colecao (id_colecao),
  PRIMARY KEY (id_usuario, id_colecao)
);

-- -----------------------------------------------------
-- Tabela Produtora
-- -----------------------------------------------------
CREATE TABLE Produtora (
  id_usuario INTEGER GENERATED ALWAYS AS IDENTITY,
  email VARCHAR(30)[] NOT NULL,
  senha VARCHAR(30) NOT NULL,
  username VARCHAR(30) NOT NULL UNIQUE,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  nome_fantasia VARCHAR(60) NOT NULL,
  razao_social VARCHAR(90) NOT NULL UNIQUE,
  id_local INTEGER NOT NULL REFERENCES Local (id_local),
  PRIMARY KEY (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Artista_Banda
-- -----------------------------------------------------
CREATE TABLE Artista_Banda (
  id_usuario INTEGER GENERATED ALWAYS AS IDENTITY,
  integrantes VARCHAR(90)[] NOT NULL,
  ano_formacao INTEGER NOT NULL,
  nome_artistico VARCHAR(60) NOT NULL,
  descricao TEXT,
  email VARCHAR(30)[] NOT NULL,
  senha VARCHAR(30) NOT NULL,
  username VARCHAR(30) NOT NULL UNIQUE,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  id_produtora INTEGER REFERENCES Produtora (id_usuario),
  id_local INTEGER NOT NULL REFERENCES Local (id_local),
  PRIMARY KEY (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Avaliacao
-- -----------------------------------------------------
CREATE TABLE Avaliacao (
  id_usuario INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  id_colecao INTEGER NOT NULL REFERENCES Colecao (id_colecao),
  titulo VARCHAR(60),
  nota DECIMAL(2,1) NOT NULL,
  descricao TEXT,
  PRIMARY KEY (id_usuario, id_colecao)
);

-- -----------------------------------------------------
-- Tabela Seguidor_Artista
-- -----------------------------------------------------
CREATE TABLE Seguidor_Artista (
  id_ouvinte INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  id_artista INTEGER NOT NULL REFERENCES Artista_Banda (id_usuario),
  PRIMARY KEY (id_ouvinte, id_artista)
);

-- -----------------------------------------------------
-- Tabela Loja
-- -----------------------------------------------------
CREATE TABLE Loja (
  id_artista INTEGER PRIMARY KEY REFERENCES Artista_Banda (id_usuario),
  nome VARCHAR(60) NOT NULL,
  id_local INTEGER NOT NULL REFERENCES Local (id_local)
);

-- -----------------------------------------------------
-- Tabela Produto
-- -----------------------------------------------------
CREATE TABLE Produto (
  nome VARCHAR(60) PRIMARY KEY,
  preco DECIMAL(6,2) NOT NULL,
  peso DECIMAL(6,2) NOT NULL,
  disponivel BOOLEAN NOT NULL
);

-- -----------------------------------------------------
-- Tabela Transacao
-- -----------------------------------------------------
CREATE TABLE Transacao (
  id_transacao INTEGER GENERATED ALWAYS AS IDENTITY,
  nome_produto VARCHAR(60) NOT NULL REFERENCES Produto (nome),
  id_ouvinte INTEGER NOT NULL REFERENCES Ouvinte (id_usuario),
  loja INTEGER NOT NULL REFERENCES Loja (id_artista),
  numero INTEGER NOT NULL UNIQUE,
  valor DECIMAL(7,2) NOT NULL,
  PRIMARY KEY (id_transacao)
);

-- -----------------------------------------------------
-- Tabela Musica_Playlist
-- -----------------------------------------------------
CREATE TABLE Musica_Playlist (
  id_musica INTEGER NOT NULL REFERENCES Musica (id_musica),
  id_playlist INTEGER NOT NULL REFERENCES Playlist (id_playlist),
  PRIMARY KEY (id_musica, id_playlist)
);

-- -----------------------------------------------------
-- Tabela Musica_Colecao
-- -----------------------------------------------------
CREATE TABLE Musica_Colecao (
  id_musica INTEGER NOT NULL REFERENCES Musica (id_musica),
  id_colecao INTEGER NOT NULL REFERENCES Colecao (id_colecao),
  PRIMARY KEY (id_musica, id_colecao)
);

-- -----------------------------------------------------
-- Tabela Videoclipe
-- -----------------------------------------------------
CREATE TABLE Videoclipe (
  id_musica INTEGER PRIMARY KEY REFERENCES Musica (id_musica),
  descricao TEXT,
  titulo VARCHAR(90) NOT NULL,
  caminho_video VARCHAR(500) NOT NULL UNIQUE,
  ano_lancamento INTEGER NOT NULL
);

-- -----------------------------------------------------
-- Tabela Genero_Musica
-- -----------------------------------------------------
CREATE TABLE Genero_Musica (
  id_genero INTEGER NOT NULL REFERENCES Genero (id_genero),
  id_musica INTEGER NOT NULL REFERENCES Musica (id_musica),
  PRIMARY KEY (id_genero, id_musica)
);

-- -----------------------------------------------------
-- Tabela Featuring
-- -----------------------------------------------------
CREATE TABLE Featuring (
  id_musica INTEGER NOT NULL REFERENCES Musica (id_musica),
  id_usuario INTEGER NOT NULL REFERENCES Artista_Banda (id_usuario),
  PRIMARY KEY (id_musica, id_usuario)
);

-- -----------------------------------------------------
-- Tabela Artista_Banda_Colecao
-- -----------------------------------------------------
CREATE TABLE Artista_Banda_Colecao (
  id_colecao INTEGER NOT NULL REFERENCES Colecao (id_colecao),
  id_usuario INTEGER NOT NULL REFERENCES Artista_Banda (id_usuario),
  PRIMARY KEY (id_colecao, id_usuario)
);

-- -----------------------------------------------------
-- Tabela Genero_Colecao
-- -----------------------------------------------------
CREATE TABLE Genero_Colecao (
  id_genero INTEGER NOT NULL REFERENCES Genero (id_genero),
  id_colecao INTEGER NOT NULL REFERENCES Colecao (id_colecao),
  PRIMARY KEY (id_genero, id_colecao)
);

-- -----------------------------------------------------
-- Tabela Disco
-- -----------------------------------------------------
CREATE TABLE Disco (
  nome_produto VARCHAR(60) PRIMARY KEY REFERENCES Produto (nome),
  id_colecao INTEGER NOT NULL REFERENCES Colecao (id_colecao),
  tipo tipo_disco_enum NOT NULL,
  quantidade_discos SMALLINT NOT NULL
);

-- -----------------------------------------------------
-- Tabela Evento
-- -----------------------------------------------------
CREATE TABLE Evento (
  nome VARCHAR(90) PRIMARY KEY,
  inicio TIMESTAMP NOT NULL,
  capacidade INTEGER NOT NULL,
  id_local INTEGER NOT NULL REFERENCES Local (id_local)
);

-- -----------------------------------------------------
-- Tabela Atracao
-- -----------------------------------------------------
CREATE TABLE Atracao (
  id_artista_banda INTEGER NOT NULL REFERENCES Artista_Banda (id_usuario),
  nome_evento VARCHAR(90) NOT NULL REFERENCES Evento (nome),
  PRIMARY KEY (id_artista_banda, nome_evento)
);

-- -----------------------------------------------------
-- Tabela Genero_Artista_Banda
-- -----------------------------------------------------
CREATE TABLE Genero_Artista_Banda (
  id_genero INTEGER NOT NULL REFERENCES Genero (id_genero),
  id_artista_banda INTEGER NOT NULL REFERENCES Artista_Banda (id_usuario),
  PRIMARY KEY (id_genero, id_artista_banda)
);

-- -----------------------------------------------------
-- Tabela Vestimenta
-- -----------------------------------------------------
CREATE TABLE Vestimenta (
  nome_produto VARCHAR(60) PRIMARY KEY REFERENCES Produto (nome),
  material VARCHAR(60) NOT NULL,
  tamanho tamanho_enum NOT NULL
);

-- -----------------------------------------------------
-- Tabela Ingresso
-- -----------------------------------------------------
CREATE TABLE Ingresso (
  nome_produto VARCHAR(60) PRIMARY KEY REFERENCES Produto (nome),
  nome_evento VARCHAR(90) NOT NULL REFERENCES Evento (nome),
  tipo tipo_ingresso_enum NOT NULL
);

-- -----------------------------------------------------
-- Índices para performance
-- -----------------------------------------------------
CREATE INDEX idx_ouvinte_username ON Ouvinte (username);
CREATE INDEX idx_ouvinte_email ON Ouvinte USING GIN (email);
CREATE INDEX idx_artista_username ON Artista_Banda (username);
CREATE INDEX idx_artista_email ON Artista_Banda USING GIN (email);
CREATE INDEX idx_artista_integrantes ON Artista_Banda USING GIN (integrantes);
CREATE INDEX idx_produtora_username ON Produtora (username);
CREATE INDEX idx_produtora_email ON Produtora USING GIN (email);
CREATE INDEX idx_musica_titulo ON Musica (titulo);
CREATE INDEX idx_colecao_titulo ON Colecao (titulo);
CREATE INDEX idx_evento_inicio ON Evento (inicio);
CREATE INDEX idx_playlist_nome ON Playlist (nome);
