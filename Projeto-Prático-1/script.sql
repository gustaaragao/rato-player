-- Deleta todos os registros presentes na Tabela "colecao"
DELETE FROM Colecao;

-- Insere alguns registros na Tabela "colecao"
INSERT INTO Colecao (id_colecao, titulo, caminho_capa, duracao, data_lancamento, tipo) VALUES
(0, 'Campo de Batalha', '/capas/edsongomes_campodebatalha.jpg', 2274, '1992-01-06', 'Album'),
(1, 'Holoceno', '/capas/papangu_holoceno.jpg', 2648, '2021-06-25', 'Album'),
(2, 'Druqks', '/capas/druqks.jpg', 6000, '2001-08-22', 'Album'),
(3, 'Last Words: Screamed from Behind God''s Muzzle', '/capas/last-words.jpg', 1328, '2020-01-08', 'EP'),
(4, 'F♯ A♯ ∞', '/capas/gybe_fsharpasharpinfinity.jpg', 3780, '1997-08-14', 'Album'),
(5, 'Onset Of Putrefication', '/necrophagist_onsetofputrefication.png', 2530, '2004-01-01', 'Album'),
(6, 'The Daily Mail/Staircase', '/sapac/thedailymail_staircase.webp', 489, '2011-12-19', 'Single'),
(7, 'Capsule Losing Contact', '/capas/duster_capsulelosingcontact.gif', 9000, '2019-03-22', 'Compilacao'),
(8, '東方風神録　～ Mountain of Faith', '/games/th/mof_ost.wbmp', 4620, '2007-08-17', 'Album'),
(9, 'Infinita Highway', '/capas/engenheiros_infinitahighway.ogg', 27240, '1998-03-04', 'Compilacao');

-- Exibe os registros presentes na Tabela "colecao"
SELECT * from colecao;