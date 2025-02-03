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


df.rename(columns={'IsHoliday_x': 'Feriado'}, inplace=True)

def calcular_impacto_feriados():
    # Calcular a média de vendas em semanas com e sem feriado
    impacto_feriados = df.groupby('Feriado')['Vendas_Semanais'].mean().reset_index()
    return impacto_feriados

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

def criar_grafico_barras_feriados(dataframe, titulo_grafico):
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Feriado', y='Vendas_Semanais', data=dataframe, color='blue')
    plt.title(titulo_grafico)
    plt.xlabel('Feriado')
    plt.ylabel('Média de Vendas Semanais')
    plt.xticks(ticks=[0, 1], labels=['Sem Feriado', 'Com Feriado'])
    
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
    titulo = ft.Text("Análise de Vendas", size=24, weight="bold")

    def exibir_resultados(dataframe, titulo_tabela, tipo_grafico='barras'):
        # Limpar a área principal antes de exibir novos resultados
        area_principal.controls.clear()

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
        elif tipo_grafico == 'barras_feriados':
            tabela = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Feriado")),
                    ft.DataColumn(ft.Text("Média de Vendas Semanais")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text("Sem Feriado" if row['Feriado'] == 0 else "Com Feriado")),
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
        elif tipo_grafico == 'barras_feriados':
            grafico_buffer = criar_grafico_barras_feriados(dataframe, titulo_tabela)

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

        # Adicionar a linha à área principal
        area_principal.controls.append(linha_resultados)
        page.update()

    def exibir_menu_principal():
       area_principal.controls.clear()
       area_principal.controls.append(
           ft.Column(
               [
                   ft.Text("Bem-vindo ao Sistema de Análise de Vendas", size=20, weight="bold"),
                    ft.Text("Selecione uma opção no menu lateral para começar.", size=16),
                    ft.Image(src="https://via.placeholder.com/600x300.png?text=Imagem+de+Exemplo", width=600, height=300),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
               
           )
       )
       page.update()

    # Função para exibir as top 10 lojas com maior vendas
    def exibir_top_10_maior(e):
        top_10_maior, _ = calcular_top_lojas()
        exibir_resultados(top_10_maior, "Top 10 Lojas com Maior Vendas", tipo_grafico='barras')

    # Função para exibir as top 10 lojas com menor vendas
    def exibir_top_10_menor(e):
        _, top_10_menor = calcular_top_lojas()
        exibir_resultados(top_10_menor, "Top 10 Lojas com Menor Vendas", tipo_grafico='barras')

    # Função para exibir as vendas ao longo do tempo
    def exibir_vendas_tempo(e):
        vendas_por_data = calcular_vendas_por_data()
        exibir_resultados(vendas_por_data, "Vendas ao Longo do Tempo", tipo_grafico='linha')

    # Função para exibir o impacto de feriados
    def exibir_impacto_feriados(e):
        impacto_feriados = calcular_impacto_feriados()
        exibir_resultados(impacto_feriados, "Impacto de Feriados nas Vendas", tipo_grafico='barras_feriados')

    # Menu lateral
    menu_lateral = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME,
                selected_icon=ft.icons.HOME_FILLED,
                label="Inicio",
            ),
            
            ft.NavigationRailDestination(
                icon=ft.icons.TRENDING_UP,
                selected_icon=ft.icons.TRENDING_UP_OUTLINED,
                label="Top 10 Maiores Vendas",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.TRENDING_DOWN,
                selected_icon=ft.icons.TRENDING_DOWN_OUTLINED,
                label="Top 10 Menores Vendas",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.TIMELINE,
                selected_icon=ft.icons.TIMELINE_OUTLINED,
                label="Vendas ao Longo do Tempo",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.HOLIDAY_VILLAGE,
                selected_icon=ft.icons.HOLIDAY_VILLAGE_OUTLINED,
                label="Impacto de Feriados",
        ),
        ],
        on_change=lambda e: atualizar_tela(e.control.selected_index),
    )

    # Área principal
    area_principal = ft.Column(alignment=ft.MainAxisAlignment.CENTER, expand=True)

    # Função para atualizar a tela com base na seleção do menu
    def atualizar_tela(index):
        if index == 0:
            exibir_menu_principal()
        elif index == 1:
            exibir_top_10_maior(None)
        elif index == 2:
            exibir_top_10_menor(None)
        elif index == 3:
            exibir_vendas_tempo(None)
        elif index == 4:
            exibir_impacto_feriados(None)

    # Layout da página
    page.add(
        ft.Row(
            [
                menu_lateral,
                ft.VerticalDivider(width=1),
                area_principal,
            ],
            expand=True,
        )
    )

    # Exibir a primeira análise ao carregar a página
    atualizar_tela(0)

# Executar o aplicativo Flet
ft.app(target=main)