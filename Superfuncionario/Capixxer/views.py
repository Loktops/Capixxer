from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Loja, DadosLoja
from django.db.models import Sum, Avg
from datetime import datetime
from django.contrib import messages

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
    
    # Obtém dados dos últimos 3 meses para cálculo de tendências
    meses_anteriores = [
        (datetime(2025, 2, 1), datetime(2025, 2, 28)),  # Fevereiro
        (datetime(2025, 1, 1), datetime(2025, 1, 31)),  # Janeiro
        (datetime(2024, 12, 1), datetime(2024, 12, 31))  # Dezembro
    ]
    
    # Lista para armazenar os dados de cada loja
    dados_lojas = []
    
    for loja in lojas:
        # Dados do mês atual
        dados_atual = DadosLoja.objects.filter(
            loja=loja,
            data__gte=data_inicio,
            data__lte=data_fim
        ).order_by('-data')
        
        if not dados_atual.exists():
            continue
            
        # Agregações para totais do mês atual
        agregacoes_atual = dados_atual.aggregate(
            total_produtos=Sum('total_produtos'),
            produtos_respondidos=Sum('produtos_respondidos'),
            produtos_nao_respondidos=Sum('produtos_nao_respondidos'),
            produtos_gondola=Sum('produtos_gondola'),
            produtos_ruptura=Sum('produtos_ruptura'),
            produtos_presente=Sum('produtos_presente'),
            produtos_presente_reposto=Sum('produtos_presente_reposto')
        )
        
        # Dados históricos dos últimos 3 meses
        dados_historicos = []
        for mes_inicio, mes_fim in meses_anteriores:
            dados_mes = DadosLoja.objects.filter(
                loja=loja,
                data__gte=mes_inicio,
                data__lte=mes_fim
            ).order_by('-data')
            
            if dados_mes.exists():
                agregacoes_mes = dados_mes.aggregate(
                    total_produtos=Sum('total_produtos'),
                    produtos_respondidos=Sum('produtos_respondidos'),
                    produtos_nao_respondidos=Sum('produtos_nao_respondidos'),
                    produtos_gondola=Sum('produtos_gondola'),
                    produtos_ruptura=Sum('produtos_ruptura'),
                    produtos_presente=Sum('produtos_presente'),
                    produtos_presente_reposto=Sum('produtos_presente_reposto')
                )
                dados_historicos.append(agregacoes_mes)
        
        # Cálculos mais precisos com tratamento de divisão por zero
        total_produtos = agregacoes_atual['total_produtos'] or 0
        produtos_respondidos = agregacoes_atual['produtos_respondidos'] or 0
        produtos_nao_respondidos = agregacoes_atual['produtos_nao_respondidos'] or 0
        produtos_gondola = agregacoes_atual['produtos_gondola'] or 0
        produtos_ruptura = agregacoes_atual['produtos_ruptura'] or 0
        produtos_presente = agregacoes_atual['produtos_presente'] or 0
        produtos_presente_reposto = agregacoes_atual['produtos_presente_reposto'] or 0
        
        # Cálculos de porcentagens atuais
        porcentagem_respondidos = round((produtos_respondidos / total_produtos * 100) if total_produtos > 0 else 0, 1)
        porcentagem_nao_respondidos = round((produtos_nao_respondidos / total_produtos * 100) if total_produtos > 0 else 0, 1)
        porcentagem_gondola = round((produtos_gondola / produtos_respondidos * 100) if produtos_respondidos > 0 else 0, 1)
        porcentagem_ruptura = round((produtos_ruptura / produtos_respondidos * 100) if produtos_respondidos > 0 else 0, 1)
        porcentagem_presente = round((produtos_presente / produtos_gondola * 100) if produtos_gondola > 0 else 0, 1)
        porcentagem_presente_reposto = round((produtos_presente_reposto / produtos_presente * 100) if produtos_presente > 0 else 0, 1)
        
        # Cálculo de tendências
        tendencia_presente = 0
        tendencia_ruptura = 0
        tendencia_reposicao = 0
        
        if dados_historicos:
            # Calcula médias históricas
            media_presente = sum([
                (d['produtos_presente'] or 0) / (d['produtos_gondola'] or 1) * 100 
                for d in dados_historicos
            ]) / len(dados_historicos)
            
            media_ruptura = sum([
                (d['produtos_ruptura'] or 0) / (d['produtos_respondidos'] or 1) * 100 
                for d in dados_historicos
            ]) / len(dados_historicos)
            
            media_reposicao = sum([
                (d['produtos_presente_reposto'] or 0) / (d['produtos_presente'] or 1) * 100 
                for d in dados_historicos
            ]) / len(dados_historicos)
            
            # Calcula tendências
            tendencia_presente = round(porcentagem_presente - media_presente, 1)
            tendencia_ruptura = round(porcentagem_ruptura - media_ruptura, 1)
            tendencia_reposicao = round(porcentagem_presente_reposto - media_reposicao, 1)
        
        dados_loja = {
            'loja': loja,
            'total_produtos': total_produtos,
            'produtos_respondidos': produtos_respondidos,
            'produtos_nao_respondidos': produtos_nao_respondidos,
            'produtos_gondola': produtos_gondola,
            'produtos_ruptura': produtos_ruptura,
            'produtos_presente': produtos_presente,
            'produtos_presente_reposto': produtos_presente_reposto,
            'porcentagem_respondidos': porcentagem_respondidos,
            'porcentagem_nao_respondidos': porcentagem_nao_respondidos,
            'porcentagem_gondola': porcentagem_gondola,
            'porcentagem_ruptura': porcentagem_ruptura,
            'porcentagem_presente': porcentagem_presente,
            'porcentagem_presente_reposto': porcentagem_presente_reposto,
            'tendencia_presente': tendencia_presente,
            'tendencia_ruptura': tendencia_ruptura,
            'tendencia_reposicao': tendencia_reposicao
        }
        dados_lojas.append(dados_loja)
    
    # Ordena as lojas por cada métrica
    ranking_presente = sorted(dados_lojas, key=lambda x: x['porcentagem_presente'], reverse=True)
    ranking_ruptura = sorted(dados_lojas, key=lambda x: x['porcentagem_ruptura'])
    ranking_presente_reposto = sorted(dados_lojas, key=lambda x: x['porcentagem_presente_reposto'], reverse=True)
    
    # Prepara dados para o gráfico
    lojas_nomes = [loja['loja'].nome for loja in dados_lojas]
    dados_presente = [loja['porcentagem_presente'] for loja in dados_lojas]
    dados_ruptura = [loja['porcentagem_ruptura'] for loja in dados_lojas]
    dados_presente_reposto = [loja['porcentagem_presente_reposto'] for loja in dados_lojas]
    
    # Análise de Tendências e Evolução
    tendencias = []
    for loja in dados_lojas:
        nome_loja = loja['loja'].nome
        
        # Análise de Presença
        if loja['porcentagem_presente'] > 90:
            tendencias.append(f"{nome_loja}: Excelente presença em loja (>90%)")
        elif loja['porcentagem_presente'] > 80:
            tendencias.append(f"{nome_loja}: Boa presença em loja (80-90%)")
        else:
            tendencias.append(f"{nome_loja}: Presença em loja abaixo do ideal (<80%)")
        
        # Análise de Ruptura (critérios mais rigorosos)
        if loja['porcentagem_ruptura'] > 30:
            tendencias.append(f"⚠️ {nome_loja}: Ruptura EM RISCO CRÍTICO (>30%) - Perda de vendas e clientes")
        elif loja['porcentagem_ruptura'] > 20:
            tendencias.append(f"⚠️ {nome_loja}: Ruptura EM ALTO RISCO (20-30%) - Impacto significativo nas vendas")
        elif loja['porcentagem_ruptura'] > 15:
            tendencias.append(f"⚠️ {nome_loja}: Ruptura EM RISCO (15-20%) - Necessidade de ação imediata")
        elif loja['porcentagem_ruptura'] > 10:
            tendencias.append(f"⚠️ {nome_loja}: Ruptura ALERTA (10-15%) - Atenção necessária")
        else:
            tendencias.append(f"{nome_loja}: Ruptura controlada (<10%) - Manter monitoramento")
        
        # Análise de Reposição
        if loja['porcentagem_presente_reposto'] > 90:
            tendencias.append(f"{nome_loja}: Excelente taxa de reposição (>90%)")
        elif loja['porcentagem_presente_reposto'] > 80:
            tendencias.append(f"{nome_loja}: Boa taxa de reposição (80-90%)")
        else:
            tendencias.append(f"{nome_loja}: Taxa de reposição abaixo do ideal (<80%)")

    # Análise Comparativa
    analise_comparativa = []
    
    # Melhor e pior em presença
    melhor_presenca = max(dados_lojas, key=lambda x: x['porcentagem_presente'])
    pior_presenca = min(dados_lojas, key=lambda x: x['porcentagem_presente'])
    diferenca_presenca = melhor_presenca['porcentagem_presente'] - pior_presenca['porcentagem_presente']
    analise_comparativa.append(f"Melhor presença: {melhor_presenca['loja'].nome} ({melhor_presenca['porcentagem_presente']}%)")
    analise_comparativa.append(f"Pior presença: {pior_presenca['loja'].nome} ({pior_presenca['porcentagem_presente']}%)")
    analise_comparativa.append(f"Diferença: {diferenca_presenca:.1f} pontos percentuais")

    # Melhor e pior em ruptura (critérios mais rigorosos)
    melhor_ruptura = min(dados_lojas, key=lambda x: x['porcentagem_ruptura'])
    pior_ruptura = max(dados_lojas, key=lambda x: x['porcentagem_ruptura'])
    diferenca_ruptura = pior_ruptura['porcentagem_ruptura'] - melhor_ruptura['porcentagem_ruptura']
    analise_comparativa.append(f"Menor ruptura: {melhor_ruptura['loja'].nome} ({melhor_ruptura['porcentagem_ruptura']}%)")
    analise_comparativa.append(f"⚠️ Maior ruptura: {pior_ruptura['loja'].nome} ({pior_ruptura['porcentagem_ruptura']}%) - RISCO ALTO")
    analise_comparativa.append(f"Diferença: {diferenca_ruptura:.1f} pontos percentuais")

    # Melhor e pior em reposição
    melhor_reposicao = max(dados_lojas, key=lambda x: x['porcentagem_presente_reposto'])
    pior_reposicao = min(dados_lojas, key=lambda x: x['porcentagem_presente_reposto'])
    diferenca_reposicao = melhor_reposicao['porcentagem_presente_reposto'] - pior_reposicao['porcentagem_presente_reposto']
    analise_comparativa.append(f"Melhor reposição: {melhor_reposicao['loja'].nome} ({melhor_reposicao['porcentagem_presente_reposto']}%)")
    analise_comparativa.append(f"Pior reposição: {pior_reposicao['loja'].nome} ({pior_reposicao['porcentagem_presente_reposto']}%)")
    analise_comparativa.append(f"Diferença: {diferenca_reposicao:.1f} pontos percentuais")

    # Recomendações
    recomendacoes = []
    for loja in dados_lojas:
        # Recomendações baseadas em ruptura (critérios mais rigorosos)
        if loja['porcentagem_ruptura'] > 30:
            recomendacoes.append(f"⚠️ {loja['loja'].nome}: Ruptura EM RISCO CRÍTICO ({loja['porcentagem_ruptura']}%) - Implementar plano de emergência imediato para evitar perda de clientes")
        elif loja['porcentagem_ruptura'] > 20:
            recomendacoes.append(f"⚠️ {loja['loja'].nome}: Ruptura EM ALTO RISCO ({loja['porcentagem_ruptura']}%) - Ação urgente necessária para evitar impacto nas vendas")
        elif loja['porcentagem_ruptura'] > 15:
            recomendacoes.append(f"⚠️ {loja['loja'].nome}: Ruptura EM RISCO ({loja['porcentagem_ruptura']}%) - Revisar e corrigir processos de reposição")
        elif loja['porcentagem_ruptura'] > 10:
            recomendacoes.append(f"⚠️ {loja['loja'].nome}: Ruptura ALERTA ({loja['porcentagem_ruptura']}%) - Monitorar e ajustar reposição")
        else:
            recomendacoes.append(f"{loja['loja'].nome}: Ruptura controlada ({loja['porcentagem_ruptura']}%) - Manter monitoramento")

        # Recomendações baseadas em presença
        if loja['porcentagem_presente'] < 80:
            recomendacoes.append(f"{loja['loja'].nome}: Presença baixa ({loja['porcentagem_presente']}%) - Verificar abastecimento")
        elif loja['porcentagem_presente'] < 90:
            recomendacoes.append(f"{loja['loja'].nome}: Presença moderada ({loja['porcentagem_presente']}%) - Acompanhar evolução")
        else:
            recomendacoes.append(f"{loja['loja'].nome}: Presença excelente ({loja['porcentagem_presente']}%) - Manter padrão")

        # Recomendações baseadas em reposição
        if loja['porcentagem_presente_reposto'] < 80:
            recomendacoes.append(f"{loja['loja'].nome}: Reposição baixa ({loja['porcentagem_presente_reposto']}%) - Revisar processos")
        elif loja['porcentagem_presente_reposto'] < 90:
            recomendacoes.append(f"{loja['loja'].nome}: Reposição moderada ({loja['porcentagem_presente_reposto']}%) - Acompanhar evolução")
        else:
            recomendacoes.append(f"{loja['loja'].nome}: Reposição excelente ({loja['porcentagem_presente_reposto']}%) - Manter padrão")

    context = {
        'current_month': 'Março 2025',
        'ranking_presente': ranking_presente,
        'ranking_ruptura': ranking_ruptura,
        'ranking_presente_reposto': ranking_presente_reposto,
        'lojas_nomes': lojas_nomes,
        'dados_presente': dados_presente,
        'dados_ruptura': dados_ruptura,
        'dados_presente_reposto': dados_presente_reposto,
        'tendencias': tendencias,
        'analise_comparativa': analise_comparativa,
        'recomendacoes': recomendacoes,
    }

    return render(request, 'home/comparativo.html', context)

