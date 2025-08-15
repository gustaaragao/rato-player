// 1. Ouvinte
db.createCollection("ouvintes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "email",
        "senha",
        "username",
        "nome",
        "sobrenome",
        "data_nascimento",
        "criado_em",
        "atualizado_em",
        "id_local"
      ],
      properties: {
        email: { bsonType: "array", items: { bsonType: "string", pattern: "^.+@.+\\..+$"
          }
        },
        senha: { bsonType: "string", minLength: 6
        },
        username: { bsonType: "string", minLength: 3, maxLength: 30
        },
        nome: { bsonType: "string", maxLength: 30
        },
        sobrenome: { bsonType: "string", maxLength: 60
        },
        sexo: { bsonType: "string", enum: [
            "Masculino",
            "Feminino",
            "Outro"
          ]
        },
        data_nascimento: { bsonType: "date"
        },
        criado_em: { bsonType: "date"
        },
        atualizado_em: { bsonType: "date"
        },
        id_local: { bsonType: "objectId"
        }
      }
    }
  }
});

// 2. Playlist
db.createCollection("playlists",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome",
        "criado_em",
        "atualizado_em",
        "id_ouvinte_criador"
      ],
      properties: {
        nome: { bsonType: "string"
        },
        descricao: { bsonType: "string"
        },
        criado_em: { bsonType: "date"
        },
        atualizado_em: { bsonType: "date"
        },
        id_ouvinte_criador: { bsonType: "objectId"
        }
      }
    }
  }
});

// 3. Musica
db.createCollection("musicas",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "caminho_audio",
        "titulo"
      ],
      properties: {
        caminho_audio: { bsonType: "string", unique: true
        },
        titulo: { bsonType: "string"
        },
        letra: { bsonType: "string"
        }
      }
    }
  }
});

// 4. Colecao
db.createCollection("colecoes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "caminho_capa",
        "duracao",
        "data_lancamento",
        "titulo",
        "tipo"
      ],
      properties: {
        caminho_capa: { bsonType: "string", unique: true
        },
        duracao: { bsonType: "int"
        },
        data_lancamento: { bsonType: "date"
        },
        titulo: { bsonType: "string"
        },
        tipo: { bsonType: "string"
        }
      }
    }
  }
});

// 5. Avaliacao
db.createCollection("avaliacoes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_usuario",
        "id_colecao",
        "nota"
      ],
      properties: {
        id_usuario: { bsonType: "objectId"
        },
        id_colecao: { bsonType: "objectId"
        },
        titulo: { bsonType: "string", maxLength: 60
        },
        nota: { bsonType: "decimal", minimum: 0, maximum: 10
        },
        descricao: { bsonType: "string", maxLength: 500
        }
      }
    }
  }
});

// 6. Artista_Banda
db.createCollection("artistas_bandas",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_usuario",
        "integrantes",
        "ano_formacao",
        "nome_artistico",
        "email",
        "senha",
        "username",
        "id_local"
      ],
      properties: {
        id_usuario: { bsonType: "objectId"
        },
        integrantes: { bsonType: "array", items: { bsonType: "string"
          }
        },
        ano_formacao: { bsonType: "int"
        },
        nome_artistico: { bsonType: "string"
        },
        descricao: { bsonType: "string"
        },
        email: { bsonType: "array", items: { bsonType: "string"
          }
        },
        senha: { bsonType: "string"
        },
        username: { bsonType: "string"
        },
        id_produtora: { bsonType: "objectId"
        },
        id_local: { bsonType: "objectId"
        }
      }
    }
  }
});

// 7. Genero
db.createCollection("generos",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome",
        "surgiu_em"
      ],
      properties: {
        nome: { bsonType: "string"
        },
        surgiu_em: { bsonType: "date"
        }
      }
    }
  }
});

// 8. Produto
db.createCollection("produtos",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome",
        "preco",
        "peso",
        "disponivel"
      ],
      properties: {
        nome: { bsonType: "string"
        },
        preco: { bsonType: "decimal"
        },
        peso: { bsonType: "decimal"
        },
        disponivel: { bsonType: "bool"
        }
      }
    }
  }
});

// 9. Evento
db.createCollection("eventos",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome",
        "inicio",
        "capacidade",
        "id_local"
      ],
      properties: {
        nome: { bsonType: "string"
        },
        inicio: { bsonType: "date"
        },
        capacidade: { bsonType: "int"
        },
        id_local: { bsonType: "objectId"
        }
      }
    }
  }
});

// 10. Videoclipe
db.createCollection("videoclipes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_musica",
        "titulo",
        "caminho_video",
        "ano_lancamento"
      ],
      properties: {
        id_musica: { bsonType: "objectId"
        },
        descricao: { bsonType: "string"
        },
        titulo: { bsonType: "string"
        },
        caminho_video: { bsonType: "string"
        },
        ano_lancamento: { bsonType: "int"
        }
      }
    }
  }
});

