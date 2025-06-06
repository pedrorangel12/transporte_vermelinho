# -*- coding: utf-8 -*-
"""
🧪 TESTE MÍNIMO - VERIFICAR SE INTERFACE FUNCIONA
Salve como: teste_minimo.py
"""

print("🚀 Iniciando teste mínimo...")

try:
    import tkinter as tk
    print("✅ Tkinter importado com sucesso")
except ImportError as e:
    print(f"❌ Erro no Tkinter: {e}")
    print("💡 Instale com: pip install tk")
    exit()

try:
    from tkinter import ttk, messagebox
    print("✅ Módulos do Tkinter OK")
except ImportError as e:
    print(f"❌ Erro nos módulos: {e}")
    exit()

try:
    import heapq
    import networkx as nx
    from dataclasses import dataclass
    print("✅ Bibliotecas básicas OK")
except ImportError as e:
    print(f"❌ Erro nas bibliotecas: {e}")
    print("💡 Instale com: pip install networkx")
    exit()

print("🎯 Criando janela de teste...")

class TesteMinimo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧪 Teste Sistema Vermelinho")
        self.root.geometry("800x600")
        self.criar_interface()
    
    def criar_interface(self):
        # Header
        header = tk.Label(self.root, 
                         text="🚌 TESTE SISTEMA VERMELINHO", 
                         font=('Arial', 20, 'bold'),
                         bg='#2C3E50', fg='white', pady=20)
        header.pack(fill=tk.X)
        
        # Área central
        frame_central = tk.Frame(self.root, bg='white')
        frame_central.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mensagem de teste
        tk.Label(frame_central, 
                text="✅ INTERFACE FUNCIONANDO!", 
                font=('Arial', 16, 'bold'),
                fg='green').pack(pady=50)
        
        tk.Label(frame_central, 
                text="Se você está vendo esta janela,\na interface gráfica está funcionando corretamente!", 
                font=('Arial', 12),
                justify=tk.CENTER).pack(pady=20)
        
        # Botão de teste
        def teste_click():
            messagebox.showinfo("Teste", "🎉 Botão funcionando!\nTodos os componentes OK!")
        
        tk.Button(frame_central,
                 text="🧪 Testar Componentes",
                 command=teste_click,
                 bg='#3498DB', fg='white',
                 font=('Arial', 14, 'bold'),
                 pady=10, padx=30).pack(pady=30)
        
        # Instruções
        instrucoes = """
📋 STATUS DOS TESTES:
✅ Python executando
✅ Tkinter funcionando
✅ Interface carregada
✅ Botões responsivos

💡 PRÓXIMOS PASSOS:
1. Clique no botão azul acima
2. Se aparecer um popup, tudo está OK!
3. Feche esta janela
4. Execute o sistema completo
        """
        
        tk.Label(frame_central,
                text=instrucoes,
                font=('Consolas', 10),
                justify=tk.LEFT,
                bg='#f8f9fa',
                fg='#2c3e50').pack(pady=20, padx=20, fill=tk.X)
        
        # Botão fechar
        tk.Button(frame_central,
                 text="❌ Fechar Teste",
                 command=self.root.destroy,
                 bg='#e74c3c', fg='white',
                 font=('Arial', 12)).pack(pady=20)
    
    def executar(self):
        try:
            print("🖥️ Mostrando janela...")
            self.root.mainloop()
            print("👋 Janela fechada")
        except Exception as e:
            print(f"❌ Erro na interface: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Executando teste mínimo...")
    
    try:
        app = TesteMinimo()
        app.executar()
        print("✅ Teste concluído com sucesso!")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n🔧 POSSÍVEIS SOLUÇÕES:")
        print("1. pip install tkinter")
        print("2. pip install networkx")
        print("3. python -m pip install --upgrade pip")
        print("4. Usar python3 no lugar de python")