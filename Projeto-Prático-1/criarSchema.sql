DROP SCHEMA IF EXISTS RatoPlayer CASCADE;
CREATE SCHEMA RatoPlayer;

CREATE TYPE RatoPlayer.tipo_colecao AS ENUM('album', 'single', 'ep', 'compilacao');

CREATE TABLE RatoPlayer.colecao(
    id INT NOT NULL,
    titulo VARCHAR(90) NOT NULL,
    caminho_capa VARCHAR(200),
    duracao int,
    lancamento DATE,
    tipo RatoPlayer.tipo_colecao NOT NULL,

    CONSTRAINT pk_id PRIMARY KEY (id),
    CONSTRAINT ck_duracao CHECK(salario >= 0)
);

INSERT INTO RatoPlayer.colecao VALUES(0, 'Campo de Batalha',                               '/capas/edsongomes_campodebatalha.jpg',   2274, '1992-01-06', 'album');
INSERT INTO RatoPlayer.colecao VALUES(1, 'Holoceno',                                       '/capas/papangu_holoceno.jpg',            2648, '2021-06-25', 'album');
INSERT INTO RatoPlayer.colecao VALUES(2, 'Druqks',                                         NULL,                                     6000, '2001-08-22', 'album');
INSERT INTO RatoPlayer.colecao VALUES(3, 'Last Words: Screamed from Behind God''s Muzzle', NULL,                                     NULL, '2020-01-08', 'ep');
INSERT INTO RatoPlayer.colecao VALUES(4, 'F♯ A♯ ∞',                                        '/capas/gybe_fsharpasharpinfinity.jpg',   3780, NULL,         'album');
INSERT INTO RatoPlayer.colecao VALUES(5, 'Onset Of Putrefication',                         '/necrophagist_onsetofputrefication.png', 2530, '2004-01-01', 'album');
INSERT INTO RatoPlayer.colecao VALUES(6, 'The Daily Mail/Staircase',                       '/sapac/thedailymail_staircase.webp',     489,  NULL,         'single');
INSERT INTO RatoPlayer.colecao VALUES(7, 'Capsule Losing Contact',                         '/capas/duster_capsulelosingcontact.gif', 9000, '2019-03-22', 'compilacao');
INSERT INTO RatoPlayer.colecao VALUES(8, '東方風神録　～ Mountain of Faith',               '/games/th/mof_ost.wbmp',                 4620, '2007-08-17', 'album');
INSERT INTO RatoPlayer.colecao VALUES(9, 'Infinita Highway',                               '/capas/engenheiros_infinitahighway.ogg', NULL, '1998-03-04', 'compilacao');
