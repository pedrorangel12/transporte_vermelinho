# -*- coding: utf-8 -*-
"""
🚌 SISTEMA VERMELINHO - INTERFACE GRÁFICA PROFISSIONAL
Busync - GUI Moderna para o Sistema de Transporte de Maricá
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import webbrowser
import os
from datetime import datetime
import heapq
import networkx as nx
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Tentar importar Folium
try:
    import folium
    from folium.plugins import Fullscreen, MeasureControl, MiniMap
    FOLIUM_DISPONIVEL = True
except ImportError:
    FOLIUM_DISPONIVEL = False

@dataclass
class PontoTransporte:
    """Representa um ponto de transporte em Maricá"""
    id: str
    nome: str
    latitude: float
    longitude: float
    tipo: str
    acessivel: bool
    descricao: str = ""

class SistemaVermelhinho:
    """Sistema do Vermelinho - Backend"""
    
    def __init__(self):
        self.pontos: Dict[str, PontoTransporte] = {}
        self.grafo = nx.Graph()
        self.configurar_dados_marica()
        
    def configurar_dados_marica(self):
        """Configura dados reais de Maricá"""
        
        # Pontos estratégicos de Maricá
        pontos_data = [
            ("centro", "Centro de Maricá", -22.9194, -42.8186, "centro", True,
             "Centro comercial e administrativo da cidade"),
            ("hospital", "Hospital Municipal Conde Modesto Leal", -22.9168, -42.8203, "hospital", True,
             "Principal hospital público com emergência 24h"),
            ("aeroporto", "Aeroporto Municipal de Maricá", -22.9241, -42.8089, "aeroporto", True,
             "Aeroporto para aviação geral e executiva"),
            ("forum", "Fórum da Comarca de Maricá", -22.9179, -42.8174, "forum", True,
             "Poder judiciário local - Totalmente acessível"),
            ("prefeitura", "Prefeitura Municipal", -22.9201, -42.8169, "governo", True,
             "Sede do governo municipal de Maricá"),
            ("rodoviaria", "Rodoviária de Maricá", -22.9206, -42.8191, "terminal", True,
             "Terminal rodoviário intermunicipal"),
            ("itaipuacu", "Itaipuaçu Centro", -22.9658, -42.9923, "bairro", False,
             "Principal bairro litorâneo de Maricá"),
            ("praia_frances", "Praia do Francês", -22.9612, -42.9734, "praia", False,
             "Praia conhecida pelo surf e natureza preservada"),
            ("parque_nanci", "Parque Natural Municipal", -22.9723, -42.9612, "parque", True,
             "Área de preservação ambiental com trilhas"),
            ("guaratiba", "Guaratiba", -22.9287, -42.8367, "bairro", True,
             "Bairro residencial com comércio local"),
            ("praia_barra", "Praia da Barra de Maricá", -22.9389, -42.8534, "praia", False,
             "Praia urbana com acesso facilitado"),
            ("lagoa_aracatiba", "Lagoa de Araçatiba", -22.9456, -42.8234, "lagoa", False,
             "Lagoa costeira integrada ao complexo lagunar"),
            ("bambui", "Bambuí", -22.9087, -42.7823, "bairro", True,
             "Região em desenvolvimento urbano"),
            ("shopping_marica", "Shopping Maricá", -22.9156, -42.8198, "shopping", True,
             "Principal centro comercial da cidade"),
        
        ]
        
        # Criar pontos
        for id_ponto, nome, lat, lng, tipo, acessivel, desc in pontos_data:
            self.pontos[id_ponto] = PontoTransporte(id_ponto, nome, lat, lng, tipo, acessivel, desc)
            self.grafo.add_node(id_ponto, nome=nome, pos=(lng, lat), tipo=tipo, 
                              acessivel=acessivel, descricao=desc)
        
        # Conexões do Vermelinho
        conexoes_data = [
            ("centro", "hospital", 1.8, 12, True),
            ("centro", "aeroporto", 3.2, 18, True),
            ("centro", "forum", 0.9, 6, True),
            ("centro", "prefeitura", 0.7, 5, True),
            ("centro", "rodoviaria", 0.8, 6, True),
            ("centro", "shopping_marica", 1.1, 8, True),

            ("rodoviaria", "itaipuacu", 22.5, 45, False),
            ("centro", "itaipuacu", 21.7, 42, False),
            ("centro", "guaratiba", 5.4, 20, True),
            ("guaratiba", "praia_barra", 3.2, 15, False),
            ("centro", "lagoa_aracatiba", 6.2, 25, False),
            ("itaipuacu", "praia_frances", 2.8, 12, False),
            ("praia_frances", 7.4, 18, False),
            ("parque_nanci", "itaipuacu", 3.2, 14, False),
            ("bambui", "centro", 9.8, 28, True),
            ("guaratiba", "hospital", 4.2, 18, True),
            ("aeroporto", "hospital", 2.6, 12, True),
            ("shopping_marica", 0.8, 6, True),
        ]
        
        # Adicionar conexões
        for origem, destino, dist, tempo, acess in conexoes_data:
            self.grafo.add_edge(origem, destino, 
                              distancia=dist, tempo=tempo, acessivel=acess)
    
    def dijkstra_mais_rapido(self, origem: str, destino: str, apenas_acessivel: bool = False):
        """Encontra a rota mais rápida"""
        if origem not in self.grafo.nodes or destino not in self.grafo.nodes:
            return [], float('inf')
        
        tempos = {node: float('inf') for node in self.grafo.nodes}
        anteriores = {node: None for node in self.grafo.nodes}
        visitados = set()
        
        tempos[origem] = 0
        heap = [(0, origem)]
        
        while heap:
            tempo_atual, no_atual = heapq.heappop(heap)
            
            if no_atual in visitados:
                continue
                
            visitados.add(no_atual)
            
            if no_atual == destino:
                break
                
            for vizinho in self.grafo.neighbors(no_atual):
                if vizinho in visitados:
                    continue
                
                edge_data = self.grafo[no_atual][vizinho]
                
                if apenas_acessivel and not edge_data['acessivel']:
                    continue
                    
                novo_tempo = tempos[no_atual] + edge_data['tempo']
                
                if novo_tempo < tempos[vizinho]:
                    tempos[vizinho] = novo_tempo
                    anteriores[vizinho] = no_atual
                    heapq.heappush(heap, (novo_tempo, vizinho))
        
        # Reconstruir caminho
        caminho = []
        no_atual = destino
        while no_atual is not None:
            caminho.append(no_atual)
            no_atual = anteriores[no_atual]
        
        caminho.reverse()
        
        if len(caminho) == 1 and caminho[0] != origem:
            return [], float('inf')
            
        return caminho, tempos[destino]
    
    def obter_detalhes_rota(self, caminho: List[str]) -> Dict:
        """Obtém detalhes completos da rota"""
        if len(caminho) < 2:
            return {}
        
        detalhes = {
            'pontos': [self.pontos[ponto].nome for ponto in caminho],
            'distancia_total_km': 0,
            'tempo_total_min': 0,
            'totalmente_acessivel': True,
            'segmentos': []
        }
        
        for i in range(len(caminho) - 1):
            origem = caminho[i]
            destino = caminho[i + 1]
            edge_data = self.grafo[origem][destino]
            
            detalhes['distancia_total_km'] += edge_data['distancia']
            detalhes['tempo_total_min'] += edge_data['tempo']
            
            if not edge_data['acessivel']:
                detalhes['totalmente_acessivel'] = False
            
            detalhes['segmentos'].append({
                'de': self.pontos[origem].nome,
                'para': self.pontos[destino].nome,
                'tempo': edge_data['tempo'],
                'distancia': edge_data['distancia'],
                'acessivel': edge_data['acessivel']
            })
        
        return detalhes
    
    def criar_mapa_interativo(self, caminho: List[str] = None) -> str:
        """Cria mapa interativo usando Folium"""
        if not FOLIUM_DISPONIVEL:
            return None
            
        # Centro do mapa em Maricá
        mapa = folium.Map(
            location=[-22.9400, -42.8400],
            zoom_start=11,
            tiles=None
        )
        
        # Adicionar camadas de mapa
        folium.TileLayer('OpenStreetMap', name='🗺️ Mapa de Ruas').add_to(mapa)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='🛰️ Vista de Satélite'
        ).add_to(mapa)
        
        # Configuração de ícones por tipo
        config_tipos = {
            'centro': {'cor': 'red', 'icone': 'star'},
            'hospital': {'cor': 'red', 'icone': 'plus'},
            'aeroporto': {'cor': 'gray', 'icone': 'plane'},
            'terminal': {'cor': 'orange', 'icone': 'bus'},
            'governo': {'cor': 'blue', 'icone': 'university'},
            'forum': {'cor': 'purple', 'icone': 'balance-scale'},
            'shopping': {'cor': 'pink', 'icone': 'shopping-cart'},
            'universidade': {'cor': 'purple', 'icone': 'graduation-cap'},
            'bairro': {'cor': 'blue', 'icone': 'home'},
            'praia': {'cor': 'green', 'icone': 'umbrella-beach'},
            'lagoa': {'cor': 'lightblue', 'icone': 'water'},
            'parque': {'cor': 'darkgreen', 'icone': 'tree'}
        }
        
        # Adicionar pontos
        for ponto_id, ponto in self.pontos.items():
            config = config_tipos.get(ponto.tipo, {'cor': 'gray', 'icone': 'info-sign'})
            
            popup_html = f"""
            <div style="width: 300px;">
                <h3 style="color: {config['cor']};">🚌 {ponto.nome}</h3>
                <p><strong>Tipo:</strong> {ponto.tipo.title()}</p>
                <p><strong>Acessibilidade:</strong> 
                {'<span style="color: green;">✅ Acessível</span>' if ponto.acessivel else '<span style="color: red;">⚠️ Limitado</span>'}</p>
                <p><strong>Descrição:</strong> {ponto.descricao}</p>
                <p><strong>Coordenadas:</strong> {ponto.latitude:.6f}, {ponto.longitude:.6f}</p>
            </div>
            """
            
            folium.Marker(
                location=[ponto.latitude, ponto.longitude],
                popup=folium.Popup(popup_html, max_width=320),
                tooltip=f"🚌 {ponto.nome}",
                icon=folium.Icon(color=config['cor'], icon=config['icone'], prefix='fa')
            ).add_to(mapa)
        
        # Adicionar rota se fornecida
        if caminho and len(caminho) > 1:
            coordenadas_rota = []
            for ponto_id in caminho:
                if ponto_id in self.pontos:
                    ponto = self.pontos[ponto_id]
                    coordenadas_rota.append([ponto.latitude, ponto.longitude])
            
            if coordenadas_rota:
                folium.PolyLine(
                    locations=coordenadas_rota,
                    color='red',
                    weight=6,
                    opacity=0.9,
                    popup='🚌 Rota Mais Rápida do Vermelinho'
                ).add_to(mapa)
                
                # Marcadores de origem e destino
                folium.Marker(
                    location=coordenadas_rota[0],
                    popup='🏁 ORIGEM',
                    icon=folium.Icon(color='green', icon='play', prefix='fa')
                ).add_to(mapa)
                
                folium.Marker(
                    location=coordenadas_rota[-1],
                    popup='🎯 DESTINO',
                    icon=folium.Icon(color='red', icon='flag-checkered', prefix='fa')
                ).add_to(mapa)
        
        # Adicionar plugins
        Fullscreen().add_to(mapa)
        MiniMap(toggle_display=True).add_to(mapa)
        folium.LayerControl().add_to(mapa)
        
        # Salvar mapa
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"mapa_vermelinho_{timestamp}.html"
        mapa.save(nome_arquivo)
        
        return nome_arquivo

class InterfaceProfissional:
    """Interface Gráfica Profissional"""
    
    def __init__(self):
        self.sistema = SistemaVermelhinho()
        self.root = tk.Tk()
        self.configurar_janela()
        self.criar_interface()
        self.ultima_rota = None
        
    def configurar_janela(self):
        """Configura a janela principal"""
        self.root.title("🚌 Sistema Vermelinho - Maricá Transport")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Configurar estilo
        self.root.configure(bg='#f0f0f0')
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Ícone (se disponível)
        try:
            self.root.iconbitmap("bus.ico")
        except:
            pass
    
    def criar_interface(self):
        """Cria a interface completa"""
        
        # Header profissional
        self.criar_header()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Painel esquerdo - Controles
        self.criar_painel_controles(main_frame)
        
        # Painel direito - Resultados
        self.criar_painel_resultados(main_frame)
        
        # Status bar
        self.criar_status_bar()
    
    def criar_header(self):
        """Cria header profissional"""
        header_frame = tk.Frame(self.root, bg='#2C3E50', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo e título
        title_frame = tk.Frame(header_frame, bg='#2C3E50')
        title_frame.pack(expand=True)
        
        # Título principal
        title_label = tk.Label(title_frame, 
                              text="🚌 SISTEMA VERMELINHO", 
                              font=('Arial', 24, 'bold'),
                              fg='white', bg='#2C3E50')
        title_label.pack(pady=(15, 5))
        
        # Subtítulo
        subtitle_label = tk.Label(title_frame,
                                 text="Busync - Transporte Público Inteligente de Maricá/RJ",
                                 font=('Arial', 12),
                                 fg='#BDC3C7', bg='#2C3E50')
        subtitle_label.pack()
        
        # Info do sistema
        info_label = tk.Label(title_frame,
                             text=f"📍 {len(self.sistema.pontos)} pontos mapeados | 🔗 {self.sistema.grafo.number_of_edges()} conexões | 💰 100% GRATUITO",
                             font=('Arial', 10),
                             fg='#95A5A6', bg='#2C3E50')
        info_label.pack()
    
    def criar_painel_controles(self, parent):
        """Cria painel de controles"""
        # Frame esquerdo
        left_frame = ttk.LabelFrame(parent, text="🎯 Planejamento da Viagem", padding="20")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Origem
        ttk.Label(left_frame, text="📍 Ponto de Origem:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.combo_origem = ttk.Combobox(left_frame, width=35, state="readonly", font=('Arial', 11))
        self.combo_origem.pack(fill=tk.X, pady=(0, 15))
        
        # Destino
        ttk.Label(left_frame, text="🎯 Ponto de Destino:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.combo_destino = ttk.Combobox(left_frame, width=35, state="readonly", font=('Arial', 11))
        self.combo_destino.pack(fill=tk.X, pady=(0, 15))
        
        # Opções de acessibilidade
        ttk.Label(left_frame, text="♿ Opções de Acessibilidade:", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.var_acessivel = tk.BooleanVar()
        check_acessivel = ttk.Checkbutton(left_frame, 
                                         text="Apenas rotas totalmente acessíveis",
                                         variable=self.var_acessivel,
                                         font=('Arial', 10))
        check_acessivel.pack(anchor=tk.W, pady=(0, 20))
        
        # Botões de ação
        self.criar_botoes_acao(left_frame)
        
        # Informações do sistema
        self.criar_info_sistema(left_frame)
        
        # Preencher dados
        self.atualizar_combos()
    
    def criar_botoes_acao(self, parent):
        """Cria botões de ação"""
        
        # Botão principal - Calcular Rota
        btn_calcular = tk.Button(parent, 
                                text="🔍 Calcular Rota Mais Rápida",
                                command=self.calcular_rota,
                                bg='#3498DB', fg='white',
                                font=('Arial', 12, 'bold'),
                                relief=tk.FLAT, pady=10,
                                cursor='hand2')
        btn_calcular.pack(fill=tk.X, pady=(0, 10))
        
        # Botão mapa interativo
        cor_mapa = '#27AE60' if FOLIUM_DISPONIVEL else '#95A5A6'
        texto_mapa = "🗺️ Abrir Mapa Interativo" if FOLIUM_DISPONIVEL else "🗺️ Mapa Interativo (Instalar Folium)"
        
        btn_mapa = tk.Button(parent,
                            text=texto_mapa,
                            command=self.abrir_mapa_interativo,
                            bg=cor_mapa, fg='white',
                            font=('Arial', 11, 'bold'),
                            relief=tk.FLAT, pady=8,
                            cursor='hand2')
        btn_mapa.pack(fill=tk.X, pady=(0, 10))
        
        # Botão demonstração
        btn_demo = tk.Button(parent,
                            text="🎬 Demonstração Automática",
                            command=self.executar_demonstracao,
                            bg='#E67E22', fg='white',
                            font=('Arial', 11, 'bold'),
                            relief=tk.FLAT, pady=8,
                            cursor='hand2')
        btn_demo.pack(fill=tk.X, pady=(0, 10))
        
        # Botão limpar
        btn_limpar = tk.Button(parent,
                              text="🗑️ Limpar Resultados",
                              command=self.limpar_resultados,
                              bg='#95A5A6', fg='white',
                              font=('Arial', 11),
                              relief=tk.FLAT, pady=6,
                              cursor='hand2')
        btn_limpar.pack(fill=tk.X, pady=(0, 20))
    
    def criar_info_sistema(self, parent):
        """Cria painel de informações do sistema"""
        info_frame = ttk.LabelFrame(parent, text="ℹ️ Informações do Sistema", padding="10")
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Estatísticas
        total_pontos = len(self.sistema.pontos)
        pontos_acessiveis = sum(1 for p in self.sistema.pontos.values() if p.acessivel)
        
        stats_text = f"""📊 ESTATÍSTICAS:
• Pontos mapeados: {total_pontos}
• Pontos acessíveis: {pontos_acessiveis} ({(pontos_acessiveis/total_pontos*100):.1f}%)
• Conexões: {self.sistema.grafo.number_of_edges()}
• Folium: {'✅ Instalado' if FOLIUM_DISPONIVEL else '❌ Não instalado'}

🎯 ALGORITMO:
• Dijkstra otimizado
• Critério: Tempo de viagem
• Transporte: 100% gratuito"""
        
        info_label = tk.Label(info_frame, text=stats_text, 
                             font=('Consolas', 9), 
                             bg='#f0f0f0', justify=tk.LEFT)
        info_label.pack(anchor=tk.W)
    
    def criar_painel_resultados(self, parent):
        """Cria painel de resultados"""
        # Frame direito
        right_frame = ttk.LabelFrame(parent, text="📊 Resultados e Análise", padding="20")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Área de texto para resultados
        self.texto_resultados = scrolledtext.ScrolledText(right_frame, 
                                                         wrap=tk.WORD,
                                                         font=('Consolas', 11),
                                                         bg='white',
                                                         fg='#2C3E50',
                                                         height=25)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Mensagem inicial
        self.mostrar_mensagem_inicial()
    
    def criar_status_bar(self):
        """Cria barra de status"""
        self.status_frame = tk.Frame(self.root, bg='#34495E', height=30)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_frame.pack_propagate(False)
        self.status_label = ttk(staticmethod)
        self.__setattr__ = threading
        
        self.status_label = tk.Label(self.status_frame,
                                    text="🚌 Sistema Vermelinho pronto para uso",
                                    font=('Arial', 10),
                                    fg='white', bg='#34495E')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Data e hora
        self.data_label = tk.Label(self.status_frame,
                                  text=datetime.now().strftime("📅 %d/%m/%Y %H:%M"),
                                  font=('Arial', 10),
                                  fg='#BDC3C7', bg='#34495E')
        self.data_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def atualizar_combos(self):
        """Atualiza os comboboxes com os pontos"""
        pontos_nomes = []
        for ponto in self.sistema.pontos.values():
            acess_icon = "♿" if ponto.acessivel else "⚠️"
            tipo_icon = {
                'centro': '🏛️', 'hospital': '🏥', 'terminal': '🚌', 
                'governo': '🏢', 'aeroporto': '✈️', 'forum': '⚖️',
                'shopping': '🛒', 'universidade': '🎓',
                'bairro': '🏘️', 'praia': '🏖️', 'lagoa': '🌊', 'parque': '🌳'
            }.get(ponto.tipo, '📍')
            
            pontos_nomes.append(f"{tipo_icon} {ponto.nome} {acess_icon}")
        
        pontos_nomes.sort()
        
        self.combo_origem['values'] = pontos_nomes
        self.combo_destino['values'] = pontos_nomes
        
        # Valores padrão
        if pontos_nomes:
            # Definir Itaipuaçu como origem padrão se existir
            for i, nome in enumerate(pontos_nomes):
                if "Itaipuaçu" in nome:
                    self.combo_origem.current(i)
                    break
            
            # Definir Centro como destino padrão se existir
            for i, nome in enumerate(pontos_nomes):
                if "Centro de Maricá" in nome:
                    self.combo_destino.current(i)
                    break
    
    def mostrar_mensagem_inicial(self):
        """Mostra mensagem inicial no painel de resultados"""
        mensagem = """
🚌 SISTEMA VERMELINHO - MARICÁ/RJ
═══════════════════════════════════════════════════════════

Bem-vindo ao sistema profissional de otimização de rotas do Vermelinho!

🎯 COMO USAR:
1. Selecione o ponto de ORIGEM no primeiro dropdown
2. Selecione o ponto de DESTINO no segundo dropdown
3. Marque a opção de acessibilidade se necessário
4. Clique em "🔍 Calcular Rota Mais Rápida"

💡 RECURSOS DISPONÍVEIS:
• Cálculo de rota mais rápida usando algoritmo de Dijkstra
• Opção de filtrar apenas rotas acessíveis
• Mapa interativo estilo Google Maps (se Folium instalado)
• Demonstração automática com casos reais
• Análise detalhada de tempo, distância e acessibilidade

🚌 SOBRE O VERMELINHO:
O sistema de transporte público de Maricá é 100% GRATUITO!
Nosso algoritmo otimiza apenas o tempo de viagem, já que não há custos.

♿ ACESSIBILIDADE:
• Pontos com ♿ são totalmente acessíveis
• Pontos com ⚠️ têm limitações de acesso
• Use a opção "Apenas rotas acessíveis" quando necessário


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""