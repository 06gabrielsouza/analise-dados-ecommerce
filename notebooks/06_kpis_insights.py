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

print("="*80)
print("ANÁLISE DE DADOS - E-COMMERCE BRASILEIRO")
print("Notebook 6: KPIs e Insights de Negócio")
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
# 2. KPIs PRINCIPAIS
# ============================================================================
print("\n" + "="*80)
print("2. KPIs PRINCIPAIS")
print("="*80)

# Filtrar apenas pedidos confirmados para alguns KPIs
df_confirmed = df[df['is_confirmed'] == 1]

# 2.1 KPIs Financeiros
print("\n--- KPIs FINANCEIROS ---")

receita_total = df_confirmed['Total'].sum()
subtotal_total = df_confirmed['Subtotal'].sum()
frete_total = df_confirmed['P_Service'].sum()
desconto_total = df_confirmed['discount_abs'].sum()

ticket_medio = df_confirmed['Total'].mean()
subtotal_medio = df_confirmed['Subtotal'].mean()
frete_medio = df_confirmed['P_Service'].mean()
desconto_medio_pct = df_confirmed['Discount'].mean() * 100

# Take-rate de frete
take_rate_frete = (frete_total / receita_total) * 100

print(f"Receita Total: R$ {receita_total:,.2f}")
print(f"Subtotal Total: R$ {subtotal_total:,.2f}")
print(f"Frete Total: R$ {frete_total:,.2f}")
print(f"Desconto Total: R$ {desconto_total:,.2f}")
print(f"\nTicket Médio: R$ {ticket_medio:.2f}")
print(f"Subtotal Médio: R$ {subtotal_medio:.2f}")
print(f"Frete Médio: R$ {frete_medio:.2f}")
print(f"Desconto Médio: {desconto_medio_pct:.2f}%")
print(f"\nTake-rate de Frete: {take_rate_frete:.2f}%")

# 2.2 KPIs Operacionais
print("\n--- KPIs OPERACIONAIS ---")

num_pedidos_total = len(df)
num_pedidos_confirmados = len(df_confirmed)
num_pedidos_cancelados = len(df[df['is_confirmed'] == 0])

taxa_confirmacao = (num_pedidos_confirmados / num_pedidos_total) * 100
taxa_cancelamento = (num_pedidos_cancelados / num_pedidos_total) * 100

print(f"Total de Pedidos: {num_pedidos_total:,}")
print(f"Pedidos Confirmados: {num_pedidos_confirmados:,}")
print(f"Pedidos Cancelados: {num_pedidos_cancelados:,}")
print(f"\nTaxa de Confirmação: {taxa_confirmacao:.2f}%")
print(f"Taxa de Cancelamento: {taxa_cancelamento:.2f}%")

# 2.3 KPIs Logísticos
print("\n--- KPIs LOGÍSTICOS ---")

prazo_medio_entrega = df_confirmed['delivery_lead_time'].mean()
atraso_medio = df_confirmed['delivery_delay_days'].mean()
taxa_atraso = (df_confirmed['is_late'].sum() / len(df_confirmed)) * 100

# Pedidos no prazo, com atraso leve e atraso grave
no_prazo = (df_confirmed['delivery_delay_days'] <= 0).sum()
atraso_leve = ((df_confirmed['delivery_delay_days'] > 0) & 
               (df_confirmed['delivery_delay_days'] <= 5)).sum()
atraso_grave = (df_confirmed['delivery_delay_days'] > 5).sum()

print(f"Prazo Médio de Entrega: {prazo_medio_entrega:.1f} dias")
print(f"Atraso Médio: {atraso_medio:.1f} dias")
print(f"Taxa de Atraso: {taxa_atraso:.2f}%")
print(f"\nPedidos no Prazo: {no_prazo:,} ({no_prazo/len(df_confirmed)*100:.1f}%)")
print(f"Atraso Leve (1-5 dias): {atraso_leve:,} ({atraso_leve/len(df_confirmed)*100:.1f}%)")
print(f"Atraso Grave (>5 dias): {atraso_grave:,} ({atraso_grave/len(df_confirmed)*100:.1f}%)")

# ============================================================================
# 3. PERFORMANCE POR MÉTODO DE PAGAMENTO
# ============================================================================
print("\n" + "="*80)
print("3. PERFORMANCE POR MÉTODO DE PAGAMENTO")
print("="*80)

payment_kpis = df.groupby('Payment_Method').agg({
    'Order_ID': 'count',
    'Total': 'sum',
    'is_confirmed': lambda x: (x.sum() / len(x) * 100)
}).round(2)

payment_kpis.columns = ['Num_Pedidos', 'Receita_Total', 'Taxa_Confirmacao']
payment_kpis['Participacao_Pedidos'] = (payment_kpis['Num_Pedidos'] / 
                                         payment_kpis['Num_Pedidos'].sum() * 100).round(2)
