# -*- coding: utf-8 -*-
"""
🚌 EXECUTAR SISTEMA VERMELINHO
Arquivo principal para executar o sistema
Salve como: executar_sistema.py
"""

import sys
import os

def main():
    """Função principal para executar o sistema"""
    
    print("🚌 SISTEMA VERMELINHO - MARICÁ TRANSPORT")
    print("=" * 50)
    print("🔧 Iniciando sistema...")
    
    try:
        # Importar e testar sistema backend
        print("📦 Importando sistema backend...")
        from sistema_backend import SistemaVermelhinho
        
        sistema = SistemaVermelhinho()
        print(f"✅ Backend carregado: {len(sistema.pontos)} pontos")
        
        # Importar interface
        print("🖥️ Carregando interface...")
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        # Criar interface simplificada para teste
        root = tk.Tk()
        root.title("🚌 Sistema Vermelinho - Maricá Transport")
        root.geometry("1400x900")
        root.configure(bg='#f0f0f0')
        
        # Header
        header = tk.Frame(root, bg='#2C3E50', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, 
                              text="🚌 SISTEMA VERMELINHO - MARICÁ TRANSPORT", 
                              font=('Arial', 20, 'bold'),
                              fg='white', bg='#2C3E50')
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Painel esquerdo
        left_frame = tk.LabelFrame(main_frame, text="🎯 Planejamento da Viagem", 
                                  font=('Arial', 12, 'bold'), padx=20, pady=20)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Combos
        tk.Label(left_frame, text="📍 Origem:", font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        combo_origem = ttk.Combobox(left_frame, width=40, state="readonly")
        combo_origem.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(left_frame, text="🎯 Destino:", font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        combo_destino = ttk.Combobox(left_frame, width=40, state="readonly")
        combo_destino.pack(fill=tk.X, pady=(0, 20))
        
        # Preencher combos
        pontos_nomes = sorted([ponto.nome for ponto in sistema.pontos.values()])
        combo_origem['values'] = pontos_nomes
        combo_destino['values'] = pontos_nomes
        
        if pontos_nomes:
            combo_origem.set(pontos_nomes[0])
            if len(pontos_nomes) > 1:
                combo_destino.set(pontos_nomes[1])
        
        # Variáveis globais para a rota
        ultima_rota = None
        pontos_rota = []
        
        def calcular_rota():
            """Calcula rota usando Dijkstra"""
            nonlocal ultima_rota, pontos_rota
            
            origem = combo_origem.get()
            destino = combo_destino.get()
            
            if not origem or not destino:
                messagebox.showwarning("Atenção", "Selecione origem e destino!")
                return
            
            if origem == destino:
                messagebox.showwarning("Atenção", "Origem e destino devem ser diferentes!")
                return
            
            # Buscar IDs dos pontos
            id_origem = None
            id_destino = None
            
            for id_ponto, ponto in sistema.pontos.items():
                if ponto.nome == origem:
                    id_origem = id_ponto
                if ponto.nome == destino:
                    id_destino = id_ponto
            
            if id_origem and id_destino:
                resultado = sistema.calcular_rota(id_origem, id_destino)
                
                if resultado['encontrada']:
                    ultima_rota = resultado
                    pontos_rota = resultado['pontos']
                    
                    # Mostrar resultado
                    texto_resultado = f"""🚌 ROTA CALCULADA COM SUCESSO!
                    
📍 ORIGEM: {resultado['origem']}
🎯 DESTINO: {resultado['destino']}
⏱️ TEMPO TOTAL: {resultado['tempo_total']:.1f} minutos
🚏 PARADAS: {len(resultado['pontos']) - 2} pontos intermediários
✅ STATUS: {resultado['status']}

🗺️ PERCURSO:"""
                    
                    for i, ponto_id in enumerate(resultado['pontos']):
                        ponto = sistema.pontos[ponto_id]
                        if i == 0:
                            texto_resultado += f"\n🏁 PARTIDA: {ponto.nome}"
                        elif i == len(resultado['pontos']) - 1:
                            texto_resultado += f"\n🎯 CHEGADA: {ponto.nome}"
                        else:
                            texto_resultado += f"\n🚏 PARADA {i}: {ponto.nome}"
                    
                    texto_resultado += "\n\n🌐 Clique em 'Ver no Google Maps' para visualizar!"
                    
                    # Mostrar no painel direito
                    resultado_text.delete('1.0', tk.END)
                    resultado_text.insert('1.0', texto_resultado)
                    
                    # Habilitar botão Google Maps
                    btn_google_maps.config(state=tk.NORMAL, bg='#4285F4')
                    
                    messagebox.showinfo("Sucesso", "Rota calculada com sucesso!")
                else:
                    messagebox.showerror("Erro", "Não foi possível calcular a rota!")
        
        def abrir_google_maps():
            """Abre rota no Google Maps"""
            if not ultima_rota or not pontos_rota:
                messagebox.showwarning("Atenção", "Calcule uma rota primeiro!")
                return
            
            try:
                import webbrowser
                import urllib.parse
                
                # Obter endereços dos pontos
                waypoints = []
                for ponto_id in pontos_rota:
                    ponto = sistema.pontos[ponto_id]
                    endereco_formatado = f"{ponto.endereco}, Maricá, RJ"
                    waypoints.append(endereco_formatado)
                
                # Construir URL do Google Maps
                origem = urllib.parse.quote(waypoints[0])
                destino = urllib.parse.quote(waypoints[-1])
                
                # URL base
                url_base = "https://www.google.com/maps/dir/"
                
                # Pontos intermediários
                if len(waypoints) > 2:
                    pontos_intermediarios = []
                    for waypoint in waypoints[1:-1]:
                        pontos_intermediarios.append(urllib.parse.quote(waypoint))
                    waypoints_str = "/".join(pontos_intermediarios)
                    url_completa = f"{url_base}{origem}/{waypoints_str}/{destino}"
                else:
                    url_completa = f"{url_base}{origem}/{destino}"
                
                # Adicionar modo transporte público
                url_completa += "?travelmode=transit&transit_mode=bus"
                
                # Abrir no navegador
                webbrowser.open(url_completa)
                
                messagebox.showinfo("Google Maps", 
                                  f"Rota aberta no Google Maps!\n\n"
                                  f"🚌 {ultima_rota['origem']} → {ultima_rota['destino']}\n"
                                  f"⏱️ {ultima_rota['tempo_total']:.1f} minutos\n"
                                  f"🚏 {len(pontos_rota)} pontos na rota")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir Google Maps:\n{str(e)}")
        
        # Botões
        btn_calcular = tk.Button(left_frame, 
                                text="🔍 Calcular Rota Mais Rápida",
                                command=calcular_rota,
                                bg='#3498DB', fg='white',
                                font=('Arial', 12, 'bold'),
                                pady=10, cursor='hand2')
        btn_calcular.pack(fill=tk.X, pady=(0, 10))
        
        btn_google_maps = tk.Button(left_frame,
                                   text="🌐 Ver Rota no Google Maps",
                                   command=abrir_google_maps,
                                   bg='#95A5A6', fg='white',
                                   font=('Arial', 11, 'bold'),
                                   pady=8, cursor='hand2',
                                   state=tk.DISABLED)
        btn_google_maps.pack(fill=tk.X, pady=(0, 20))
        
        # Info do sistema
        info_frame = tk.LabelFrame(left_frame, text="ℹ️ Sistema", font=('Arial', 10, 'bold'))
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_text = f"""📊 ESTATÍSTICAS:
• Pontos: {len(sistema.pontos)}
• Conexões: {sistema.grafo.number_of_edges()}
• Algoritmo: Dijkstra
• Transporte: 100% gratuito"""
        
        tk.Label(info_frame, text=info_text, font=('Consolas', 9), 
                justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=10)
        
        # Painel direito - Resultados
        right_frame = tk.LabelFrame(main_frame, text="📊 Resultados da Rota", 
                                   font=('Arial', 12, 'bold'), padx=20, pady=20)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Texto de resultado
        resultado_text = tk.Text(right_frame, font=('Consolas', 11), 
                               wrap=tk.WORD, bg='white', height=30)
        resultado_text.pack(fill=tk.BOTH, expand=True)
        
        # Mensagem inicial
        mensagem_inicial = """🚌 SISTEMA VERMELINHO - MARICÁ TRANSPORT
═══════════════════════════════════════════════════════════════

🎯 BEM-VINDO AO SISTEMA DE TRANSPORTE INTELIGENTE!

Desenvolvido pela Busync para encontrar as rotas
mais eficientes entre pontos de ônibus em Maricá/RJ.

📋 COMO USAR:
1. Selecione o ponto de origem
2. Escolha seu destino  
3. Clique em "Calcular Rota Mais Rápida"
4. Visualize a rota no Google Maps

🌟 RECURSOS:
• Algoritmo Dijkstra otimizado
• 35 pontos mapeados em Maricá
• Integração com Google Maps
• Transporte 100% gratuito

═══════════════════════════════════════════════════════════════
Sistema pronto para uso!"""
        
        resultado_text.insert('1.0', mensagem_inicial)
        
        # Status bar
        status_frame = tk.Frame(root, bg='#34495E', height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        status_label = tk.Label(status_frame,
                               text="🚌 Sistema Vermelinho pronto para uso",
                               font=('Arial', 10),
                               fg='white', bg='#34495E')
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        print("✅ Interface carregada com sucesso!")
        print("🚀 Sistema pronto para uso!")
        
        # Executar interface
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Certifique-se de ter o arquivo 'sistema_backend.py'")
        input("Pressione Enter para sair...")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()