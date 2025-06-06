# -*- coding: utf-8 -*-
"""
🗺️ VISUALIZADOR DE GRAFO - SISTEMA VERMELINHO
BuSync - Visualização da rede de transporte com Matplotlib

Salve como: visualizador_grafo.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import networkx as nx
import numpy as np
from typing import List, Dict, Optional, Tuple
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VisualizadorGrafo:
    """Classe para visualizar o grafo do sistema de transporte"""
    
    def __init__(self, sistema_vermelinho):
        """
        Inicializa o visualizador
        
        Args:
            sistema_vermelinho: Instância do SistemaVermelhinho
        """
        self.sistema = sistema_vermelinho
        self.grafo = sistema_vermelinho.grafo
        self.pontos = sistema_vermelinho.pontos
        self.fig = None
        self.ax = None
        self.pos = None
        self.calcular_posicoes()
        
    def calcular_posicoes(self):
        """Calcula as posições dos nós baseadas nas coordenadas geográficas"""
        self.pos = {}
        
        # Obter coordenadas min/max para normalização
        lats = [p.latitude for p in self.pontos.values()]
        lons = [p.longitude for p in self.pontos.values()]
        
        lat_min, lat_max = min(lats), max(lats)
        lon_min, lon_max = min(lons), max(lons)
        
        # Normalizar coordenadas para o plano 2D
        for ponto_id, ponto in self.pontos.items():
            # Inverter latitude para que norte fique em cima
            x = (ponto.longitude - lon_min) / (lon_max - lon_min) * 10
            y = (lat_max - ponto.latitude) / (lat_max - lat_min) * 8
            self.pos[ponto_id] = (x, y)
    
    def criar_visualizacao(self, rota_destacada: Optional[List[str]] = None, 
                          tamanho_figura: Tuple[int, int] = (16, 12)):
        """
        Cria a visualização do grafo
        
        Args:
            rota_destacada: Lista de IDs dos pontos da rota a destacar
            tamanho_figura: Tupla (largura, altura) da figura
        """
        # Criar figura
        self.fig, self.ax = plt.subplots(figsize=tamanho_figura)
        self.fig.patch.set_facecolor('#f0f0f0')
        self.ax.set_facecolor('white')
        
        # Título
        self.ax.set_title('🚌 REDE DE TRANSPORTE PÚBLICO - MARICÁ/RJ\nSistema Vermelinho - BuSync', 
                         fontsize=20, fontweight='bold', pad=20)
        
        # Desenhar componentes
        self._desenhar_areas_geograficas()
        self._desenhar_arestas(rota_destacada)
        self._desenhar_nos(rota_destacada)
        self._adicionar_legenda()
        self._adicionar_estatisticas()
        
        # Ajustes finais
        self.ax.set_xlim(-0.5, 10.5)
        self.ax.set_ylim(-0.5, 8.5)
        self.ax.axis('off')
        
        plt.tight_layout()
        
    def _desenhar_areas_geograficas(self):
        """Desenha áreas geográficas de fundo"""
        # Área do mar (direita - leste)
        mar = FancyBboxPatch((9, -0.5), 2, 9, 
                             boxstyle="round,pad=0.1",
                             facecolor='#87CEEB', alpha=0.3,
                             edgecolor='none')
        self.ax.add_patch(mar)
        self.ax.text(10, 8, '🌊 OCEANO\nATLÂNTICO', 
                    ha='center', va='top', fontsize=10,
                    style='italic', alpha=0.6)
        
        # Áreas dos bairros principais
        areas = [
            # (x, y, largura, altura, cor, nome)
            (0, 6, 3, 2, '#90EE90', 'ZONA NORTE'),
            (0, 3, 3, 3, '#FFE4B5', 'CENTRO'),
            (0, 0, 3, 3, '#FFB6C1', 'ZONA SUL'),
            (3, 4, 3, 4, '#E6E6FA', 'ZONA OESTE'),
            (6, 2, 3, 6, '#F0E68C', 'ZONA LESTE'),
        ]
        
        for x, y, w, h, cor, nome in areas:
            area = FancyBboxPatch((x, y), w, h,
                                 boxstyle="round,pad=0.1",
                                 facecolor=cor, alpha=0.2,
                                 edgecolor='gray', linestyle='--')
            self.ax.add_patch(area)
            self.ax.text(x + w/2, y + h - 0.2, nome,
                        ha='center', va='top', fontsize=9,
                        style='italic', alpha=0.7)
    
    def _desenhar_arestas(self, rota_destacada: Optional[List[str]] = None):
        """Desenha as arestas (conexões) do grafo"""
        # Preparar arestas da rota se houver
        arestas_rota = set()
        if rota_destacada:
            for i in range(len(rota_destacada) - 1):
                arestas_rota.add((rota_destacada[i], rota_destacada[i + 1]))
                arestas_rota.add((rota_destacada[i + 1], rota_destacada[i]))
        
        # Desenhar todas as arestas
        for (u, v, data) in self.grafo.edges(data=True):
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            
            # Verificar se é aresta da rota
            if (u, v) in arestas_rota:
                cor = '#FF0000'
                largura = 4
                alpha = 1.0
                zorder = 10
                # Adicionar seta para indicar direção
                self.ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                               arrowprops=dict(arrowstyle='->', lw=largura,
                                             color=cor, alpha=alpha),
                               zorder=zorder)
            else:
                cor = '#666666'
                largura = 1
                alpha = 0.5
                zorder = 1
                self.ax.plot([x1, x2], [y1, y2], 
                           color=cor, linewidth=largura, 
                           alpha=alpha, zorder=zorder)
            
            # Adicionar tempo de viagem no meio da aresta (apenas para rotas)
            if (u, v) in arestas_rota and 'weight' in data:
                xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
                self.ax.text(xm, ym, f"{data['weight']}'", 
                           ha='center', va='center',
                           bbox=dict(boxstyle="round,pad=0.3", 
                                   facecolor='yellow', alpha=0.8),
                           fontsize=8, zorder=15)
    
    def _desenhar_nos(self, rota_destacada: Optional[List[str]] = None):
        """Desenha os nós (pontos de parada) do grafo"""
        # Preparar nós da rota
        nos_rota = set(rota_destacada) if rota_destacada else set()
        
        for ponto_id, (x, y) in self.pos.items():
            ponto = self.pontos[ponto_id]
            
            # Definir aparência baseada no tipo e se está na rota
            if ponto_id in nos_rota:
                if rota_destacada and ponto_id == rota_destacada[0]:
                    cor = '#00FF00'  # Verde para origem
                    tamanho = 1000
                    marcador = 'o'
                    borda = 'darkgreen'
                elif rota_destacada and ponto_id == rota_destacada[-1]:
                    cor = '#FF0000'  # Vermelho para destino
                    tamanho = 1000
                    marcador = 's'
                    borda = 'darkred'
                else:
                    cor = '#FFA500'  # Laranja para intermediários
                    tamanho = 600
                    marcador = 'o'
                    borda = 'darkorange'
                zorder = 20
            else:
                # Cor baseada no tipo
                if ponto.tipo == "terminal":
                    cor = '#4169E1'
                    tamanho = 500
                    marcador = '^'
                else:
                    cor = '#87CEEB'
                    tamanho = 200
                    marcador = 'o'
                borda = 'black'
                zorder = 5
            
            # Desenhar nó
            self.ax.scatter(x, y, c=cor, s=tamanho, marker=marcador,
                          edgecolors=borda, linewidths=2, zorder=zorder)
            
            # Adicionar ícone para terminais
            if ponto.tipo == "terminal":
                self.ax.text(x, y, '🚌', ha='center', va='center',
                           fontsize=12, zorder=zorder + 1)
            
            # Label do ponto (simplificado)
            nome_curto = ponto.nome.split('(')[0].strip()
            if len(nome_curto) > 15:
                nome_curto = nome_curto[:12] + '...'
            
            # Mostrar nome apenas para pontos importantes ou na rota
            if ponto.tipo == "terminal" or ponto_id in nos_rota:
                self.ax.text(x, y - 0.3, nome_curto,
                           ha='center', va='top', fontsize=8,
                           bbox=dict(boxstyle="round,pad=0.2",
                                   facecolor='white', alpha=0.8),
                           zorder=zorder + 1)
    
    def _adicionar_legenda(self):
        """Adiciona legenda ao gráfico"""
        elementos_legenda = [
            plt.Line2D([0], [0], marker='o', color='w', label='Origem',
                      markerfacecolor='#00FF00', markersize=15, markeredgecolor='darkgreen'),
            plt.Line2D([0], [0], marker='s', color='w', label='Destino',
                      markerfacecolor='#FF0000', markersize=15, markeredgecolor='darkred'),
            plt.Line2D([0], [0], marker='o', color='w', label='Parada Intermediária',
                      markerfacecolor='#FFA500', markersize=12, markeredgecolor='darkorange'),
            plt.Line2D([0], [0], marker='^', color='w', label='Terminal',
                      markerfacecolor='#4169E1', markersize=12, markeredgecolor='black'),
            plt.Line2D([0], [0], marker='o', color='w', label='Ponto de Ônibus',
                      markerfacecolor='#87CEEB', markersize=10, markeredgecolor='black'),
            plt.Line2D([0], [0], color='#FF0000', linewidth=4, label='Rota Calculada'),
            plt.Line2D([0], [0], color='#666666', linewidth=1, label='Conexão Disponível', alpha=0.5),
        ]
        
        self.ax.legend(handles=elementos_legenda, loc='upper left',
                      bbox_to_anchor=(0.02, 0.98), frameon=True,
                      fancybox=True, shadow=True)
    
    def _adicionar_estatisticas(self):
        """Adiciona caixa de estatísticas ao gráfico"""
        stats = self.sistema.obter_estatisticas()
        
        texto_stats = f"""📊 ESTATÍSTICAS DO SISTEMA
