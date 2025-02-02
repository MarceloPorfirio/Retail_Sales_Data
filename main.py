import pandas as pd

# # Carregar os dados
# sales_data = pd.read_csv('Sales.csv')  # Arquivo principal de vendas
# store_data = pd.read_csv('Stores.csv')  # Informações sobre as lojas
# features_data = pd.read_csv('Features.csv')  # Características das lojas (como promoções)

# # # Visualizar as primeiras linhas de cada DataFrame
# # print(sales_data.head())
# # print(store_data.head())
# # print(features_data.head())

# # # Verificar informações básicas
# # print(sales_data.info())
# # print(store_data.info())
# # print(features_data.info())

# # # Verificar estatísticas descritivas
# # print(sales_data.describe())
# # print(store_data.describe())
# # print(features_data.describe())

# # Juntar os dados de vendas com informações das lojas
# merged_data = pd.merge(sales_data, store_data, on='Store', how='left')

# # Juntar com as características das lojas
# merged_data = pd.merge(merged_data, features_data, on=['Store', 'Date'], how='left')

# # # Verificar o resultado
# # print(merged_data.head())

# # # Verificar dados nulos em cada coluna
# # print(merged_data.isnull().sum())

# # Dicionário de tradução
# traducao_colunas = {
#     'Store': 'Loja',
#     'Dept': 'Departamento',
#     'Date': 'Data',
#     'Weekly_Sales': 'Vendas_Semanais',
#     'IsHoliday': 'Feriado',
#     'Temperature': 'Temperatura',
#     'Fuel_Price': 'Preco_Combustivel',
#     'MarkDown1': 'Promocao1',
#     'MarkDown2': 'Promocao2',
#     'MarkDown3': 'Promocao3',
#     'MarkDown4': 'Promocao4',
#     'MarkDown5': 'Promocao5',
#     'CPI': 'IPC',  # Índice de Preços ao Consumidor
#     'Unemployment': 'Desemprego',
#     'Type': 'Tipo_Loja',
#     'Size': 'Tamanho_Loja'
# }

# # Renomear as colunas
# merged_data.rename(columns=traducao_colunas, inplace=True)

# # Verificar o resultado
# print(merged_data.head())

# Salvar o DataFrame com colunas em português
import pandas as pd

# Carregar o arquivo
df = pd.read_csv('retail_sales_cleaned_pt.csv')

# Verificar as primeiras linhas
print(df.head())

# Verificar informações básicas
print(df.info())

# Verificar dados nulos
print(df.isnull().sum())

# Preencher valores nulos em colunas numéricas
df['Temperatura'] = df['Temperatura'].fillna(df['Temperatura'].mean())
df['Preco_Combustivel'] = df['Preco_Combustivel'].fillna(df['Preco_Combustivel'].mean())
df['Promocao1'] = df['Promocao1'].fillna(0)
df['Promocao2'] = df['Promocao2'].fillna(0)
df['Promocao3'] = df['Promocao3'].fillna(0)
df['Promocao4'] = df['Promocao4'].fillna(0)
df['Promocao5'] = df['Promocao5'].fillna(0)

# Remover linhas com valores nulos em colunas críticas
df = df.dropna(subset=['Vendas_Semanais', 'Data'])

# Preencher valores nulos em colunas categóricas
moda_tipo_loja = df['Tipo_Loja'].mode()[0]
df['Tipo_Loja'] = df['Tipo_Loja'].fillna(moda_tipo_loja)

# Remover linhas onde 'Vendas_Semanais' ou 'Data' são nulos
df.dropna(subset=['Vendas_Semanais', 'Data'], inplace=True)

# Preencher valores nulos em 'Tipo_Loja' com a moda
moda_tipo_loja = df['Tipo_Loja'].mode()[0]
df['Tipo_Loja'].fillna(moda_tipo_loja, inplace=True)