payment_kpis['Participacao_Receita'] = (payment_kpis['Receita_Total'] / 
                                         payment_kpis['Receita_Total'].sum() * 100).round(2)

payment_kpis = payment_kpis.sort_values('Receita_Total', ascending=False)

print("\n--- KPIs por Método de Pagamento ---")
print(payment_kpis)

# Insight: Conversão por método de pagamento
print("\n--- INSIGHT: Conversão por Método de Pagamento ---")
best_payment = payment_kpis['Taxa_Confirmacao'].idxmax()
worst_payment = payment_kpis['Taxa_Confirmacao'].idxmin()
print(f"✓ Melhor conversão: {best_payment} ({payment_kpis.loc[best_payment, 'Taxa_Confirmacao']:.2f}%)")
print(f"✗ Pior conversão: {worst_payment} ({payment_kpis.loc[worst_payment, 'Taxa_Confirmacao']:.2f}%)")

# ============================================================================
# 4. PERFORMANCE LOGÍSTICA POR SERVIÇO
# ============================================================================
print("\n" + "="*80)
print("4. PERFORMANCE LOGÍSTICA POR SERVIÇO")
print("="*80)

service_kpis = df_confirmed.groupby('Services').agg({
    'Order_ID': 'count',
    'P_Service': 'mean',
    'delivery_lead_time': 'mean',
    'delivery_delay_days': 'mean',
    'is_late': lambda x: (x.sum() / len(x) * 100)
}).round(2)

service_kpis.columns = ['Num_Pedidos', 'Frete_Medio', 'Prazo_Medio', 
                        'Atraso_Medio', 'Taxa_Atraso']
service_kpis['Participacao'] = (service_kpis['Num_Pedidos'] / 
                                 service_kpis['Num_Pedidos'].sum() * 100).round(2)

service_kpis = service_kpis.sort_values('Num_Pedidos', ascending=False)

print("\n--- KPIs por Tipo de Serviço ---")
print(service_kpis)

# Insight: Relação custo-benefício dos serviços
print("\n--- INSIGHT: Análise de Serviços de Entrega ---")
print(f"✓ Standard: Mais usado ({service_kpis.loc['Standard', 'Participacao']:.1f}%), "
      f"frete baixo (R$ {service_kpis.loc['Standard', 'Frete_Medio']:.2f}), "
      f"mas maior prazo ({service_kpis.loc['Standard', 'Prazo_Medio']:.1f} dias)")
print(f"✓ Same-Day: Mais caro (R$ {service_kpis.loc['Same-Day', 'Frete_Medio']:.2f}), "
      f"mas entrega rápida ({service_kpis.loc['Same-Day', 'Prazo_Medio']:.1f} dias)")
print(f"✓ Scheduled: Equilíbrio entre custo e prazo")

# ============================================================================
# 5. MIX DE PRODUTOS E ELASTICIDADE
# ============================================================================
print("\n" + "="*80)
print("5. MIX DE PRODUTOS E ELASTICIDADE AO DESCONTO")
print("="*80)

category_kpis = df_confirmed.groupby('Category').agg({
    'Order_ID': 'count',
    'Total': ['sum', 'mean'],
    'Discount': 'mean',
    'Quantity': 'sum'
}).round(2)

category_kpis.columns = ['Num_Pedidos', 'Receita_Total', 'Ticket_Medio', 
                         'Desconto_Medio', 'Qtd_Vendida']
category_kpis['Desconto_Medio'] = (category_kpis['Desconto_Medio'] * 100).round(2)
category_kpis['Participacao_Receita'] = (category_kpis['Receita_Total'] / 
                                          category_kpis['Receita_Total'].sum() * 100).round(2)

category_kpis = category_kpis.sort_values('Receita_Total', ascending=False)

print("\n--- Mix de Produtos por Categoria ---")
print(category_kpis)

# Análise de elasticidade (correlação entre desconto e volume)
print("\n--- Elasticidade ao Desconto por Categoria ---")
for category in df_confirmed['Category'].unique():
    df_cat = df_confirmed[df_confirmed['Category'] == category]
    
    # Agrupar por faixas de desconto
    df_cat['discount_range'] = pd.cut(df_cat['Discount']*100, 
                                       bins=[0, 5, 10, 15, 100], 
                                       labels=['0-5%', '5-10%', '10-15%', '>15%'])
    
    volume_by_discount = df_cat.groupby('discount_range')['Order_ID'].count()
    
    if len(volume_by_discount) > 1:
        print(f"\n{category}:")
        print(volume_by_discount)

