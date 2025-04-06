from django.shortcuts import render
from django.http import HttpResponse
from .models import Loja, DadosLoja
from django.db.models import Sum, Avg
from datetime import datetime

def home(request):
    # Obtém as 5 lojas específicas
    lojas = Loja.objects.filter(nome__in=['Arv', 'Ceara', 'Atacale', 'Gv', 'Leblon'])
    
    # Obtém os dados de março de 2025 para cada loja
    data_inicio = datetime(2025, 3, 1)
    data_fim = datetime(2025, 3, 31)
    
    # Lista para armazenar os dados de cada loja
    dados_lojas_lista = []
    
    for loja in lojas:
        dados = DadosLoja.objects.filter(
            loja=loja,
            data__gte=data_inicio,
            data__lte=data_fim
        ).order_by('-data')
        
        if not dados.exists():
            continue
            
        # Agregações para totais
        agregacoes = dados.aggregate(
            total_produtos=Sum('total_produtos'),
            produtos_respondidos=Sum('produtos_respondidos'),
            produtos_nao_respondidos=Sum('produtos_nao_respondidos'),
            produtos_gondola=Sum('produtos_gondola'),
            produtos_ruptura=Sum('produtos_ruptura'),
            produtos_presente=Sum('produtos_presente'),
            produtos_presente_reposto=Sum('produtos_presente_reposto')
        )
        
        # Calcula as porcentagens
        total_produtos = agregacoes['total_produtos'] or 0
        produtos_respondidos = agregacoes['produtos_respondidos'] or 0
        produtos_gondola = agregacoes['produtos_gondola'] or 0
        
        porcentagens = {
            'respondidos': round((produtos_respondidos / total_produtos * 100) if total_produtos > 0 else 0, 2),
            'nao_respondidos': round((agregacoes['produtos_nao_respondidos'] or 0) / total_produtos * 100 if total_produtos > 0 else 0, 2),
            'gondola': round((produtos_gondola / produtos_respondidos * 100) if produtos_respondidos > 0 else 0, 2),
            'ruptura': round((agregacoes['produtos_ruptura'] or 0) / produtos_respondidos * 100 if produtos_respondidos > 0 else 0, 2),
            'presente': round((agregacoes['produtos_presente'] or 0) / produtos_gondola * 100 if produtos_gondola > 0 else 0, 2),
            'presente_reposto': round((agregacoes['produtos_presente_reposto'] or 0) / produtos_gondola * 100 if produtos_gondola > 0 else 0, 2),
        }
        
        # Adiciona dados da loja à lista
        dados_lojas_lista.append({
            'loja': loja,
            'dados': dados,
            'total_produtos': total_produtos,
            'produtos_respondidos': produtos_respondidos,
            'produtos_nao_respondidos': agregacoes['produtos_nao_respondidos'] or 0,
            'produtos_gondola': produtos_gondola,
            'produtos_ruptura': agregacoes['produtos_ruptura'] or 0,
            'produtos_presente': agregacoes['produtos_presente'] or 0,
            'produtos_presente_reposto': agregacoes['produtos_presente_reposto'] or 0,
            'porcentagens': porcentagens
        })
    
    context = {
        'dados_lojas_lista': dados_lojas_lista,
    }
    
    return render(request, 'home/home.html', context)