// 11. Transacao
db.createCollection("transacoes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome_produto",
        "id_ouvinte",
        "loja",
        "numero",
        "valor"
      ],
      properties: {
        nome_produto: { bsonType: "string"
        },
        id_ouvinte: { bsonType: "objectId"
        },
        loja: { bsonType: "objectId"
        },
        numero: { bsonType: "int"
        },
        valor: { bsonType: "decimal"
        }
      }
    }
  }
});

// 12. Featuring
db.createCollection("featuring",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_musica",
        "id_usuario"
      ],
      properties: {
        id_musica: { bsonType: "objectId"
        },
        id_usuario: { bsonType: "string"
        }
      }
    }
  }
});

// 13. Reacao
db.createCollection("reacoes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_usuario_ouvinte",
        "id_musica",
        "id_usuario_reagiu",
        "emoji"
      ],
      properties: {
        id_usuario_ouvinte: { bsonType: "objectId"
        },
        id_musica: { bsonType: "objectId"
        },
        id_usuario_reagiu: { bsonType: "objectId"
        },
        emoji: { bsonType: "string", minLength: 1, maxLength: 1
        }
      }
    }
  }
});

// 14. Escutando
db.createCollection("escutando",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_usuario",
        "id_musica"
      ],
      properties: {
        id_usuario: { bsonType: "objectId"
        },
        id_musica: { bsonType: "objectId"
        }
      }
    }
  }
});

// 15. Disco
db.createCollection("discos",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome_produto",
        "id_colecao",
        "tipo",
        "quantidade_discos"
      ],
      properties: {
        nome_produto: { bsonType: "string"
        },
        id_colecao: { bsonType: "objectId"
        },
        tipo: { bsonType: "string"
        },
        quantidade_discos: { bsonType: "int"
        }
      }
    }
  }
});

// 16. Vestimenta
db.createCollection("vestimentas",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome_produto",
        "preco",
        "tamanho",
        "cor",
        "tipo",
        "disponivel"
      ],
      properties: {
        nome_produto: { bsonType: "string"
        },
        preco: { bsonType: "decimal"
        },
        tamanho: { bsonType: "string"
        },
        cor: { bsonType: "string"
        },
        tipo: { bsonType: "string"
        },
        disponivel: { bsonType: "bool"
        }
      }
    }
  }
});

// 17. Ingresso
db.createCollection("ingressos",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome_produto",
        "nome_evento",
        "tipo"
      ],
      properties: {
        nome_produto: { bsonType: "string"
        },
        nome_evento: { bsonType: "string"
        },
        tipo: { bsonType: "string"
        }
      }
    }
  }
});

// 18. Playlists_Salvas
db.createCollection("playlists_salvas",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "ouvinte_id_usuario",
        "playlist_id_playlist"
      ],
      properties: {
        ouvinte_id_usuario: { bsonType: "objectId"
        },
        playlist_id_playlist: { bsonType: "objectId"
        }
      }
    }
  }
});

// 19. Atracoes
db.createCollection("atracoes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_artista_banda",
        "nome_evento"
      ],
      properties: {
        id_artista_banda: { bsonType: "string"
        },
        nome_evento: { bsonType: "string"
        }
      }
    }
  }
});

// 20. Generos_Artistas_Banda
db.createCollection("generos_artistas_banda",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome_genero",
        "id_artista_banda"
      ],
      properties: {
        nome_genero: { bsonType: "string"
        },
        id_artista_banda: { bsonType: "string"
        }
      }
    }
  }
});

// 21. Generos_Colecoes
db.createCollection("generos_colecoes",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome_genero",
        "id_colecao"
      ],
      properties: {
        nome_genero: { bsonType: "string"
        },
        id_colecao: { bsonType: "objectId"
        }
      }
    }
  }
});

// 22. Generos_Musicas
db.createCollection("generos_musicas",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "nome_genero",
        "id_musica"
      ],
      properties: {
        nome_genero: { bsonType: "string"
        },
        id_musica: { bsonType: "objectId"
        }
      }
    }
  }
});

// 23. Musicas_Playlist
db.createCollection("musicas_playlist",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_musica",
        "id_playlist"
      ],
      properties: {
        id_musica: { bsonType: "objectId"
        },
        id_playlist: { bsonType: "objectId"
        }
      }
    }
  }
});

// 24. Amizades
db.createCollection("amizades",
{
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "id_seguidor",
        "id_seguindo"
      ],
      properties: {
        id_seguidor: { bsonType: "objectId"
        },
        id_seguindo: { bsonType: "objectId"
        }
      }
    }
  }
});
