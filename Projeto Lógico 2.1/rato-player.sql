-- Caso existe, drop tabelas
DROP TABLE IF EXISTS Ingresso CASCADE;
DROP TABLE IF EXISTS Vestimenta CASCADE;
DROP TABLE IF EXISTS Genero_Artista_Banda CASCADE;
DROP TABLE IF EXISTS Atracoes CASCADE;
DROP TABLE IF EXISTS Evento CASCADE;
DROP TABLE IF EXISTS Disco CASCADE;
DROP TABLE IF EXISTS Genero_Colecao CASCADE;
DROP TABLE IF EXISTS Artista_Banda_Colecao CASCADE;
DROP TABLE IF EXISTS Featuring CASCADE;
DROP TABLE IF EXISTS Genero_Musica CASCADE;
DROP TABLE IF EXISTS Videoclipe CASCADE;
DROP TABLE IF EXISTS Musica_Colecao CASCADE;
DROP TABLE IF EXISTS Musicas_Playlist CASCADE;
DROP TABLE IF EXISTS Transacao CASCADE;
DROP TABLE IF EXISTS Produto CASCADE;
DROP TABLE IF EXISTS Loja CASCADE;
DROP TABLE IF EXISTS Seguidores_Artistas CASCADE;
DROP TABLE IF EXISTS Avaliacao CASCADE;
DROP TABLE IF EXISTS Artista_Banda CASCADE;
DROP TABLE IF EXISTS Produtora CASCADE;
DROP TABLE IF EXISTS Colecoes_Favoritas CASCADE;
DROP TABLE IF EXISTS Colecao CASCADE;
DROP TABLE IF EXISTS Reacao CASCADE;
DROP TABLE IF EXISTS Escutando CASCADE;
DROP TABLE IF EXISTS Musica CASCADE;
DROP TABLE IF EXISTS Genero_Favorito CASCADE;
DROP TABLE IF EXISTS Genero CASCADE;
DROP TABLE IF EXISTS Playlists_Salvas CASCADE;
DROP TABLE IF EXISTS Playlist CASCADE;
DROP TABLE IF EXISTS Amizade CASCADE;
DROP TABLE IF EXISTS Ouvinte CASCADE;
DROP TABLE IF EXISTS Local CASCADE;

-- Criar ENUM types
CREATE TYPE sexo_enum AS ENUM ('M', 'F', 'NB');
CREATE TYPE tipo_colecao_enum AS ENUM ('Album', 'EP', 'Single', 'Compilacao');
CREATE TYPE tipo_disco_enum AS ENUM ('CD', 'Vinil', 'Fita');
CREATE TYPE tamanho_enum AS ENUM ('PP', 'P', 'M', 'G', 'GG', 'XGG');
CREATE TYPE tipo_ingresso_enum AS ENUM ('Normal', 'Premium');

-- -----------------------------------------------------
-- Tabela Local
-- -----------------------------------------------------
CREATE TABLE Local (
  id_local INTEGER NOT NULL,
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
  id_usuario INTEGER NOT NULL,
  email VARCHAR(30)[] NOT NULL,
  senha VARCHAR(30) NOT NULL,
  username VARCHAR(30) NOT NULL,
  nome VARCHAR(30) NOT NULL,
  sobrenome VARCHAR(60) NOT NULL,
  sexo sexo_enum,
  data_nascimento DATE NOT NULL,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  id_local INTEGER NOT NULL,
  PRIMARY KEY (id_usuario),
  UNIQUE (username),
  FOREIGN KEY (id_local) REFERENCES Local (id_local)
);