━━━━━━━━━━━━━━━━━━━━━━
Pontos de Parada: {stats['total_pontos']}
Conexões: {stats['total_conexoes']}
Linhas Ativas: {stats['total_linhas']}
Acessibilidade: {stats['percentual_acessivel']:.1f}%
Densidade: {stats['densidade_grafo']:.3f}
Conectividade: {'✅ Total' if stats['conectividade'] else '❌ Parcial'}"""
        
        # Caixa de estatísticas
        props = dict(boxstyle='round,pad=0.5', facecolor='lightblue', 
                    alpha=0.9, edgecolor='darkblue', linewidth=2)
        self.ax.text(0.98, 0.02, texto_stats, transform=self.ax.transAxes,
                    fontsize=10, verticalalignment='bottom',
                    horizontalalignment='right', bbox=props,
                    family='monospace')
    
    def visualizar_rota(self, origem: str, destino: str, 
                       apenas_acessivel: bool = False) -> Optional[plt.Figure]:
        """
        Visualiza uma rota específica no grafo
        
        Args:
            origem: ID do ponto de origem
            destino: ID do ponto de destino
            apenas_acessivel: Se True, calcula rota apenas acessível
            
        Returns:
            Figure do matplotlib ou None se houver erro
        """
        # Calcular rota
        resultado = self.sistema.calcular_rota(origem, destino, apenas_acessivel)
        
        if not resultado['encontrada']:
            print(f"❌ Erro ao calcular rota: {resultado.get('erro', 'Desconhecido')}")
            return None
        
        # Criar visualização com rota destacada
        self.criar_visualizacao(rota_destacada=resultado['pontos'])
        
        # Adicionar informações da rota
        info_rota = f"""🚌 ROTA CALCULADA
