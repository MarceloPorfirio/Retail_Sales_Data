import flet as ft
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Configura o Matplotlib para não usar uma GUI
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64  # Adicionado para codificar o buffer em base64

# Carregar os dados
df = pd.read_csv('retail_sales_cleaned_final.csv')

# Função para calcular as top 10 lojas com maior e menor vendas
def calcular_top_lojas():
    # Calcular vendas totais por loja
    vendas_por_loja = df.groupby('Loja')['Vendas_Semanais'].sum().reset_index()
    
    # Ordenar por vendas (maior para menor)
    top_10_maior = vendas_por_loja.sort_values(by='Vendas_Semanais', ascending=False).head(10)
    top_10_menor = vendas_por_loja.sort_values(by='Vendas_Semanais', ascending=True).head(10)
    
    return top_10_maior, top_10_menor

# Função para calcular vendas por data
def calcular_vendas_por_data():
    # Converter a coluna 'Data' para o tipo datetime com o formato correto
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    
    # Agrupar vendas por data
    vendas_por_data = df.groupby('Data')['Vendas_Semanais'].sum().reset_index()
    return vendas_por_data

# Função para criar um gráfico de barras
def criar_grafico_barras(dataframe, titulo_grafico):
    plt.figure(figsize=(8, 5))  # Tamanho menor para caber ao lado da tabela
    sns.barplot(x='Loja', y='Vendas_Semanais', data=dataframe, color='blue')  # Cor fixa
    plt.title(titulo_grafico)
    plt.xlabel('Loja')
    plt.ylabel('Vendas Semanais')
    plt.xticks(rotation=45)
    
    # Salvar o gráfico em um buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf

# Função para criar um gráfico de linha
def criar_grafico_linha(dataframe, titulo_grafico):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Data', y='Vendas_Semanais', data=dataframe, color='blue')
    plt.title(titulo_grafico)
    plt.xlabel('Data')
    plt.ylabel('Vendas Semanais')
    plt.xticks(rotation=45)
    
    # Salvar o gráfico em um buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf

# Função principal do Flet
def main(page: ft.Page):
    page.title = "Análise de Vendas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Título da página
    titulo = ft.Text("Análise de Vendas - Top 10 Lojas", size=24, weight="bold")

    # Botões para exibir as análises
    def exibir_top_10_maior(e):
        top_10_maior, _ = calcular_top_lojas()
        exibir_resultados(top_10_maior, "Top 10 Lojas com Maior Vendas", tipo_grafico='barras')

    def exibir_top_10_menor(e):
        _, top_10_menor = calcular_top_lojas()
        exibir_resultados(top_10_menor, "Top 10 Lojas com Menor Vendas", tipo_grafico='barras')

    def exibir_vendas_tempo(e):
        vendas_por_data = calcular_vendas_por_data()
        exibir_resultados(vendas_por_data, "Vendas ao Longo do Tempo", tipo_grafico='linha')

    # Função para exibir os resultados em uma tabela e gráfico
    def exibir_resultados(dataframe, titulo_tabela, tipo_grafico='barras'):
        # Limpar a página antes de exibir novos resultados
        page.clean()
        page.add(titulo)

        # Criar uma tabela com os resultados (se aplicável)
        if tipo_grafico == 'barras':
            tabela = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Loja")),
                    ft.DataColumn(ft.Text("Vendas Semanais")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row['Loja']))),
                            ft.DataCell(ft.Text(f"R$ {row['Vendas_Semanais']:,.2f}")),
                        ]
                    ) for index, row in dataframe.iterrows()
                ],
            )
        else:
            tabela = None

        # Criar o gráfico
        if tipo_grafico == 'barras':
            grafico_buffer = criar_grafico_barras(dataframe, titulo_tabela)
        elif tipo_grafico == 'linha':
            grafico_buffer = criar_grafico_linha(dataframe, titulo_tabela)

        print("Gráfico gerado com sucesso! Tamanho do buffer:", len(grafico_buffer.getvalue()))  # Verificação

        # Codificar o buffer em base64
        grafico_base64 = base64.b64encode(grafico_buffer.getvalue()).decode('utf-8')

        # Exibir o gráfico
        imagem_grafico = ft.Image(src_base64=grafico_base64, width=600, height=400)  # Tamanho ajustado

        # Organizar tabela e gráfico em uma linha (se aplicável)
        if tabela:
            linha_resultados = ft.Row(
                controls=[
                    ft.Container(tabela, width=400),  # Largura fixa para a tabela
                    imagem_grafico,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,  # Espaçamento entre a tabela e o gráfico
            )
        else:
            linha_resultados = ft.Row(
                controls=[imagem_grafico],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        # Adicionar a linha à página
        page.add(linha_resultados)

        # Botão para voltar ao menu
        botao_voltar = ft.ElevatedButton("Voltar ao Menu", on_click=voltar_ao_menu)
        page.add(botao_voltar)

    # Função para voltar ao menu principal
    def voltar_ao_menu(e):
        page.clean()
        page.add(titulo)
        page.add(botao_maior_vendas, botao_menor_vendas, botao_vendas_tempo)

    # Botões do menu principal
    botao_maior_vendas = ft.ElevatedButton("Top 10 Lojas com Maior Vendas", on_click=exibir_top_10_maior)
    botao_menor_vendas = ft.ElevatedButton("Top 10 Lojas com Menor Vendas", on_click=exibir_top_10_menor)
    botao_vendas_tempo = ft.ElevatedButton("Vendas ao Longo do Tempo", on_click=exibir_vendas_tempo)

    # Adicionar elementos à página inicial
    page.add(titulo)
    page.add(botao_maior_vendas, botao_menor_vendas, botao_vendas_tempo)

# Executar o aplicativo Flet
ft.app(target=main)