-- -----------------------------------------------------
-- Tabela Amizade
-- -----------------------------------------------------
CREATE TABLE Amizade (
  id_seguidor INTEGER NOT NULL,
  id_seguindo INTEGER NOT NULL,
  PRIMARY KEY (id_seguidor, id_seguindo),
  FOREIGN KEY (id_seguidor) REFERENCES Ouvinte (id_usuario),
  FOREIGN KEY (id_seguindo) REFERENCES Ouvinte (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Playlist
-- -----------------------------------------------------
CREATE TABLE Playlist (
  id_playlist INTEGER NOT NULL,
  nome VARCHAR(45) NOT NULL,
  descricao TEXT,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  id_ouvinte_criador INTEGER NOT NULL,
  PRIMARY KEY (id_playlist),
  FOREIGN KEY (id_ouvinte_criador) REFERENCES Ouvinte (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Playlists_Salvas
-- -----------------------------------------------------
CREATE TABLE Playlists_Salvas (
  ouvinte_id_usuario INTEGER NOT NULL,
  playlist_id_playlist INTEGER NOT NULL,
  PRIMARY KEY (ouvinte_id_usuario, playlist_id_playlist),
  FOREIGN KEY (ouvinte_id_usuario) REFERENCES Ouvinte (id_usuario),
  FOREIGN KEY (playlist_id_playlist) REFERENCES Playlist (id_playlist)
);

-- -----------------------------------------------------
-- Tabela Genero
-- -----------------------------------------------------
CREATE TABLE Genero (
  nome VARCHAR(60) NOT NULL,
  surgiu_em DATE NOT NULL,
  PRIMARY KEY (nome)
);

-- -----------------------------------------------------
-- Tabela Genero_Favorito
-- -----------------------------------------------------
CREATE TABLE Genero_Favorito (
  nome_genero VARCHAR(60) NOT NULL,
  id_usuario INTEGER NOT NULL,
  PRIMARY KEY (nome_genero, id_usuario),
  FOREIGN KEY (nome_genero) REFERENCES Genero (nome),
  FOREIGN KEY (id_usuario) REFERENCES Ouvinte (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Musica
-- -----------------------------------------------------
CREATE TABLE Musica (
  id_musica INTEGER NOT NULL,
  letra TEXT,
  caminho_audio VARCHAR(500) NOT NULL,
  titulo VARCHAR(60) NOT NULL,
  PRIMARY KEY (id_musica),
  UNIQUE (caminho_audio)
);

-- -----------------------------------------------------
-- Tabela Escutando
-- -----------------------------------------------------
CREATE TABLE Escutando (
  id_usuario INTEGER NOT NULL,
  id_musica INTEGER NOT NULL,
  PRIMARY KEY (id_usuario, id_musica),
  FOREIGN KEY (id_usuario) REFERENCES Ouvinte (id_usuario),
  FOREIGN KEY (id_musica) REFERENCES Musica (id_musica)
);

-- -----------------------------------------------------
-- Tabela Reacao
-- -----------------------------------------------------
CREATE TABLE Reacao (
  id_usuario_ouvinte INTEGER NOT NULL,
  id_musica INTEGER NOT NULL,
  id_usuario_reagiu INTEGER NOT NULL,
  emoji VARCHAR(1) NOT NULL,
  PRIMARY KEY (id_usuario_ouvinte, id_musica, id_usuario_reagiu),
  FOREIGN KEY (id_usuario_ouvinte, id_musica) REFERENCES Escutando (id_usuario, id_musica),
  FOREIGN KEY (id_usuario_reagiu) REFERENCES Ouvinte (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Colecao
-- -----------------------------------------------------
CREATE TABLE Colecao (
  id_colecao INTEGER NOT NULL,
  caminho_capa VARCHAR(500) NOT NULL,
  duracao INTEGER NOT NULL,
  data_lancamento DATE NOT NULL,
  titulo VARCHAR(90) NOT NULL,
  tipo tipo_colecao_enum NOT NULL,
  PRIMARY KEY (id_colecao),
  UNIQUE (caminho_capa)
);

-- -----------------------------------------------------
-- Tabela Colecoes_Favoritas
-- -----------------------------------------------------
CREATE TABLE Colecoes_Favoritas (
  id_usuario INTEGER NOT NULL,
  id_colecao INTEGER NOT NULL,
  PRIMARY KEY (id_usuario, id_colecao),
  FOREIGN KEY (id_usuario) REFERENCES Ouvinte (id_usuario),
  FOREIGN KEY (id_colecao) REFERENCES Colecao (id_colecao)
);

-- -----------------------------------------------------
-- Tabela Produtora
-- -----------------------------------------------------
CREATE TABLE Produtora (
  id_usuario INTEGER NOT NULL,
  email VARCHAR(30)[] NOT NULL,
  senha VARCHAR(30) NOT NULL,
  username VARCHAR(30) NOT NULL,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  nome_fantasia VARCHAR(60) NOT NULL,
  razao_social VARCHAR(90) NOT NULL,
  id_local INTEGER NOT NULL,
  PRIMARY KEY (id_usuario),
  UNIQUE (username),
  UNIQUE (razao_social),
  FOREIGN KEY (id_local) REFERENCES Local (id_local)
);

-- -----------------------------------------------------
-- Tabela Artista_Banda
-- -----------------------------------------------------
CREATE TABLE Artista_Banda (
  id_usuario VARCHAR(45) NOT NULL,
  integrantes VARCHAR(90)[] NOT NULL,
  ano_formacao INTEGER NOT NULL,
  nome_artistico VARCHAR(60) NOT NULL,
  descricao TEXT,
  email VARCHAR(30)[] NOT NULL,
  senha VARCHAR(30) NOT NULL,
  username VARCHAR(30) NOT NULL,
  criado_em TIMESTAMP NOT NULL,
  atualizado_em TIMESTAMP NOT NULL,
  id_produtora INTEGER,
  id_local INTEGER NOT NULL,
  PRIMARY KEY (id_usuario),
  UNIQUE (username),
  FOREIGN KEY (id_produtora) REFERENCES Produtora (id_usuario),
  FOREIGN KEY (id_local) REFERENCES Local (id_local)
);

-- -----------------------------------------------------
-- Tabela Avaliacao
-- -----------------------------------------------------
CREATE TABLE Avaliacao (
  id_usuario INTEGER NOT NULL,
  id_colecao INTEGER NOT NULL,
  titulo VARCHAR(60),
  nota DECIMAL(2,1) NOT NULL,
  descricao TEXT,
  PRIMARY KEY (id_usuario, id_colecao),
  FOREIGN KEY (id_usuario) REFERENCES Ouvinte (id_usuario),
  FOREIGN KEY (id_colecao) REFERENCES Colecao (id_colecao)
);

-- -----------------------------------------------------
-- Tabela Seguidores_Artistas
-- -----------------------------------------------------
CREATE TABLE Seguidores_Artistas (
  id_ouvinte INTEGER NOT NULL,
  id_artista VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_ouvinte, id_artista),
  FOREIGN KEY (id_ouvinte) REFERENCES Ouvinte (id_usuario),
  FOREIGN KEY (id_artista) REFERENCES Artista_Banda (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Loja
-- -----------------------------------------------------
CREATE TABLE Loja (
  id_artista VARCHAR(45) NOT NULL,
  nome VARCHAR(60) NOT NULL,
  id_local INTEGER NOT NULL,
  PRIMARY KEY (id_artista),
  FOREIGN KEY (id_artista) REFERENCES Artista_Banda (id_usuario),
  FOREIGN KEY (id_local) REFERENCES Local (id_local)
);

-- -----------------------------------------------------
-- Tabela Produto
-- -----------------------------------------------------
CREATE TABLE Produto (
  nome VARCHAR(60) NOT NULL,
  preco DECIMAL(6,2) NOT NULL,
  peso DECIMAL(6,2) NOT NULL,
  disponivel BOOLEAN NOT NULL,
  PRIMARY KEY (nome)
);

-- -----------------------------------------------------
-- Tabela Transacao
-- -----------------------------------------------------
CREATE TABLE Transacao (
  nome_produto VARCHAR(60) NOT NULL,
  id_ouvinte INTEGER NOT NULL,
  loja VARCHAR(45) NOT NULL,
  numero INTEGER NOT NULL,
  valor DECIMAL(7,2) NOT NULL,
  PRIMARY KEY (nome_produto),
  UNIQUE (numero),
  FOREIGN KEY (nome_produto) REFERENCES Produto (nome),
  FOREIGN KEY (id_ouvinte) REFERENCES Ouvinte (id_usuario),
  FOREIGN KEY (loja) REFERENCES Loja (id_artista)
);

-- -----------------------------------------------------
-- Tabela Musicas_Playlist
-- -----------------------------------------------------
CREATE TABLE Musicas_Playlist (
  id_musica INTEGER NOT NULL,
  id_playlist INTEGER NOT NULL,
  PRIMARY KEY (id_musica, id_playlist),
  FOREIGN KEY (id_musica) REFERENCES Musica (id_musica),
  FOREIGN KEY (id_playlist) REFERENCES Playlist (id_playlist)
);

-- -----------------------------------------------------
-- Tabela Musica_Colecao
-- -----------------------------------------------------
CREATE TABLE Musica_Colecao (
  id_musica INTEGER NOT NULL,
  id_colecao INTEGER NOT NULL,
  PRIMARY KEY (id_musica, id_colecao),
  FOREIGN KEY (id_musica) REFERENCES Musica (id_musica),
  FOREIGN KEY (id_colecao) REFERENCES Colecao (id_colecao)
);

-- -----------------------------------------------------
-- Tabela Videoclipe
-- -----------------------------------------------------
CREATE TABLE Videoclipe (
  id_musica INTEGER NOT NULL,
  descricao TEXT,
  titulo VARCHAR(90) NOT NULL,
  caminho_video VARCHAR(500) NOT NULL,
  ano_lancamento INTEGER NOT NULL,
  PRIMARY KEY (id_musica),
  UNIQUE (caminho_video),
  FOREIGN KEY (id_musica) REFERENCES Musica (id_musica)
);

-- -----------------------------------------------------
-- Tabela Genero_Musica
-- -----------------------------------------------------
CREATE TABLE Genero_Musica (
  nome_genero VARCHAR(60) NOT NULL,
  id_musica INTEGER NOT NULL,
  PRIMARY KEY (nome_genero, id_musica),
  FOREIGN KEY (nome_genero) REFERENCES Genero (nome),
  FOREIGN KEY (id_musica) REFERENCES Musica (id_musica)
);

-- -----------------------------------------------------
-- Tabela Featuring
-- -----------------------------------------------------
CREATE TABLE Featuring (
  id_musica INTEGER NOT NULL,
  id_usuario VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_musica, id_usuario),
  FOREIGN KEY (id_musica) REFERENCES Musica (id_musica),
  FOREIGN KEY (id_usuario) REFERENCES Artista_Banda (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Artista_Banda_Colecao
-- -----------------------------------------------------
CREATE TABLE Artista_Banda_Colecao (
  id_colecao INTEGER NOT NULL,
  id_usuario VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_colecao, id_usuario),
  FOREIGN KEY (id_colecao) REFERENCES Colecao (id_colecao),
  FOREIGN KEY (id_usuario) REFERENCES Artista_Banda (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Genero_Colecao
-- -----------------------------------------------------
CREATE TABLE Genero_Colecao (
  nome_genero VARCHAR(60) NOT NULL,
  id_colecao INTEGER NOT NULL,
  PRIMARY KEY (nome_genero, id_colecao),
  FOREIGN KEY (nome_genero) REFERENCES Genero (nome),
  FOREIGN KEY (id_colecao) REFERENCES Colecao (id_colecao)
);

-- -----------------------------------------------------
-- Tabela Disco
-- -----------------------------------------------------
CREATE TABLE Disco (
  nome_produto VARCHAR(60) NOT NULL,
  id_colecao INTEGER NOT NULL,
  tipo tipo_disco_enum NOT NULL,
  quantidade_discos SMALLINT NOT NULL,
  PRIMARY KEY (nome_produto),
  FOREIGN KEY (nome_produto) REFERENCES Produto (nome),
  FOREIGN KEY (id_colecao) REFERENCES Colecao (id_colecao)
);

-- -----------------------------------------------------
-- Tabela Evento
-- -----------------------------------------------------
CREATE TABLE Evento (
  nome VARCHAR(90) NOT NULL,
  inicio TIMESTAMP NOT NULL,
  capacidade INTEGER NOT NULL,
  id_local INTEGER NOT NULL,
  PRIMARY KEY (nome),
  FOREIGN KEY (id_local) REFERENCES Local (id_local)
);

-- -----------------------------------------------------
-- Tabela Atracoes
-- -----------------------------------------------------
CREATE TABLE Atracoes (
  id_artista_banda VARCHAR(45) NOT NULL,
  nome_evento VARCHAR(90) NOT NULL,
  PRIMARY KEY (id_artista_banda, nome_evento),
  FOREIGN KEY (id_artista_banda) REFERENCES Artista_Banda (id_usuario),
  FOREIGN KEY (nome_evento) REFERENCES Evento (nome)
);

-- -----------------------------------------------------
-- Tabela Genero_Artista_Banda
-- -----------------------------------------------------
CREATE TABLE Genero_Artista_Banda (
  nome_genero VARCHAR(60) NOT NULL,
  id_artista_banda VARCHAR(45) NOT NULL,
  PRIMARY KEY (nome_genero, id_artista_banda),
  FOREIGN KEY (nome_genero) REFERENCES Genero (nome),
  FOREIGN KEY (id_artista_banda) REFERENCES Artista_Banda (id_usuario)
);

-- -----------------------------------------------------
-- Tabela Vestimenta
-- -----------------------------------------------------
CREATE TABLE Vestimenta (
  nome_produto VARCHAR(60) NOT NULL,
  material VARCHAR(60) NOT NULL,
  tamanho tamanho_enum NOT NULL,
  PRIMARY KEY (nome_produto),
  FOREIGN KEY (nome_produto) REFERENCES Produto (nome)
);

-- -----------------------------------------------------
-- Tabela Ingresso
-- -----------------------------------------------------
CREATE TABLE Ingresso (
  nome_produto VARCHAR(60) NOT NULL,
  nome_evento VARCHAR(90) NOT NULL,
  tipo tipo_ingresso_enum NOT NULL,
  PRIMARY KEY (nome_produto),
  FOREIGN KEY (nome_produto) REFERENCES Produto (nome),
  FOREIGN KEY (nome_evento) REFERENCES Evento (nome)
);

-- Criando indexes para melhor performance
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