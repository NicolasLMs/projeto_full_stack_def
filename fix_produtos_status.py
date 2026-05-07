"""
Script para corrigir produtos com status=False no banco.
Execute uma vez: python fix_produtos_status.py
"""
from app import app
from infrastructure.database.models import db, ProdutoModel

with app.app_context():
    produtos_inativos = ProdutoModel.query.filter_by(status=False).all()
    
    if not produtos_inativos:
        print("Nenhum produto inativo encontrado. Tudo certo!")
    else:
        print(f"Encontrados {len(produtos_inativos)} produto(s) com status=False:")
        for p in produtos_inativos:
            print(f"  - ID {p.id}: {p.nome}")
        
        for p in produtos_inativos:
            p.status = True
        
        db.session.commit()
        print(f"\n✓ {len(produtos_inativos)} produto(s) atualizados para status=True.")
