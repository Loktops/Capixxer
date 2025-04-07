import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Superfuncionario.settings')
django.setup()

from Capixxer.models import Loja, DadosLoja

# Limpar dados existentes
Loja.objects.all().delete()

# Criar a loja ARV
loja_arv, created = Loja.objects.get_or_create(
    nome='Arv',
    defaults={
        'endereco': 'Endereço ARV',
        'telefone': '(00) 0000-0000',
        'email': 'arv@example.com'
    }
)

# Dados da ARV
dados_arv = {
    'total_produtos': 1459,
    'produtos_respondidos': 783,  # 53%
    'produtos_nao_respondidos': 676,  # 46%
    'produtos_gondola': 517,  # 66%
    'produtos_ruptura': 266,  # 33%
    'produtos_presente': 491,  # 94%
    'produtos_presente_reposto': 26,  # 5%
}

# Criar registro para ARV
DadosLoja.objects.create(
    loja=loja_arv,
    data=datetime(2025, 3, 1),
    vendas=0,
    clientes=0,
    ticket_medio=0,
    meta=0,
    total_produtos=dados_arv['total_produtos'],
    produtos_respondidos=dados_arv['produtos_respondidos'],
    produtos_nao_respondidos=dados_arv['produtos_nao_respondidos'],
    produtos_gondola=dados_arv['produtos_gondola'],
    produtos_ruptura=dados_arv['produtos_ruptura'],
    produtos_presente=dados_arv['produtos_presente'],
    produtos_presente_reposto=dados_arv['produtos_presente_reposto'],
    observacoes='Dados de março 2025'
)

# Criar a loja Ceará
loja_ceara, created = Loja.objects.get_or_create(
    nome='Ceara',
    defaults={
        'endereco': 'Endereço Ceará',
        'telefone': '(00) 0000-0000',
        'email': 'ceara@example.com'
    }
)

# Dados da Ceará
dados_ceara = {
    'total_produtos': 2177,
    'produtos_respondidos': 1507,  # 69%
    'produtos_nao_respondidos': 670,  # 30%
    'produtos_gondola': 1284,  # 85%
    'produtos_ruptura': 223,  # 14%
    'produtos_presente': 944,  # 73%
    'produtos_presente_reposto': 340,  # 26%
}

# Criar registro para Ceará
DadosLoja.objects.create(
    loja=loja_ceara,
    data=datetime(2025, 3, 1),
    vendas=0,
    clientes=0,
    ticket_medio=0,
    meta=0,
    total_produtos=dados_ceara['total_produtos'],
    produtos_respondidos=dados_ceara['produtos_respondidos'],
    produtos_nao_respondidos=dados_ceara['produtos_nao_respondidos'],
    produtos_gondola=dados_ceara['produtos_gondola'],
    produtos_ruptura=dados_ceara['produtos_ruptura'],
    produtos_presente=dados_ceara['produtos_presente'],
    produtos_presente_reposto=dados_ceara['produtos_presente_reposto'],
    observacoes='Dados de março 2025'
)

# Criar a loja Atacale
loja_atacale, created = Loja.objects.get_or_create(
    nome='Atacale',
    defaults={
        'endereco': 'Endereço Atacale',
        'telefone': '(00) 0000-0000',
        'email': 'atacale@example.com'
    }
)

# Dados do Atacale (da imagem)
dados_atacale = {
    'total_produtos': 881,
    'produtos_respondidos': 199,  # 22%
    'produtos_nao_respondidos': 682,  # 77%
    'produtos_gondola': 161,  # 80%
    'produtos_ruptura': 38,  # 19%
    'produtos_presente': 156,  # 96%
    'produtos_presente_reposto': 5,  # 3%
}

# Criar registro para Atacale
DadosLoja.objects.create(
    loja=loja_atacale,
    data=datetime(2025, 3, 1),
    vendas=0,
    clientes=0,
    ticket_medio=0,
    meta=0,
    total_produtos=dados_atacale['total_produtos'],
    produtos_respondidos=dados_atacale['produtos_respondidos'],
    produtos_nao_respondidos=dados_atacale['produtos_nao_respondidos'],
    produtos_gondola=dados_atacale['produtos_gondola'],
    produtos_ruptura=dados_atacale['produtos_ruptura'],
    produtos_presente=dados_atacale['produtos_presente'],
    produtos_presente_reposto=dados_atacale['produtos_presente_reposto'],
    observacoes='Dados de março 2025'
)

# Criar a loja GV
loja_gv, created = Loja.objects.get_or_create(
    nome='Gv',
    defaults={
        'endereco': 'Endereço GV',
        'telefone': '(00) 0000-0000',
        'email': 'gv@example.com'
    }
)

# Dados da GV (da imagem)
dados_gv = {
    'total_produtos': 1168,
    'produtos_respondidos': 732,  # 62.7%
    'produtos_nao_respondidos': 436,  # 37%
    'produtos_gondola': 504,  # 68.9%
    'produtos_ruptura': 228,  # 31.1%
    'produtos_presente': 492,  # 97.6%
    'produtos_presente_reposto': 12,  # 2%
}

# Criar registro para GV
DadosLoja.objects.create(
    loja=loja_gv,
    data=datetime(2025, 3, 1),
    vendas=0,
    clientes=0,
    ticket_medio=0,
    meta=0,
    total_produtos=dados_gv['total_produtos'],
    produtos_respondidos=dados_gv['produtos_respondidos'],
    produtos_nao_respondidos=dados_gv['produtos_nao_respondidos'],
    produtos_gondola=dados_gv['produtos_gondola'],
    produtos_ruptura=dados_gv['produtos_ruptura'],
    produtos_presente=dados_gv['produtos_presente'],
    produtos_presente_reposto=dados_gv['produtos_presente_reposto'],
    observacoes='Dados de março 2025'
)

# Criar a loja Leblon
loja_leblon, created = Loja.objects.get_or_create(
    nome='Leblon',
    defaults={
        'endereco': 'Endereço Leblon',
        'telefone': '(00) 0000-0000',
        'email': 'leblon@example.com'
    }
)

# Dados da Leblon (da imagem)
dados_leblon = {
    'total_produtos': 2156,
    'produtos_respondidos': 1970,  # 91.4%
    'produtos_nao_respondidos': 186,  # 8%
    'produtos_gondola': 1747,  # 88.7%
    'produtos_ruptura': 223,  # 11%
    'produtos_presente': 1606,  # 91.9%
    'produtos_presente_reposto': 141,  # 8%
}

# Criar registro para Leblon
DadosLoja.objects.create(
    loja=loja_leblon,
    data=datetime(2025, 3, 1),
    vendas=0,
    clientes=0,
    ticket_medio=0,
    meta=0,
    total_produtos=dados_leblon['total_produtos'],
    produtos_respondidos=dados_leblon['produtos_respondidos'],
    produtos_nao_respondidos=dados_leblon['produtos_nao_respondidos'],
    produtos_gondola=dados_leblon['produtos_gondola'],
    produtos_ruptura=dados_leblon['produtos_ruptura'],
    produtos_presente=dados_leblon['produtos_presente'],
    produtos_presente_reposto=dados_leblon['produtos_presente_reposto'],
    observacoes='Dados de março 2025'
)

print('Dados inseridos com sucesso!') 