def inserir_dados(request):
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            mes = int(request.POST.get('mes'))
            ano = int(request.POST.get('ano'))
            nome_loja = request.POST.get('loja')
            
            # Obter a loja
            loja = Loja.objects.get(nome=nome_loja)
            
            # Criar data do primeiro dia do mês
            data = datetime(ano, mes, 1)
            
            # Verificar se já existem dados para este mês/loja
            if DadosLoja.objects.filter(loja=loja, data__year=ano, data__month=mes).exists():
                messages.warning(request, f'Já existem dados para {nome_loja} em {mes}/{ano}. Atualizando...')
                dados = DadosLoja.objects.get(loja=loja, data__year=ano, data__month=mes)
            else:
                dados = DadosLoja(loja=loja, data=data)
            
            # Atualizar dados
            dados.total_produtos = int(request.POST.get('total_produtos'))
            dados.produtos_respondidos = int(request.POST.get('produtos_respondidos'))
            dados.produtos_nao_respondidos = int(request.POST.get('produtos_nao_respondidos'))
            dados.produtos_gondola = int(request.POST.get('produtos_gondola'))
            dados.produtos_ruptura = int(request.POST.get('produtos_ruptura'))
            dados.produtos_presente = int(request.POST.get('produtos_presente'))
            dados.produtos_presente_reposto = int(request.POST.get('produtos_presente_reposto'))
            
            # Salvar dados
            dados.save()
            
            messages.success(request, f'Dados de {nome_loja} para {mes}/{ano} salvos com sucesso!')
            return redirect('inserir_dados')
            
        except Exception as e:
            messages.error(request, f'Erro ao salvar dados: {str(e)}')
            return redirect('inserir_dados')
    
    return render(request, 'home/inserir_dados.html')  