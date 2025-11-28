-- Arquivo SQL para atender ao requisito de reprodutibilidade.
-- O projeto utiliza Python/Pandas para o processamento de dados,
-- mas este arquivo demonstra a estrutura lógica das tabelas.

-- Tabela de Fatos (Pedidos)
CREATE TABLE FACT_Orders (
    Order_ID VARCHAR(50) PRIMARY KEY,
    Customer_ID VARCHAR(50),
    Product_ID VARCHAR(50),
    Delivery_ID VARCHAR(50),
    Shopping_ID VARCHAR(50),
    Order_Date DATE,
    D_Forecast DATE,
    D_Date DATE,
    Purchase_Status VARCHAR(50),
    Quantity INT,
    Subtotal DECIMAL(10, 2),
    Discount DECIMAL(10, 2),
    P_Service DECIMAL(10, 2),
    Total DECIMAL(10, 2)
);

-- Tabela de Dimensão (Clientes)
CREATE TABLE DIM_Customer (
    Customer_ID VARCHAR(50) PRIMARY KEY,
    UF VARCHAR(2),
    Region VARCHAR(50)
);

-- Tabela de Dimensão (Produtos)
CREATE TABLE DIM_Products (
    Product_ID VARCHAR(50) PRIMARY KEY,
    Category VARCHAR(50),
    Subcategory VARCHAR(50)
);

-- Tabela de Dimensão (Entrega)
CREATE TABLE DIM_Delivery (
    Delivery_ID VARCHAR(50) PRIMARY KEY,
    Services VARCHAR(50)
);

-- Tabela de Dimensão (Compra/Pagamento)
CREATE TABLE DIM_Shopping (
    Shopping_ID VARCHAR(50) PRIMARY KEY,
    Payment_Method VARCHAR(50)
);

-- Nota: O processamento e análise de dados são realizados integralmente em Python (Pandas/Scipy).
