import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configuração de visualização
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10
sns.set_style('whitegrid')
sns.set_palette('Set2')

print("="*80)
print("ANÁLISE DE DADOS - E-COMMERCE BRASILEIRO")
print("Notebook 4: EDA - Análise Temporal e Categórica")
print("="*80)

# ============================================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================================
print("\n" + "="*80)
print("1. CARREGAMENTO DOS DADOS")
print("="*80)

df = pd.read_csv('../data/ecommerce_clean.csv')

# Reconverter datas
date_columns = ['Order_Date', 'D_Forecast', 'D_Date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

print(f"✓ Dados carregados: {len(df)} registros")

# ============================================================================
# 2. ANÁLISE TEMPORAL - SAZONALIDADE
# ============================================================================
print("\n" + "="*80)
print("2. ANÁLISE TEMPORAL - SAZONALIDADE")
print("="*80)

# Agregação mensal
monthly_data = df.groupby('order_month').agg({
    'Order_ID': 'count',
    'Total': ['sum', 'mean'],
    'is_confirmed': 'mean'
}).round(2)

monthly_data.columns = ['Num_Pedidos', 'Receita_Total', 'Ticket_Medio', 'Taxa_Confirmacao']
monthly_data['Taxa_Confirmacao'] = (monthly_data['Taxa_Confirmacao'] * 100).round(2)

print("\n--- Resumo Mensal ---")
print(monthly_data)

# Gráficos temporais
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Análise Temporal - Sazonalidade Mensal', fontsize=16, fontweight='bold')

# Número de pedidos por mês
months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out']
axes[0, 0].bar(range(1, 11), monthly_data['Num_Pedidos'], color='steelblue', edgecolor='black')
axes[0, 0].set_xlabel('Mês')
axes[0, 0].set_ylabel('Número de Pedidos')
axes[0, 0].set_title('Volume de Pedidos por Mês')
axes[0, 0].set_xticks(range(1, 11))
axes[0, 0].set_xticklabels(months)
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Receita total por mês
axes[0, 1].bar(range(1, 11), monthly_data['Receita_Total'], color='green', edgecolor='black')
axes[0, 1].set_xlabel('Mês')
axes[0, 1].set_ylabel('Receita Total (R$)')
axes[0, 1].set_title('Receita Total por Mês')
axes[0, 1].set_xticks(range(1, 11))
axes[0, 1].set_xticklabels(months)
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Ticket médio por mês
axes[1, 0].plot(range(1, 11), monthly_data['Ticket_Medio'], marker='o', linewidth=2, 
                markersize=8, color='orange')
axes[1, 0].set_xlabel('Mês')
axes[1, 0].set_ylabel('Ticket Médio (R$)')
axes[1, 0].set_title('Ticket Médio por Mês')
axes[1, 0].set_xticks(range(1, 11))
axes[1, 0].set_xticklabels(months)
axes[1, 0].grid(True, alpha=0.3)

# Taxa de confirmação por mês
axes[1, 1].plot(range(1, 11), monthly_data['Taxa_Confirmacao'], marker='s', linewidth=2,
                markersize=8, color='purple')
axes[1, 1].set_xlabel('Mês')
axes[1, 1].set_ylabel('Taxa de Confirmação (%)')
axes[1, 1].set_title('Taxa de Confirmação por Mês')
axes[1, 1].set_xticks(range(1, 11))
axes[1, 1].set_xticklabels(months)
axes[1, 1].axhline(monthly_data['Taxa_Confirmacao'].mean(), color='red', 
                   linestyle='--', label='Média Geral')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../figures/05_sazonalidade.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 05_sazonalidade.png")
plt.close()

# ============================================================================
# 3. ANÁLISE POR REGIÃO/UF
# ============================================================================
print("\n" + "="*80)
print("3. ANÁLISE POR REGIÃO/UF")
print("="*80)

# Agregação por região
region_data = df.groupby('Region').agg({
    'Order_ID': 'count',
    'Total': ['sum', 'mean'],
    'P_Service': 'mean',
    'is_confirmed': 'mean',
    'is_late': lambda x: x.mean() * 100
}).round(2)

region_data.columns = ['Num_Pedidos', 'Receita_Total', 'Ticket_Medio', 
                       'Frete_Medio', 'Taxa_Confirmacao', 'Taxa_Atraso']
region_data['Taxa_Confirmacao'] = (region_data['Taxa_Confirmacao'] * 100).round(2)

print("\n--- Resumo por Região ---")
print(region_data.sort_values('Receita_Total', ascending=False))

# Top 10 UFs
uf_data = df.groupby('UF').agg({
    'Order_ID': 'count',
    'Total': 'sum'
}).round(2)
uf_data.columns = ['Num_Pedidos', 'Receita_Total']
uf_data = uf_data.sort_values('Receita_Total', ascending=False).head(10)

print("\n--- Top 10 UFs por Receita ---")
print(uf_data)

# Gráficos por região
fig, axes = plt.subplots(1, 2, figsize=(18, 6))
fig.suptitle('Análise por Região', fontsize=16, fontweight='bold')

# Receita por região
region_data_sorted = region_data.sort_values('Receita_Total', ascending=True)
axes[0].barh(region_data_sorted.index, region_data_sorted['Receita_Total'], 
             color='teal', edgecolor='black')
axes[0].set_xlabel('Receita Total (R$)')
axes[0].set_title('Receita Total por Região')
axes[0].grid(True, alpha=0.3, axis='x')

# Frete médio por região
region_data_sorted_freight = region_data.sort_values('Frete_Medio', ascending=True)
axes[1].barh(region_data_sorted_freight.index, region_data_sorted_freight['Frete_Medio'],
             color='coral', edgecolor='black')
axes[1].set_xlabel('Frete Médio (R$)')
axes[1].set_title('Frete Médio por Região')
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('../figures/06_analise_regional.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 06_analise_regional.png")
plt.close()

# ============================================================================
# 4. ANÁLISE POR CATEGORIA DE PRODUTO
# ============================================================================
print("\n" + "="*80)
print("4. ANÁLISE POR CATEGORIA DE PRODUTO")
print("="*80)

# Agregação por categoria
category_data = df.groupby('Category').agg({
    'Order_ID': 'count',
    'Total': ['sum', 'mean'],
    'Discount': 'mean',
    'Quantity': 'sum'
}).round(2)

category_data.columns = ['Num_Pedidos', 'Receita_Total', 'Ticket_Medio', 
                         'Desconto_Medio', 'Qtd_Total']
category_data['Desconto_Medio'] = (category_data['Desconto_Medio'] * 100).round(2)
category_data['Participacao_Receita'] = (category_data['Receita_Total'] / 
                                          category_data['Receita_Total'].sum() * 100).round(2)

print("\n--- Resumo por Categoria ---")
print(category_data.sort_values('Receita_Total', ascending=False))

# Gráficos por categoria
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Análise por Categoria de Produto', fontsize=16, fontweight='bold')

# Participação na receita (pizza)
category_sorted = category_data.sort_values('Receita_Total', ascending=False)
colors_pie = sns.color_palette('Set2', len(category_sorted))
axes[0, 0].pie(category_sorted['Receita_Total'], labels=category_sorted.index, 
               autopct='%1.1f%%', startangle=90, colors=colors_pie)
axes[0, 0].set_title('Participação na Receita Total')

# Ticket médio por categoria
category_sorted_ticket = category_data.sort_values('Ticket_Medio', ascending=True)
axes[0, 1].barh(category_sorted_ticket.index, category_sorted_ticket['Ticket_Medio'],
                color='gold', edgecolor='black')
axes[0, 1].set_xlabel('Ticket Médio (R$)')
axes[0, 1].set_title('Ticket Médio por Categoria')
axes[0, 1].grid(True, alpha=0.3, axis='x')

# Desconto médio por categoria
category_sorted_discount = category_data.sort_values('Desconto_Medio', ascending=True)
axes[1, 0].barh(category_sorted_discount.index, category_sorted_discount['Desconto_Medio'],
                color='salmon', edgecolor='black')
axes[1, 0].set_xlabel('Desconto Médio (%)')
axes[1, 0].set_title('Desconto Médio por Categoria')
axes[1, 0].grid(True, alpha=0.3, axis='x')

# Volume de pedidos por categoria
category_sorted_volume = category_data.sort_values('Num_Pedidos', ascending=True)
axes[1, 1].barh(category_sorted_volume.index, category_sorted_volume['Num_Pedidos'],
                color='skyblue', edgecolor='black')
axes[1, 1].set_xlabel('Número de Pedidos')
axes[1, 1].set_title('Volume de Pedidos por Categoria')
axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('../figures/07_analise_categoria.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 07_analise_categoria.png")
plt.close()

# ============================================================================
# 5. ANÁLISE POR MÉTODO DE PAGAMENTO
# ============================================================================
print("\n" + "="*80)
print("5. ANÁLISE POR MÉTODO DE PAGAMENTO")
print("="*80)

# Agregação por método de pagamento
payment_data = df.groupby('Payment_Method').agg({
    'Order_ID': 'count',
    'Total': 'sum',
    'is_confirmed': lambda x: (x.sum() / len(x) * 100).round(2)
}).round(2)

payment_data.columns = ['Num_Pedidos', 'Receita_Total', 'Taxa_Confirmacao']
payment_data['Participacao'] = (payment_data['Num_Pedidos'] / 
                                 payment_data['Num_Pedidos'].sum() * 100).round(2)

print("\n--- Resumo por Método de Pagamento ---")
print(payment_data.sort_values('Num_Pedidos', ascending=False))

# Gráfico
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Análise por Método de Pagamento', fontsize=16, fontweight='bold')

# Distribuição de pedidos
payment_sorted = payment_data.sort_values('Num_Pedidos', ascending=False)
axes[0].bar(range(len(payment_sorted)), payment_sorted['Num_Pedidos'], 
            color='mediumseagreen', edgecolor='black')
axes[0].set_xticks(range(len(payment_sorted)))
axes[0].set_xticklabels(payment_sorted.index, rotation=45, ha='right')
axes[0].set_ylabel('Número de Pedidos')
axes[0].set_title('Volume de Pedidos por Método de Pagamento')
axes[0].grid(True, alpha=0.3, axis='y')

# Taxa de confirmação
payment_sorted_conf = payment_data.sort_values('Taxa_Confirmacao', ascending=False)
axes[1].bar(range(len(payment_sorted_conf)), payment_sorted_conf['Taxa_Confirmacao'],
            color='mediumpurple', edgecolor='black')
axes[1].set_xticks(range(len(payment_sorted_conf)))
axes[1].set_xticklabels(payment_sorted_conf.index, rotation=45, ha='right')
axes[1].set_ylabel('Taxa de Confirmação (%)')
axes[1].set_title('Taxa de Confirmação por Método de Pagamento')
axes[1].axhline(payment_data['Taxa_Confirmacao'].mean(), color='red', 
                linestyle='--', label='Média Geral')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../figures/08_analise_pagamento.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 08_analise_pagamento.png")
plt.close()

# ============================================================================
# 6. ANÁLISE POR TIPO DE SERVIÇO DE ENTREGA
# ============================================================================
print("\n" + "="*80)
print("6. ANÁLISE POR TIPO DE SERVIÇO DE ENTREGA")
print("="*80)

# Agregação por serviço
service_data = df[df['is_confirmed'] == 1].groupby('Services').agg({
    'Order_ID': 'count',
    'P_Service': 'mean',
    'delivery_lead_time': 'mean',
    'is_late': lambda x: (x.mean() * 100).round(2)
}).round(2)

service_data.columns = ['Num_Pedidos', 'Frete_Medio', 'Prazo_Medio', 'Taxa_Atraso']

print("\n--- Resumo por Tipo de Serviço ---")
print(service_data.sort_values('Num_Pedidos', ascending=False))

# Gráfico
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Performance Logística por Tipo de Serviço', fontsize=16, fontweight='bold')

# Frete médio
service_sorted = service_data.sort_values('Frete_Medio', ascending=False)
axes[0].bar(service_sorted.index, service_sorted['Frete_Medio'], 
            color='indianred', edgecolor='black')
axes[0].set_ylabel('Frete Médio (R$)')
axes[0].set_title('Frete Médio por Tipo de Serviço')
axes[0].grid(True, alpha=0.3, axis='y')

# Prazo médio
service_sorted_time = service_data.sort_values('Prazo_Medio', ascending=False)
axes[1].bar(service_sorted_time.index, service_sorted_time['Prazo_Medio'],
            color='lightcoral', edgecolor='black')
axes[1].set_ylabel('Prazo Médio (dias)')
axes[1].set_title('Prazo Médio de Entrega por Tipo de Serviço')
axes[1].grid(True, alpha=0.3, axis='y')

# Taxa de atraso
service_sorted_late = service_data.sort_values('Taxa_Atraso', ascending=False)
axes[2].bar(service_sorted_late.index, service_sorted_late['Taxa_Atraso'],
            color='tomato', edgecolor='black')
axes[2].set_ylabel('Taxa de Atraso (%)')
axes[2].set_title('Taxa de Atraso por Tipo de Serviço')
axes[2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../figures/09_analise_servico.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 09_analise_servico.png")
plt.close()

print("\n" + "="*80)
print("FIM DO NOTEBOOK 4")
print("="*80)