# ============================================================================
# 6. SAZONALIDADE E TENDÊNCIAS
# ============================================================================
print("\n" + "="*80)
print("6. SAZONALIDADE E TENDÊNCIAS")
print("="*80)

monthly_kpis = df_confirmed.groupby('order_month').agg({
    'Order_ID': 'count',
    'Total': ['sum', 'mean']
}).round(2)

monthly_kpis.columns = ['Num_Pedidos', 'Receita_Total', 'Ticket_Medio']

# Identificar meses de pico e vale
mes_pico_volume = monthly_kpis['Num_Pedidos'].idxmax()
mes_vale_volume = monthly_kpis['Num_Pedidos'].idxmin()
mes_pico_receita = monthly_kpis['Receita_Total'].idxmax()

meses_nomes = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 
               5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
               9: 'Setembro', 10: 'Outubro'}

print("\n--- Sazonalidade Mensal ---")
print(f"✓ Mês com maior volume: {meses_nomes[mes_pico_volume]} "
      f"({monthly_kpis.loc[mes_pico_volume, 'Num_Pedidos']:.0f} pedidos)")
print(f"✓ Mês com menor volume: {meses_nomes[mes_vale_volume]} "
      f"({monthly_kpis.loc[mes_vale_volume, 'Num_Pedidos']:.0f} pedidos)")
print(f"✓ Mês com maior receita: {meses_nomes[mes_pico_receita]} "
      f"(R$ {monthly_kpis.loc[mes_pico_receita, 'Receita_Total']:,.2f})")

# Variação mensal
variacao_volume = ((monthly_kpis['Num_Pedidos'].max() - 
                    monthly_kpis['Num_Pedidos'].min()) / 
                   monthly_kpis['Num_Pedidos'].mean() * 100)
print(f"\nVariação de volume entre meses: {variacao_volume:.1f}%")

# ============================================================================
# 7. ANÁLISE REGIONAL
# ============================================================================
print("\n" + "="*80)
print("7. ANÁLISE REGIONAL")
print("="*80)

region_kpis = df_confirmed.groupby('Region').agg({
    'Order_ID': 'count',
    'Total': ['sum', 'mean'],
    'P_Service': 'mean',
    'is_late': lambda x: (x.sum() / len(x) * 100)
}).round(2)

region_kpis.columns = ['Num_Pedidos', 'Receita_Total', 'Ticket_Medio', 
                       'Frete_Medio', 'Taxa_Atraso']
region_kpis['Participacao_Receita'] = (region_kpis['Receita_Total'] / 
                                        region_kpis['Receita_Total'].sum() * 100).round(2)

region_kpis = region_kpis.sort_values('Receita_Total', ascending=False)

print("\n--- Performance por Região ---")
print(region_kpis)

# Insights regionais
print("\n--- INSIGHTS REGIONAIS ---")
regiao_maior_receita = region_kpis['Receita_Total'].idxmax()
regiao_maior_frete = region_kpis['Frete_Medio'].idxmax()
regiao_maior_atraso = region_kpis['Taxa_Atraso'].idxmax()

print(f"✓ Maior receita: {regiao_maior_receita} "
      f"({region_kpis.loc[regiao_maior_receita, 'Participacao_Receita']:.1f}% do total)")
print(f"✗ Maior custo de frete: {regiao_maior_frete} "
      f"(R$ {region_kpis.loc[regiao_maior_frete, 'Frete_Medio']:.2f})")
print(f"✗ Maior taxa de atraso: {regiao_maior_atraso} "
      f"({region_kpis.loc[regiao_maior_atraso, 'Taxa_Atraso']:.1f}%)")

# ============================================================================
# 8. DASHBOARD DE KPIs
# ============================================================================
print("\n" + "="*80)
print("8. CRIANDO DASHBOARD DE KPIs")
print("="*80)

# Criar visualização consolidada
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# KPI 1: Receita Total por Mês
ax1 = fig.add_subplot(gs[0, :2])
months = list(range(1, 11))
month_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out']
ax1.bar(months, monthly_kpis['Receita_Total'], color='steelblue', edgecolor='black')
ax1.set_xlabel('Mês')
ax1.set_ylabel('Receita (R$)')
ax1.set_title('Receita Total Mensal', fontweight='bold', fontsize=12)
ax1.set_xticks(months)
ax1.set_xticklabels(month_labels)
ax1.grid(True, alpha=0.3, axis='y')

# KPI 2: Taxa de Confirmação
ax2 = fig.add_subplot(gs[0, 2])
labels_conf = ['Confirmados', 'Cancelados']
sizes_conf = [num_pedidos_confirmados, num_pedidos_cancelados]
colors_conf = ['#2ecc71', '#e74c3c']
ax2.pie(sizes_conf, labels=labels_conf, autopct='%1.1f%%', colors=colors_conf, startangle=90)
ax2.set_title('Taxa de Confirmação', fontweight='bold', fontsize=12)

