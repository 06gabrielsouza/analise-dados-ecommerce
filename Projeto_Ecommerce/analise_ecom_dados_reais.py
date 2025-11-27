import pandas as pd
import matplotlib.pyplot as plt
import os

# ==============================================================================
# 1. CONFIGURAÇÃO DOS ARQUIVOS (Ajuste os nomes se necessário)
# ==============================================================================
ARQUIVOS = {
    'pedidos':  'FACT_Orders.csv',
    'clientes': 'DIM_Customer.csv',
    'entrega':  'DIM_Delivery.csv',
    'itens':    'DIM_Shopping.csv',
    'produtos': 'DIM_Products.csv'
}

# ==============================================================================
# 2. FUNÇÃO DE INTEGRAÇÃO DE DADOS (O "Cérebro" da Adaptação)
# ==============================================================================
def carregar_e_unificar_dados():
    print("📂 Carregando tabelas do banco de dados...")
    
    # Verificar se arquivos existem
    for nome, arquivo in ARQUIVOS.items():
        if not os.path.exists(arquivo):
            print(f"❌ Erro: Arquivo '{arquivo}' não encontrado.")
            return None

    # 1. Carregar as tabelas
    df_orders   = pd.read_csv(ARQUIVOS['pedidos'])
    df_customer = pd.read_csv(ARQUIVOS['clientes'])
    df_delivery = pd.read_csv(ARQUIVOS['entrega'])
    df_shopping = pd.read_csv(ARQUIVOS['itens'])
    df_products = pd.read_csv(ARQUIVOS['produtos'])

    print("🔄 Unificando as tabelas (Merge)...")
    
    # 2. Juntar Tabela Fato (Pedidos) com Dimensões (Cliente, Entrega, Shopping)
    # Usamos o 'Id' como chave comum entre elas
    df_full = df_orders.merge(df_customer, on='Id', how='left')
    df_full = df_full.merge(df_delivery, on='Id', how='left')
    df_full = df_full.merge(df_shopping, on='Id', how='left')
    
    # 3. Juntar com Produtos para pegar a Categoria
    # A tabela Shopping tem 'Product', a tabela Products tem 'Product_Name'
    df_full = df_full.merge(df_products, left_on='Product', right_on='Product_Name', how='left')

    print("✅ Tabelas unificadas com sucesso!")
    
    # 4. Selecionar e Renomear para o padrão do nosso script de análise
    # Mapeamento: Nome na sua base nova -> Nome que o script de análise usa
    tabela_final = df_full.rename(columns={
        'Id':               'Codigo_Pedido',
        'Order_Date':       'Data_Venda',
        'Total':            'Valor_Final',
        'P_Sevice':         'Valor_Frete',    # Corrigindo possível typo 'Sevice' do arquivo
        'Subtotal':         'Valor_Produtos',
        'Category':         'Categoria',      # Veio da tabela DIM_Products
        'Region':           'Regiao',         # Veio da tabela DIM_Customer
        'Purchase_Status':  'Status',
        'D_Date':           'Data_Entrega_Real',
        'D_Forecast':       'Data_Entrega_Prevista',
        'payment':          'Metodo_Pagamento'
    })
    
    # Tratamento para caso a coluna de frete tenha vindo com nome diferente no merge
    if 'Valor_Frete' not in tabela_final.columns and 'P_Sevice' in df_delivery.columns:
         tabela_final['Valor_Frete'] = df_delivery['P_Sevice']

    return tabela_final

