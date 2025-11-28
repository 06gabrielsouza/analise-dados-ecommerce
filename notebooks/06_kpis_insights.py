import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (14, 6)

print("="*80)
print("NOTEBOOK 6: KPIS E INSIGHTS DE NEGÓCIO")
print("="*80)

df = pd.read_csv('../data/ecommerce_clean.csv')
for col in ['Order_Date', 'D_Forecast', 'D_Date']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Cálculos Básicos
receita = df['Total'].sum()
pedidos = len(df)
ticket = df['Total'].mean()
confirmados = df[df['is_confirmed'] == 1]
taxa_conf = (len(confirmados) / pedidos) * 100

print(f"\n💰 Faturamento: R$ {receita:,.2f}")
print(f"📦 Pedidos: {pedidos}")
print(f"✅ Taxa Confirmação: {taxa_conf:.1f}%")

# DASHBOARD FINAL (CORREÇÃO AQUI: Eixos dinâmicos)
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(2, 3)

# 1. Vendas por Mês
ax1 = fig.add_subplot(gs[0, 0])
vendas_mes = df.groupby('order_month')['Total'].sum()
ax1.bar(vendas_mes.index, vendas_mes.values, color='royalblue')
ax1.set_title('Faturamento Mensal')
ax1.set_xlabel('Mês')
ax1.set_xticks(vendas_mes.index) # Garante que só mostra meses existentes

# 2. Confirmação
ax2 = fig.add_subplot(gs[0, 1])
status_counts = df['Purchase_Status'].value_counts()
ax2.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
ax2.set_title('Status dos Pedidos')

# 3. Atrasos por Serviço
ax3 = fig.add_subplot(gs[0, 2])
atraso_serv = df.groupby('Services')['is_late'].mean() * 100
ax3.bar(atraso_serv.index, atraso_serv.values, color='tomato')
ax3.set_title('Taxa de Atraso (%)')

# 4. Top Regiões
ax4 = fig.add_subplot(gs[1, :2]) # Ocupa 2 colunas
top_regioes = df.groupby('Region')['Total'].sum().sort_values(ascending=False)
ax4.barh(top_regioes.index, top_regioes.values, color='purple')
ax4.set_title('Ranking de Receita por Região')

# 5. Pagamentos
ax5 = fig.add_subplot(gs[1, 2])
pagamentos = df['Payment_Method'].value_counts()
ax5.bar(pagamentos.index, pagamentos.values, color='green')
ax5.set_title('Pedidos por Meio de Pagamento')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('../figures/13_dashboard_kpis.png')
print("\n✓ Dashboard Final salvo com sucesso: 13_dashboard_kpis.png")

# Salvar Resumo TXT
with open('../reports/kpis_summary.txt', 'w') as f:
    f.write(f"Receita: {receita}\nPedidos: {pedidos}\nTaxa Conf: {taxa_conf:.1f}%")
print("✓ Resumo TXT salvo.")
