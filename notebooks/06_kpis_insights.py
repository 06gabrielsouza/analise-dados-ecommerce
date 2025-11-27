# 06_kpis_insights.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Constantes ---
CAMINHO_DADOS = 'data/ecommerce_clean.csv'
FIGURA_SAIDA = 'figures/13_dashboard_kpis.png'

def carregar_dados(caminho):
    """Carrega os dados limpos."""
    try:
        df = pd.read_csv(caminho)
        # Converter colunas de data (ajuste os nomes)
        df['data_pedido'] = pd.to_datetime(df['data_pedido'])
        df['data_entrega'] = pd.to_datetime(df['data_entrega_real'])
        df['data_estimada'] = pd.to_datetime(df['data_entrega_estimada'])
        print("Dados limpos carregados com sucesso.")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo {CAMINHO_DADOS} não encontrado.")
        return None

def calcular_kpis(df):
    """Calcula os principais KPIs."""
    print("\n--- Calculando KPIs ---")
    kpis = {}
    
    # Total de Pedidos
    kpis['total_pedidos'] = df['id_pedido'].nunique()
    
    # Receita Total (GMV)
    kpis['receita_total'] = df['valor_pedido'].sum()
    
    # Ticket Médio
    kpis['ticket_medio'] = kpis['receita_total'] / kpis['total_pedidos']
    
    # Taxa de Cancelamento
    total_cancelados = df[df['status_pedido'] == 'Cancelado']['id_pedido'].nunique()
    kpis['taxa_cancelamento'] = (total_cancelados / kpis['total_pedidos']) * 100
    
    # Taxa de Atraso
    df_entregues = df[df['status_pedido'] == 'Entregue'].dropna(subset=['data_entrega', 'data_estimada'])
    total_atrasos = (df_entregues['data_entrega'] > df_entregues['data_estimada']).sum()
    kpis['taxa_atraso'] = (total_atrasos / len(df_entregues)) * 100
    
    print("KPIs calculados:")
    for key, value in kpis.items():
        if isinstance(value, float) and key != 'ticket_medio':
            print(f"- {key}: {value:.2f}%")
        elif key == 'ticket_medio':
             print(f"- {key}: ${value:.2f}")
        else:
            print(f"- {key}: {value}")
            
    return kpis

def analisar_elasticidade_simples(df):
    """Gera dados para análise de elasticidade (simplificada)."""
    # Elasticidade real exige modelos de regressão complexos.
    # Isto é uma aproximação: agrupar por nível de desconto e ver o impacto.
    print("\n--- Análise de Elasticidade (Simplificada) ---")
    
    # Assumindo que 'desconto_percentual' e 'quantidade' existem
    if 'desconto_percentual' not in df.columns or 'quantidade' not in df.columns:
        print("Colunas 'desconto_percentual' ou 'quantidade' não encontradas. Pulando elasticidade.")
        return None

    # Agrupa por desconto e calcula a quantidade média vendida
    df_elasticidade = df.groupby('desconto_percentual')['quantidade'].mean().reset_index()
    print(df_elasticidade.head())
    return df_elasticidade

def gerar_dashboard(df, kpis):
    """Gera um dashboard consolidado com os principais insights."""
    print(f"\n--- Gerando Dashboard em {FIGURA_SAIDA} ---")
    
    # Configuração do Dashboard (Grid 2x2)
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle('Dashboard de Performance E-commerce', fontsize=20, weight='bold')
    sns.set_style('whitegrid')

    # --- Gráfico 1: Receita por Categoria (Ex: Eletrônicos) ---
    # (Substitua 'categoria_produto' e 'valor_pedido')
    receita_categoria = df.groupby('categoria_produto')['valor_pedido'].sum().nlargest(5).sort_values(ascending=False)
    sns.barplot(x=receita_categoria.values, y=receita_categoria.index, ax=axes[0, 0], palette='viridis')
    axes[0, 0].set_title('Top 5 Categorias por Receita', fontsize=14)
    axes[0, 0].set_xlabel('Receita Total (R$)')
    axes[0, 0].set_ylabel('Categoria')

    # --- Gráfico 2: Taxa de Cancelamento por Pagamento ---
    # (Substitua 'metodo_pagamento' e 'status_pedido')
    df_cancel = df.groupby('metodo_pagamento')['status_pedido'].apply(lambda x: (x == 'Cancelado').mean() * 100).sort_values(ascending=False)
    sns.barplot(x=df_cancel.index, y=df_cancel.values, ax=axes[0, 1], palette='OrRd_r')
    axes[0, 1].set_title('Taxa de Cancelamento por Método de Pagamento', fontsize=14)
    axes[0, 1].set_ylabel('Taxa de Cancelamento (%)')
    axes[0, 1].set_xlabel('Método de Pagamento')

    # --- Gráfico 3: Taxa de Atraso por Região ---
    # (Substitua 'regiao' e as colunas de data)
    df_entregues = df[df['status_pedido'] == 'Entregue'].dropna(subset=['data_entrega', 'data_estimada', 'regiao'])
    df_entregues['atrasado'] = df_entregues['data_entrega'] > df_entregues['data_estimada']
    taxa_atraso_regiao = df_entregues.groupby('regiao')['atrasado'].mean().sort_values(ascending=False) * 100
    sns.barplot(x=taxa_atraso_regiao.index, y=taxa_atraso_regiao.values, ax=axes[1, 0], palette='coolwarm')
    axes[1, 0].set_title('Taxa de Atraso na Entrega por Região', fontsize=14)
    axes[1, 0].set_ylabel('Taxa de Atraso (%)')
    axes[1, 0].set_xlabel('Região')

    # --- Gráfico 4: KPIs Principais (Texto) ---
    axes[1, 1].axis('off')
    kpi_texto = f"""
    Principais KPIs:
    
    Receita Total: R$ {kpis['receita_total']:,.2f}
    Total de Pedidos: {kpis['total_pedidos']:,}
    Ticket Médio: R$ {kpis['ticket_medio']:.2f}
    
    Taxa de Cancelamento: {kpis['taxa_cancelamento']:.2f}%
    Taxa de Atraso: {kpis['taxa_atraso']:.2f}%
    """
    axes[1, 1].text(0.5, 0.5, kpi_texto, 
                    ha='center', va='center', fontsize=16, 
                    fontfamily='monospace',
                    bbox=dict(boxstyle="round,pad=0.5", fc='aliceblue', ec='grey', lw=1))
    axes[1, 1].set_title('Visão Geral dos KPIs', fontsize=14)

    # Salvar a figura
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(FIGURA_SAIDA, dpi=150, bbox_inches='tight')
    print(f"Dashboard salvo com sucesso em {FIGURA_SAIDA}")

def main():
    df = carregar_dados(CAMINHO_DADOS)
    if df is None:
        return
        
    kpis = calcular_kpis(df)
    
    # A análise de elasticidade é complexa e pode exigir um script separado
    # analisar_elasticidade_simples(df) 
    
    gerar_dashboard(df, kpis)

if __name__ == "__main__":
    main()