# ==============================================================================
# 3. FUNÇÕES DE LIMPEZA E CÁLCULO (Mantidas do script anterior)
# ==============================================================================
def corrigir_dados(tabela):
    print("🧹 Limpando e organizando tipos de dados...")
    
    # Converter datas
    cols_data = ['Data_Venda', 'Data_Entrega_Real', 'Data_Entrega_Prevista']
    for col in cols_data:
        if col in tabela.columns:
            tabela[col] = pd.to_datetime(tabela[col], errors='coerce')

    # Converter numéricos
    cols_num = ['Valor_Final', 'Valor_Frete']
    for col in cols_num:
        if col in tabela.columns:
            tabela[col] = pd.to_numeric(tabela[col], errors='coerce').fillna(0)
            
    # Criar indicadores
    if 'Data_Entrega_Real' in tabela.columns and 'Data_Venda' in tabela.columns:
        tabela['Dias_Entrega'] = (tabela['Data_Entrega_Real'] - tabela['Data_Venda']).dt.days
        
    if 'Data_Entrega_Real' in tabela.columns and 'Data_Entrega_Prevista' in tabela.columns:
        tabela['Atrasou'] = tabela['Data_Entrega_Real'] > tabela['Data_Entrega_Prevista']
        
    if 'Data_Venda' in tabela.columns:
        tabela['Mes_Venda'] = tabela['Data_Venda'].dt.to_period('M')

    return tabela

# ==============================================================================
# 4. FUNÇÕES DE VISUALIZAÇÃO E RELATÓRIO
# ==============================================================================
def gerar_relatorio(tabela):
    # Filtra apenas confirmados para análise financeira
    vendas = tabela[tabela['Status'] == 'Confirmado']
    
    print("\n" + "="*40)
    print("📊 RELATÓRIO EXECUTIVO E-COMMERCE")
    print("="*40)
    
    # 1. Financeiro
    fat_total = vendas['Valor_Final'].sum()
    frete_total = vendas['Valor_Frete'].sum()
    ticket = vendas['Valor_Final'].mean()
    
    print(f"💰 Faturamento Total:   R$ {fat_total:,.2f}")
    print(f"📦 Total de Pedidos:    {len(vendas)}")
    print(f"🎫 Ticket Médio:        R$ {ticket:,.2f}")
    print(f"🚚 Custo Total Frete:   R$ {frete_total:,.2f}")
    
    # 2. Logística
    if 'Atrasou' in vendas.columns:
        atrasos = vendas['Atrasou'].sum()
        taxa_atraso = (atrasos / len(vendas)) * 100
        print(f"⚠️ Pedidos com Atraso:  {atrasos} ({taxa_atraso:.1f}%)")
    
    # 3. Top Categorias
    if 'Categoria' in vendas.columns:
        print("\n🏆 Top 3 Categorias:")
        top_cat = vendas.groupby('Categoria')['Valor_Final'].sum().sort_values(ascending=False).head(3)
        for cat, val in top_cat.items():
            print(f"   - {cat}: R$ {val:,.2f}")

def gerar_graficos(tabela):
    print("\n📈 Gerando gráficos...")
    vendas = tabela[tabela['Status'] == 'Confirmado']
    
    # Gráfico 1: Vendas por Mês
    if 'Mes_Venda' in vendas.columns:
        plt.figure(figsize=(10, 5))
        vendas.groupby('Mes_Venda')['Valor_Final'].sum().plot(kind='bar', color='royalblue')
        plt.title('Faturamento Mensal')
        plt.xlabel('Mês')
        plt.ylabel('Reais (R$)')
        plt.tight_layout()
        plt.savefig('grafico_vendas_reais.png')
        print("✓ Gráfico salvo: grafico_vendas_reais.png")

    # Gráfico 2: Vendas por Região
    if 'Regiao' in vendas.columns:
        plt.figure(figsize=(8, 5))
        vendas.groupby('Regiao')['Valor_Final'].sum().sort_values().plot(kind='barh', color='green')
        plt.title('Faturamento por Região')
        plt.tight_layout()
        plt.savefig('grafico_regiao_reais.png')
        print("✓ Gráfico salvo: grafico_regiao_reais.png")

# ==============================================================================
# 5. EXECUÇÃO
# ==============================================================================
if __name__ == "__main__":
    dados = carregar_e_unificar_dados()
    
    if dados is not None:
        dados_processados = corrigir_dados(dados)
        gerar_relatorio(dados_processados)
        gerar_graficos(dados_processados)
        
        print("\n✅ Análise concluída com a nova base de dados!")