━━━━━━━━━━━━━━━━
Origem: {resultado['origem']}
Destino: {resultado['destino']}
Tempo Total: {resultado['tempo_total']:.1f} min
Distância: {resultado['distancia_estimada']:.1f} km
Paradas: {resultado['numero_paradas']}
Linhas: {', '.join(resultado['linhas_utilizadas'])}"""
        
        props = dict(boxstyle='round,pad=0.5', facecolor='lightgreen',
                    alpha=0.9, edgecolor='darkgreen', linewidth=2)
        self.ax.text(0.02, 0.02, info_rota, transform=self.ax.transAxes,
                    fontsize=10, verticalalignment='bottom',
                    horizontalalignment='left', bbox=props,
                    family='monospace')
        
        return self.fig
    
    def salvar_visualizacao(self, nome_arquivo: str = "grafo_vermelinho.png", 
                           dpi: int = 300):
        """
        Salva a visualização em arquivo
        
        Args:
            nome_arquivo: Nome do arquivo para salvar
            dpi: Resolução da imagem
        """
        if self.fig:
            self.fig.savefig(nome_arquivo, dpi=dpi, bbox_inches='tight',
                           facecolor=self.fig.get_facecolor())
            print(f"✅ Visualização salva em: {nome_arquivo}")
        else:
            print("❌ Nenhuma visualização criada ainda")
    
    def integrar_com_tkinter(self, parent_frame: tk.Frame) -> FigureCanvasTkAgg:
        """
        Integra a visualização com uma janela Tkinter
        
        Args:
            parent_frame: Frame do Tkinter onde inserir o gráfico
            
        Returns:
            Canvas do matplotlib para Tkinter
        """
        if not self.fig:
            self.criar_visualizacao()
        
        canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return canvas

# Funções auxiliares para análise de complexidade
def analisar_complexidade_dijkstra(tamanhos: List[int]) -> Dict[str, List[float]]:
    """
    Analisa a complexidade do algoritmo de Dijkstra
    
    Args:
        tamanhos: Lista com diferentes tamanhos de grafo para testar
        
    Returns:
        Dicionário com tempos de execução
    """
    import time
    import random
    
    resultados = {
        'vertices': tamanhos,
        'tempos': [],
        'teorico': []
    }
    
    for n in tamanhos:
        # Criar grafo aleatório
        G = nx.erdos_renyi_graph(n, 0.3)
        
        # Adicionar pesos
        for (u, v) in G.edges():
            G[u][v]['weight'] = random.uniform(1, 10)
        
        # Medir tempo
        inicio = time.time()
        
        # Executar Dijkstra 10 vezes para média
        for _ in range(10):
            if len(G) > 1:
                origem = random.choice(list(G.nodes()))
                destino = random.choice(list(G.nodes()))
                try:
                    nx.shortest_path(G, origem, destino, weight='weight')
                except:
                    pass
        
        tempo = (time.time() - inicio) / 10
        resultados['tempos'].append(tempo)
        
        # Complexidade teórica O((V + E) log V)
        E = G.number_of_edges()
        V = G.number_of_nodes()
        teorico = (V + E) * np.log2(V) / 1000000  # Normalizar
        resultados['teorico'].append(teorico)
    
    return resultados

def criar_grafico_complexidade():
    """Cria gráfico de análise de complexidade"""
    tamanhos = [10, 20, 50, 100, 200, 500]
    resultados = analisar_complexidade_dijkstra(tamanhos)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(resultados['vertices'], resultados['tempos'], 
            'bo-', label='Tempo Real', linewidth=2, markersize=8)
    ax.plot(resultados['vertices'], resultados['teorico'], 
            'r--', label='O((V+E)log V)', linewidth=2)
    
    ax.set_xlabel('Número de Vértices', fontsize=12)
    ax.set_ylabel('Tempo (s) / Complexidade Normalizada', fontsize=12)
    ax.set_title('Análise de Complexidade - Algoritmo de Dijkstra', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

# Teste do visualizador
if __name__ == "__main__":
    print("🧪 Testando Visualizador de Grafo...")
    
    # Importar sistema
    try:
        from sistema_backend import SistemaVermelhinho
        
        # Criar sistema e visualizador
        sistema = SistemaVermelhinho()
        visualizador = VisualizadorGrafo(sistema)
        
        # Criar visualização básica
        visualizador.criar_visualizacao()
        visualizador.salvar_visualizacao("grafo_completo.png")
        
        # Visualizar uma rota
        fig = visualizador.visualizar_rota("RODOVIARIA", "TERMINAL_BARRA")
        if fig:
            visualizador.salvar_visualizacao("grafo_com_rota.png")
        
        # Análise de complexidade
        fig_complexidade = criar_grafico_complexidade()
        fig_complexidade.savefig("analise_complexidade.png", dpi=300, bbox_inches='tight')
        
        print("✅ Visualizações criadas com sucesso!")
        print("📊 Arquivos gerados:")
        print("   - grafo_completo.png")
        print("   - grafo_com_rota.png")
        print("   - analise_complexidade.png")
        
    except ImportError:
        print("❌ Erro: sistema_backend.py não encontrado!")
    except Exception as e:
        print(f"❌ Erro: {e}")

        if __name__ == "__main__":
            print("🧪 Testando Visualizador de Grafo...")
    
    try:
        from sistema_backend import SistemaVermelhinho
        
        sistema = SistemaVermelhinho()
        visualizador = VisualizadorGrafo(sistema)

        # Mostrar todos os IDs dos pontos disponíveis
        print("📍 Pontos disponíveis no sistema:")
        for ponto_id in sistema.pontos:
            print(f" - {ponto_id}")
        
        # Escolher dois pontos válidos manualmente
        origem = list(sistema.pontos.keys())[0]
        destino = list(sistema.pontos.keys())[1]
        print(f"\n🔄 Visualizando rota entre: {origem} -> {destino}")

        # Criar visualização sem rota
        visualizador.criar_visualizacao()
        visualizador.salvar_visualizacao("grafo_completo.png")
        
        # Criar visualização com rota válida
        fig = visualizador.visualizar_rota(origem, destino)
        if fig:
            visualizador.salvar_visualizacao("grafo_com_rota.png")
        
        # Gerar gráfico de complexidade
        fig_complexidade = criar_grafico_complexidade()
        fig_complexidade.savefig("analise_complexidade.png", dpi=300, bbox_inches='tight')
        
        print("\n✅ Visualizações criadas com sucesso!")
        print("📊 Arquivos gerados:")
        print("   - grafo_completo.png")
        print("   - grafo_com_rota.png")
        print("   - analise_complexidade.png")
        
    except ImportError:
        print("❌ Erro: sistema_backend.py não encontrado!")
    except Exception as e:
        print(f"❌ Erro: {e}")


import matplotlib.pyplot as plt

def visualizar_grafo(grafo, caminho=None):
    """
    Exibe o grafo usando matplotlib, destacando a rota se fornecida.
    """
    pos = nx.get_node_attributes(grafo, 'pos')
    labels = nx.get_node_attributes(grafo, 'nome')
    
    plt.figure(figsize=(14, 10))
    plt.title("🗺️ Rede de Transporte - Sistema Vermelinho (Maricá)", fontsize=16)
    
    # Desenhar nós e arestas normais
    nx.draw_networkx_nodes(grafo, pos, node_size=700, node_color='skyblue', edgecolors='black')
    nx.draw_networkx_edges(grafo, pos, width=2, alpha=0.6)
    nx.draw_networkx_labels(grafo, pos, labels, font_size=10)

    # Se houver rota calculada, destacar em vermelho
    if caminho and len(caminho) > 1:
        edges_rota = list(zip(caminho[:-1], caminho[1:]))
        nx.draw_networkx_edges(grafo, pos, edgelist=edges_rota, width=4, edge_color='red')
        nx.draw_networkx_nodes(grafo, pos, nodelist=caminho, node_size=800, node_color='red')
    
    plt.axis('off')
    plt.tight_layout()
    plt.show()
