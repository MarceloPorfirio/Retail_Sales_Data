import flet as ft
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns

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

# Função para criar um gráfico de barras
def criar_grafico_barras(dataframe, titulo_grafico):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Loja', y='Vendas_Semanais', data=dataframe, palette='viridis')
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
        exibir_resultados(top_10_maior, "Top 10 Lojas com Maior Vendas")

    def exibir_top_10_menor(e):
        _, top_10_menor = calcular_top_lojas()
        exibir_resultados(top_10_menor, "Top 10 Lojas com Menor Vendas")

    # Função para exibir os resultados em uma tabela e gráfico
    def exibir_resultados(dataframe, titulo_tabela):
        # Limpar a página antes de exibir novos resultados
        page.clean()
        page.add(titulo)

        # Criar uma tabela com os resultados
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

        # Adicionar a tabela à página
        page.add(ft.Text(titulo_tabela, size=18, weight="bold"))
        page.add(tabela)

        # Criar e exibir o gráfico
        grafico_buffer = criar_grafico_barras(dataframe, titulo_tabela)
        page.add(ft.Image(src_base64=grafico_buffer.getvalue().decode('latin1')))

        # Botão para voltar ao menu
        botao_voltar = ft.ElevatedButton("Voltar ao Menu", on_click=voltar_ao_menu)
        page.add(botao_voltar)

    # Função para voltar ao menu principal
    def voltar_ao_menu(e):
        page.clean()
        page.add(titulo)
        page.add(botao_maior_vendas, botao_menor_vendas)

    # Botões do menu principal
    botao_maior_vendas = ft.ElevatedButton("Top 10 Lojas com Maior Vendas", on_click=exibir_top_10_maior)
    botao_menor_vendas = ft.ElevatedButton("Top 10 Lojas com Menor Vendas", on_click=exibir_top_10_menor)

    # Adicionar elementos à página inicial
    page.add(titulo)
    page.add(botao_maior_vendas, botao_menor_vendas)

# Executar o aplicativo Flet
ft.app(target=main)