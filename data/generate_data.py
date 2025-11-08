"""
Script para gerar dados sintéticos realistas de e-commerce brasileiro
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurar seed para reprodutibilidade
np.random.seed(42)
random.seed(42)

# Parâmetros
N_ORDERS = 5000

# Listas de valores brasileiros
ESTADOS = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'CE', 'DF', 'GO', 'ES', 'PA', 'AM', 'MA']
REGIOES = {
    'SP': 'Sudeste', 'RJ': 'Sudeste', 'MG': 'Sudeste', 'ES': 'Sudeste',
    'RS': 'Sul', 'PR': 'Sul', 'SC': 'Sul',
    'BA': 'Nordeste', 'PE': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste',
    'PA': 'Norte', 'AM': 'Norte'
}

CATEGORIAS = {
    'Eletrônicos': ['Smartphones', 'Notebooks', 'Tablets', 'Fones de Ouvido', 'Smartwatches'],
    'Moda': ['Camisetas', 'Calças', 'Vestidos', 'Calçados', 'Acessórios'],
    'Casa e Decoração': ['Móveis', 'Utensílios', 'Decoração', 'Iluminação', 'Têxtil'],
    'Livros': ['Ficção', 'Não-ficção', 'Técnicos', 'Infantis', 'HQs'],
    'Esportes': ['Roupas Esportivas', 'Equipamentos', 'Suplementos', 'Acessórios', 'Calçados']
}

PAYMENT_METHODS = ['Cartão de Crédito', 'Boleto', 'PIX', 'Cartão de Débito']
SERVICES = ['Standard', 'Same-Day', 'Scheduled']
STATUS = ['Confirmado', 'Cancelado']

# Gerar dados
data = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 10, 31)

for i in range(N_ORDERS):
    # Data do pedido
    order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    # Localização
    uf = random.choice(ESTADOS)
    region = REGIOES[uf]
    
    # Categoria e subcategoria
    category = random.choice(list(CATEGORIAS.keys()))
    subcategory = random.choice(CATEGORIAS[category])
    
    # Valores base (dependem da categoria)
    if category == 'Eletrônicos':
        base_price = np.random.uniform(500, 5000)
    elif category == 'Moda':
        base_price = np.random.uniform(50, 500)
    elif category == 'Casa e Decoração':
        base_price = np.random.uniform(100, 2000)
    elif category == 'Livros':
        base_price = np.random.uniform(20, 150)
    else:  # Esportes
        base_price = np.random.uniform(80, 800)
    
    # Quantidade
    quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])
    
    # Subtotal
    subtotal = base_price * quantity
    
    # Desconto (%)
    discount_pct = np.random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20], 
                                     p=[0.4, 0.2, 0.1, 0.15, 0.10, 0.03, 0.02])
    
    # Serviço de entrega
    service = np.random.choice(SERVICES, p=[0.7, 0.15, 0.15])
    
    # Frete (depende do serviço e região)
    if service == 'Standard':
        freight_base = np.random.uniform(10, 40)
    elif service == 'Same-Day':
        freight_base = np.random.uniform(30, 80)
    else:  # Scheduled
        freight_base = np.random.uniform(15, 50)
    
    # Ajuste regional
    if region in ['Norte', 'Nordeste']:
        freight_base *= 1.3
    elif region == 'Centro-Oeste':
        freight_base *= 1.1
    
    p_service = round(freight_base, 2)
    
    # Total
    total = round(subtotal * (1 - discount_pct) + p_service, 2)
    
    # Método de pagamento
    payment = np.random.choice(PAYMENT_METHODS, p=[0.5, 0.15, 0.25, 0.10])
    
    # Status (PIX e Cartão têm mais confirmação)
    if payment in ['PIX', 'Cartão de Crédito']:
        status = np.random.choice(STATUS, p=[0.92, 0.08])
    else:
        status = np.random.choice(STATUS, p=[0.80, 0.20])
    
    # Prazo previsto (depende do serviço)
    if service == 'Standard':
        forecast_days = np.random.randint(5, 15)
    elif service == 'Same-Day':
        forecast_days = 0
    else:  # Scheduled
        forecast_days = np.random.randint(3, 10)
    
    d_forecast = order_date + timedelta(days=forecast_days)
    
    # Data de entrega real (com possibilidade de atraso)
    if status == 'Confirmado':
        # 70% no prazo, 20% com atraso leve, 10% com atraso grave
        delay_type = np.random.choice(['on_time', 'light_delay', 'heavy_delay'], 
                                       p=[0.70, 0.20, 0.10])
        if delay_type == 'on_time':
            actual_days = max(0, forecast_days + np.random.randint(-2, 2))
        elif delay_type == 'light_delay':
            actual_days = forecast_days + np.random.randint(1, 5)
        else:
            actual_days = forecast_days + np.random.randint(5, 15)
        
        d_date = order_date + timedelta(days=actual_days)
    else:
        d_date = None
    
    # Criar registro
    record = {
        'Order_ID': f'ORD{i+1:06d}',
        'Order_Date': order_date.strftime('%Y-%m-%d'),
        'UF': uf,
        'Region': region,
        'Category': category,
        'Subcategory': subcategory,
        'Quantity': quantity,
        'Subtotal': round(subtotal, 2),
        'Discount': discount_pct,
        'P_Service': p_service,
        'Total': total,
        'Payment_Method': payment,
        'Purchase_Status': status,
        'Services': service,
        'D_Forecast': d_forecast.strftime('%Y-%m-%d'),
        'D_Date': d_date.strftime('%Y-%m-%d') if d_date else None
    }
    
    data.append(record)

# Criar DataFrame
df = pd.DataFrame(data)

# Adicionar alguns registros duplicados (para testar limpeza)
duplicates = df.sample(n=50, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Adicionar alguns valores faltantes aleatórios
missing_indices = np.random.choice(df.index, size=30, replace=False)
df.loc[missing_indices[:10], 'D_Date'] = None
df.loc[missing_indices[10:20], 'Discount'] = None
df.loc[missing_indices[20:30], 'P_Service'] = None

# Adicionar alguns outliers
outlier_indices = np.random.choice(df.index, size=10, replace=False)
df.loc[outlier_indices[:5], 'Total'] = df.loc[outlier_indices[:5], 'Total'] * 10
df.loc[outlier_indices[5:], 'P_Service'] = df.loc[outlier_indices[5:], 'P_Service'] * 5

# Salvar
df.to_csv('/home/ubuntu/ecommerce-analytics/data/ecommerce_raw.csv', index=False)
print(f"✓ Dados gerados: {len(df)} registros")
print(f"✓ Período: {df['Order_Date'].min()} a {df['Order_Date'].max()}")
print(f"✓ Arquivo salvo: ecommerce_raw.csv")