# KPI 3: Receita por Categoria
ax3 = fig.add_subplot(gs[1, :2])
categories = category_kpis.index
ax3.barh(categories, category_kpis['Receita_Total'], color='green', edgecolor='black')
ax3.set_xlabel('Receita Total (R$)')
ax3.set_title('Receita por Categoria', fontweight='bold', fontsize=12)
ax3.grid(True, alpha=0.3, axis='x')

# KPI 4: Taxa de Atraso por Serviço
ax4 = fig.add_subplot(gs[1, 2])
services = service_kpis.index
ax4.bar(services, service_kpis['Taxa_Atraso'], color='coral', edgecolor='black')
ax4.set_ylabel('Taxa de Atraso (%)')
ax4.set_title('Taxa de Atraso por Serviço', fontweight='bold', fontsize=12)
ax4.grid(True, alpha=0.3, axis='y')

# KPI 5: Ticket Médio por Região
ax5 = fig.add_subplot(gs[2, :2])
regions = region_kpis.index
ax5.barh(regions, region_kpis['Ticket_Medio'], color='purple', edgecolor='black')
ax5.set_xlabel('Ticket Médio (R$)')
ax5.set_title('Ticket Médio por Região', fontweight='bold', fontsize=12)
ax5.grid(True, alpha=0.3, axis='x')

# KPI 6: Conversão por Método de Pagamento
ax6 = fig.add_subplot(gs[2, 2])
payments = payment_kpis.index
ax6.bar(range(len(payments)), payment_kpis['Taxa_Confirmacao'], 
        color='mediumseagreen', edgecolor='black')
ax6.set_xticks(range(len(payments)))
ax6.set_xticklabels(payments, rotation=45, ha='right', fontsize=8)
ax6.set_ylabel('Taxa de Confirmação (%)')
ax6.set_title('Conversão por Pagamento', fontweight='bold', fontsize=12)
ax6.grid(True, alpha=0.3, axis='y')

fig.suptitle('DASHBOARD DE KPIs - E-COMMERCE', fontsize=16, fontweight='bold', y=0.995)
plt.savefig('../figures/13_dashboard_kpis.png', dpi=300, bbox_inches='tight')
print("✓ Dashboard salvo: 13_dashboard_kpis.png")
plt.close()

# ============================================================================
# 9. EXPORTAR RESUMO DE KPIs
# ============================================================================
print("\n" + "="*80)
print("9. EXPORTANDO RESUMO DE KPIs")
print("="*80)

# Criar arquivo de resumo
with open('../reports/kpis_summary.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RESUMO DE KPIs - E-COMMERCE BRASILEIRO\n")
    f.write("="*80 + "\n\n")
    
    f.write("1. KPIs FINANCEIROS\n")
    f.write("-"*80 + "\n")
    f.write(f"Receita Total: R$ {receita_total:,.2f}\n")
    f.write(f"Ticket Médio: R$ {ticket_medio:.2f}\n")
    f.write(f"Frete Médio: R$ {frete_medio:.2f}\n")
    f.write(f"Desconto Médio: {desconto_medio_pct:.2f}%\n")
    f.write(f"Take-rate de Frete: {take_rate_frete:.2f}%\n\n")
    
    f.write("2. KPIs OPERACIONAIS\n")
    f.write("-"*80 + "\n")
    f.write(f"Total de Pedidos: {num_pedidos_total:,}\n")
    f.write(f"Taxa de Confirmação: {taxa_confirmacao:.2f}%\n")
    f.write(f"Taxa de Cancelamento: {taxa_cancelamento:.2f}%\n\n")
    
    f.write("3. KPIs LOGÍSTICOS\n")
    f.write("-"*80 + "\n")
    f.write(f"Prazo Médio de Entrega: {prazo_medio_entrega:.1f} dias\n")
    f.write(f"Atraso Médio: {atraso_medio:.1f} dias\n")
    f.write(f"Taxa de Atraso: {taxa_atraso:.2f}%\n\n")
    
    f.write("4. TOP INSIGHTS\n")
    f.write("-"*80 + "\n")
    f.write(f"✓ Categoria mais lucrativa: {category_kpis.index[0]}\n")
    f.write(f"✓ Melhor método de pagamento: {best_payment}\n")
    f.write(f"✓ Região com maior receita: {regiao_maior_receita}\n")
    f.write(f"✗ Região com maior custo de frete: {regiao_maior_frete}\n")
    f.write(f"✗ Maior taxa de atraso: {regiao_maior_atraso}\n")

print("✓ Resumo de KPIs salvo: kpis_summary.txt")

print("\n" + "="*80)
print("FIM DO NOTEBOOK 6")
print("="*80)