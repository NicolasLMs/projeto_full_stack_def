"""
Adiciona a coluna forma_pagamento na tabela venda.
Execute uma vez: python migrate_forma_pagamento.py
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'meu_banco.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verifica se a coluna já existe
cursor.execute("PRAGMA table_info(venda)")
colunas = [row[1] for row in cursor.fetchall()]

if 'forma_pagamento' in colunas:
    print("Coluna forma_pagamento já existe. Nada a fazer.")
else:
    cursor.execute("ALTER TABLE venda ADD COLUMN forma_pagamento VARCHAR(20) NOT NULL DEFAULT 'pix'")
    conn.commit()
    print("✓ Coluna forma_pagamento adicionada com sucesso.")

conn.close()