def comparativo(request):
    # Obtém as 5 lojas específicas
    lojas = Loja.objects.filter(nome__in=['Arv', 'Ceara', 'Atacale', 'Gv', 'Leblon'])
    
    # Obtém os dados de março de 2025 para cada loja
    data_inicio = datetime(2025, 3, 1)
    data_fim = datetime(2025, 3, 31)
    
    # Lista para armazenar os dados de cada loja
    dados_lojas = []
    
    for loja in lojas:
        dados = DadosLoja.objects.filter(
            loja=loja,
            data__gte=data_inicio,
            data__lte=data_fim
        ).order_by('-data')
        
        if not dados.exists():
            continue
            
        # Agregações para totais
        agregacoes = dados.aggregate(
            total_produtos=Sum('total_produtos'),
            produtos_respondidos=Sum('produtos_respondidos'),
            produtos_nao_respondidos=Sum('produtos_nao_respondidos'),
            produtos_gondola=Sum('produtos_gondola'),
            produtos_ruptura=Sum('produtos_ruptura'),
            produtos_presente=Sum('produtos_presente'),
            produtos_presente_reposto=Sum('produtos_presente_reposto')
        )
        
        # Cálculos mais precisos com tratamento de divisão por zero
        total_produtos = agregacoes['total_produtos'] or 0
        produtos_respondidos = agregacoes['produtos_respondidos'] or 0
        produtos_nao_respondidos = agregacoes['produtos_nao_respondidos'] or 0
        produtos_gondola = agregacoes['produtos_gondola'] or 0
        produtos_presente = agregacoes['produtos_presente'] or 0
        produtos_presente_reposto = agregacoes['produtos_presente_reposto'] or 0
        produtos_ruptura = agregacoes['produtos_ruptura'] or 0
        
        # Cálculos de porcentagens
        porcentagem_nao_respondidos = round((produtos_nao_respondidos / total_produtos * 100) if total_produtos > 0 else 0, 2)
        porcentagem_respondidos = round((produtos_respondidos / total_produtos * 100) if total_produtos > 0 else 0, 2)
        porcentagem_gondola = round((produtos_gondola / produtos_respondidos * 100) if produtos_respondidos > 0 else 0, 2)
        porcentagem_ruptura = round((produtos_ruptura / produtos_respondidos * 100) if produtos_respondidos > 0 else 0, 2)
        porcentagem_reposto = round((produtos_presente_reposto / produtos_gondola * 100) if produtos_gondola > 0 else 0, 2)
        
        # Calcula a eficiência geral (média ponderada)
        eficiencia_geral = round((
            (porcentagem_respondidos * 0.3) +  # Taxa de resposta tem peso 30%
            (porcentagem_gondola * 0.3) +  # Produtos em gôndola tem peso 30%
            (porcentagem_reposto * 0.2) +  # Produtos repostos tem peso 20%
            ((100 - porcentagem_ruptura) * 0.2)  # Redução de ruptura tem peso 20%
        ), 2)
        
        dados_loja = {
            'loja': loja,
            'porcentagem_nao_respondidos': porcentagem_nao_respondidos,
            'porcentagem_respondidos': porcentagem_respondidos,
            'porcentagem_gondola': porcentagem_gondola,
            'porcentagem_ruptura': porcentagem_ruptura,
            'porcentagem_reposto': porcentagem_reposto,
            'eficiencia_geral': eficiencia_geral,
            'total_produtos': total_produtos,
            'produtos_respondidos': produtos_respondidos,
            'produtos_nao_respondidos': produtos_nao_respondidos,
            'produtos_gondola': produtos_gondola,
            'produtos_presente_reposto': produtos_presente_reposto,
            'produtos_ruptura': produtos_ruptura
        }
        dados_lojas.append(dados_loja)
    
    # Ordena as lojas por cada métrica
    ranking_nao_respondidos = sorted(dados_lojas, key=lambda x: x['porcentagem_nao_respondidos'])
    ranking_respondidos = sorted(dados_lojas, key=lambda x: x['porcentagem_respondidos'], reverse=True)
    ranking_gondola = sorted(dados_lojas, key=lambda x: x['porcentagem_gondola'], reverse=True)
    ranking_ruptura = sorted(dados_lojas, key=lambda x: x['porcentagem_ruptura'])
    ranking_reposto = sorted(dados_lojas, key=lambda x: x['porcentagem_reposto'], reverse=True)
    ranking_eficiencia = sorted(dados_lojas, key=lambda x: x['eficiencia_geral'], reverse=True)
    
    # Prepara dados para o gráfico
    lojas_nomes = [loja['loja'].nome for loja in dados_lojas]
    dados_nao_respondidos = [loja['porcentagem_nao_respondidos'] for loja in dados_lojas]
    dados_respondidos = [loja['porcentagem_respondidos'] for loja in dados_lojas]
    dados_gondola = [loja['porcentagem_gondola'] for loja in dados_lojas]
    dados_ruptura = [loja['porcentagem_ruptura'] for loja in dados_lojas]
    dados_reposto = [loja['porcentagem_reposto'] for loja in dados_lojas]
    
    # Análise IA - Gera insights baseados nos dados
    melhor_loja = ranking_eficiencia[0] if ranking_eficiencia else None
    pior_loja = ranking_eficiencia[-1] if ranking_eficiencia else None
    
    # Análise de tendências
    tendencias = []
    for loja in dados_lojas:
        if loja['porcentagem_nao_respondidos'] > 20:
            tendencias.append(f"{loja['loja'].nome} tem alta taxa de não resposta ({loja['porcentagem_nao_respondidos']}%)")
        if loja['porcentagem_gondola'] < 80:
            tendencias.append(f"{loja['loja'].nome} precisa melhorar produtos em gôndola ({loja['porcentagem_gondola']}%)")
        if loja['porcentagem_reposto'] < 70:
            tendencias.append(f"{loja['loja'].nome} precisa melhorar taxa de reposição ({loja['porcentagem_reposto']}%)")
        if loja['porcentagem_ruptura'] > 15:
            tendencias.append(f"{loja['loja'].nome} precisa reduzir ruptura ({loja['porcentagem_ruptura']}%)")
    
    # Análise comparativa
    analise_comparativa = []
    for i, loja in enumerate(ranking_eficiencia):
        if i > 0:
            diferenca = loja['eficiencia_geral'] - ranking_eficiencia[i-1]['eficiencia_geral']
            analise_comparativa.append(
                f"{loja['loja'].nome} está {abs(diferenca):.2f} pontos {'abaixo' if diferenca < 0 else 'acima'} de {ranking_eficiencia[i-1]['loja'].nome}"
            )
    
    # Recomendações específicas
    recomendacoes = []
    for loja in dados_lojas:
        if loja['porcentagem_nao_respondidos'] > 10:
            recomendacoes.append(f"{loja['loja'].nome}: Reduzir taxa de não resposta (atual: {loja['porcentagem_nao_respondidos']}%)")
        if loja['porcentagem_gondola'] < 85:
            recomendacoes.append(f"{loja['loja'].nome}: Aumentar produtos em gôndola (atual: {loja['porcentagem_gondola']}%)")
        if loja['porcentagem_reposto'] < 75:
            recomendacoes.append(f"{loja['loja'].nome}: Melhorar taxa de reposição (atual: {loja['porcentagem_reposto']}%)")
        if loja['porcentagem_ruptura'] > 10:
            recomendacoes.append(f"{loja['loja'].nome}: Reduzir taxa de ruptura (atual: {loja['porcentagem_ruptura']}%)")
    
    context = {
        'current_month': 'Março 2025',
        'ranking_nao_respondidos': ranking_nao_respondidos,
        'ranking_respondidos': ranking_respondidos,
        'ranking_gondola': ranking_gondola,
        'ranking_ruptura': ranking_ruptura,
        'ranking_reposto': ranking_reposto,
        'ranking_eficiencia': ranking_eficiencia,
        'lojas_nomes': lojas_nomes,
        'dados_nao_respondidos': dados_nao_respondidos,
        'dados_respondidos': dados_respondidos,
        'dados_gondola': dados_gondola,
        'dados_ruptura': dados_ruptura,
        'dados_reposto': dados_reposto,
        'tendencias': tendencias,
        'analise_comparativa': analise_comparativa,
        'recomendacoes': recomendacoes
    }
    
    return render(request, 'home/comparativo.html', context)  