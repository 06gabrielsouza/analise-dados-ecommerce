import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("NOTEBOOK 1: INTEGRACAO E LIMPEZA (DADOS REAIS) - VERSÃO CORRIGIDA")
print("="*80)

# Caminho dos arquivos
DATA_DIR = '../data'

# 1. CARREGAR AS 5 TABELAS
print("\n1. Carregando tabelas...")
try:
    # encoding='utf-8-sig' remove o BOM que as vezes vem do Excel
    orders = pd.read_csv(os.path.join(DATA_DIR, 'FACT_Orders.csv'), encoding='utf-8-sig')
    customers = pd.read_csv(os.path.join(DATA_DIR, 'DIM_Customer.csv'), encoding='utf-8-sig')
    delivery = pd.read_csv(os.path.join(DATA_DIR, 'DIM_Delivery.csv'), encoding='utf-8-sig')
    shopping = pd.read_csv(os.path.join(DATA_DIR, 'DIM_Shopping.csv'), encoding='utf-8-sig')
    products = pd.read_csv(os.path.join(DATA_DIR, 'DIM_Products.csv'), encoding='utf-8-sig')
    
    # LIMPEZA DE CABEÇALHOS (Remove espaços invisíveis: 'Id ' -> 'Id')
    for tabela in [orders, customers, delivery, shopping, products]:
        tabela.columns = tabela.columns.str.strip()
        
    print("✓ Todas as tabelas carregadas e higienizadas!")
except FileNotFoundError as e:
    print(f"❌ Erro: {e}")
    exit()

# 2. UNIFICAR OS DADOS (MERGE)
print("\n2. Unificando dados...")

# Verifica se a coluna 'Id' existe
if 'Id' not in orders.columns:
    print(f"❌ Erro Crítico: Coluna 'Id' não encontrada em FACT_Orders. Colunas disponíveis: {list(orders.columns)}")
    exit()

# Merge
df = orders.merge(customers, on='Id', how='left')
df = df.merge(delivery, on='Id', how='left')
df = df.merge(shopping, on='Id', how='left')
df = df.merge(products, left_on='Product', right_on='Product_Name', how='left')

print(f"✓ Dados unificados: {len(df)} registros")

# 3. RENOMEAR COLUNAS
print("\n3. Padronizando colunas...")

# Dicionário de Tradução
de_para = {
    'Id': 'Order_ID',
    'Order_Date': 'Order_Date',
    'Total': 'Total',
    'Subtotal': 'Subtotal',
    'Discount': 'Discount',
    'payment': 'Payment_Method',
    'Purchase_Status': 'Purchase_Status',
    'State': 'UF',
    'Region_x': 'Region',  # Prioriza região do Cliente
    'Region_y': 'Region_Alt', # Caso venha duplicado
    'P_Sevice': 'P_Service', # Typo original
    'P_Service': 'P_Service', # Caso já esteja corrigido
    'D_Forecast': 'D_Forecast',
    'D_Date': 'D_Date',
    'Services': 'Services',
    'Category': 'Category',
    'Subcategory': 'Subcategory',
    'Quantity': 'Quantity'
}

# Renomear
df_final = df.rename(columns=de_para)

# Tratamento especial para Região (se x e y existirem)
if 'Region' not in df_final.columns and 'Region_x' in df.columns:
    df_final['Region'] = df['Region_x']

# 4. SELEÇÃO DE COLUNAS
# Garante que Order_ID está presente
if 'Order_ID' not in df_final.columns:
    print("⚠️ Aviso: Renomeação de ID falhou. Forçando criação...")
    if 'Id' in df.columns:
        df_final['Order_ID'] = df['Id']
    else:
        # Se tudo falhar, usa o índice
        df_final['Order_ID'] = df_final.index + 1

# Lista de colunas desejadas que realmente existem no DF
cols_desejadas = ['Order_ID', 'Order_Date', 'Total', 'Subtotal', 'Discount', 'P_Service', 
                  'Payment_Method', 'Purchase_Status', 'UF', 'Region', 'Category', 
                  'D_Forecast', 'D_Date', 'Services', 'Quantity']

cols_finais = [c for c in cols_desejadas if c in df_final.columns]
df_final = df_final[cols_finais]

# Preencher Frete vazio com 0 para não dar erro depois
if 'P_Service' in df_final.columns:
    df_final['P_Service'] = df_final['P_Service'].fillna(0)

# 5. SALVAR
output_path = os.path.join(DATA_DIR, 'ecommerce_cleaned_checkpoint.csv')
df_final.to_csv(output_path, index=False)
print(f"\n✓ Arquivo salvo em: {output_path}")
print("✓ Colunas salvas:", list(df_final.columns))
print("Agora pode rodar o script 02!")