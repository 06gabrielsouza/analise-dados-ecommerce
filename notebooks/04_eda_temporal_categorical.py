import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10
sns.set_style('whitegrid')

print("="*80)
print("NOTEBOOK 4: CORRIGIDO (DADOS DINÂMICOS)")
print("="*80)

# 1. Carregar
df = pd.read_csv('../data/ecommerce_clean.csv')
for col in ['Order_Date', 'D_Forecast', 'D_Date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# 2. Sazonalidade (CORREÇÃO AQUI: Usa os meses que existem, não fixos)
monthly_data = df.groupby('order_month').agg({
    'Order_ID': 'count',
    'Total': ['sum', 'mean'],
    'is_confirmed': 'mean'
}).round(2)

monthly_data.columns = ['Num_Pedidos', 'Receita_Total', 'Ticket_Medio', 'Taxa_Confirmacao']
monthly_data['Taxa_Confirmacao'] = (monthly_data['Taxa_Confirmacao'] * 100).round(2)

# Gráficos Dinâmicos
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
meses_presentes = monthly_data.index

# Volume
axes[0, 0].bar(meses_presentes, monthly_data['Num_Pedidos'], color='steelblue', edgecolor='black')
axes[0, 0].set_title('Volume de Pedidos por Mês')
axes[0, 0].set_xticks(meses_presentes)

# Receita
axes[0, 1].bar(meses_presentes, monthly_data['Receita_Total'], color='green', edgecolor='black')
axes[0, 1].set_title('Receita Total por Mês')
axes[0, 1].set_xticks(meses_presentes)

# Ticket Médio
axes[1, 0].plot(meses_presentes, monthly_data['Ticket_Medio'], marker='o', color='orange')
axes[1, 0].set_title('Ticket Médio por Mês')
axes[1, 0].set_xticks(meses_presentes)

# Taxa Confirmação
axes[1, 1].plot(meses_presentes, monthly_data['Taxa_Confirmacao'], marker='s', color='purple')
axes[1, 1].set_title('Taxa de Confirmação (%)')
axes[1, 1].set_xticks(meses_presentes)

plt.tight_layout()
plt.savefig('../figures/05_sazonalidade.png')
print("✓ Gráfico de Sazonalidade salvo.")

# 3. Análise Regional
region_data = df.groupby('Region')['Total'].sum().sort_values()
plt.figure(figsize=(10, 6))
region_data.plot(kind='barh', color='teal')
plt.title('Receita por Região')
plt.tight_layout()
plt.savefig('../figures/06_analise_regional.png')
print("✓ Gráfico Regional salvo.")

# 4. Categoria
cat_data = df.groupby('Category')['Total'].sum().sort_values()
plt.figure(figsize=(10, 6))
cat_data.plot(kind='barh', color='salmon')
plt.title('Receita por Categoria')
plt.tight_layout()
plt.savefig('../figures/07_analise_categoria.png')
print("✓ Gráfico de Categoria salvo.")

# 5. Pagamento
pay_data = df['Payment_Method'].value_counts()
plt.figure(figsize=(8, 8))
pay_data.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Métodos de Pagamento')
plt.savefig('../figures/08_analise_pagamento.png')
print("✓ Gráfico de Pagamento salvo.")

# 6. Serviços
serv_data = df.groupby('Services')['is_late'].mean() * 100
plt.figure(figsize=(10, 6))
serv_data.sort_values().plot(kind='bar', color='tomato')
plt.title('Taxa de Atraso por Serviço (%)')
plt.tight_layout()
plt.savefig('../figures/09_analise_servico.png')
print("✓ Gráfico de Serviço salvo.")