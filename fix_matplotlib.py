# -*- coding: utf-8 -*-
"""
🔧 CORREÇÃO MATPLOTLIB - SISTEMA VERMELINHO
Fix rápido para problemas de fonte no matplotlib
Execute ANTES de usar o sistema

Salve como: fix_matplotlib.py
"""

import matplotlib
import matplotlib.pyplot as plt
import warnings
import os

def corrigir_matplotlib():
    """Corrige configurações do matplotlib"""
    
    print("🔧 Corrigindo configurações do matplotlib...")
    
    try:
        # Suprimir warnings
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=FutureWarning)
        
        # Configurar backend seguro
        matplotlib.use('TkAgg')
        
        # Configurar fontes seguras disponíveis em qualquer sistema
        plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'Liberation Sans', 'sans-serif']
        plt.rcParams['font.size'] = 10
        plt.rcParams['font.weight'] = 'normal'
        
        # Configurar tamanhos de fonte
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 9
        plt.rcParams['figure.titlesize'] = 14
        
        # Configurar outros parâmetros
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['figure.max_open_warning'] = 0
        
        # Configurar cores e estilo
        plt.style.use('default')
        
        # Configurar salvamento
        plt.rcParams['savefig.dpi'] = 300
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['savefig.facecolor'] = 'white'
        
        print("✅ Matplotlib configurado com sucesso!")
        
        # Teste rápido
        fig, ax = plt.subplots(1, 1, figsize=(6, 4))
        ax.plot([1, 2, 3], [1, 4, 2], 'o-', label='Teste')
        ax.set_title('Teste de Configuração')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Salvar teste
        plt.savefig('teste_matplotlib.png', dpi=150, bbox_inches='tight')
        plt.close(fig)  # Fechar para não mostrar
        
        print("✅ Teste de visualização passou!")
        
        # Remover arquivo de teste
        if os.path.exists('teste_matplotlib.png'):
            os.remove('teste_matplotlib.png')
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        print("💡 Tentando configuração alternativa...")
        
        try:
            # Configuração mínima de emergência
            matplotlib.rcParams.update(matplotlib.rcParamsDefault)
            plt.rcParams['font.size'] = 10
            plt.rcParams['axes.unicode_minus'] = False
            
            print("⚠️ Configuração mínima aplicada")
            return True
            
        except Exception as e2:
            print(f"❌ Erro crítico: {e2}")
            return False

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    
    print("📦 Verificando dependências...")
    
    dependencias = {
        'matplotlib': 'matplotlib',
        'networkx': 'networkx', 
        'numpy': 'numpy',
        'tkinter': 'tkinter (built-in)'
    }
    
    erros = []
    
    for modulo, nome in dependencias.items():
        try:
            if modulo == 'tkinter':
                import tkinter
            else:
                __import__(modulo)
            print(f"✅ {nome}")
        except ImportError:
            print(f"❌ {nome} - NÃO INSTALADO")
            if modulo != 'tkinter':
                erros.append(modulo)
    
    if erros:
        print(f"\n💡 Para instalar dependências faltantes:")
        print(f"pip install {' '.join(erros)}")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def main():
    """Função principal de correção"""
    
    print("🔧 CORREÇÃO DO SISTEMA VERMELINHO")
    print("=" * 50)
    print("🎯 Corrigindo problemas de fonte e configuração")
    print()
    
    # Verificar dependências
    deps_ok = verificar_dependencias()
    
    if not deps_ok:
        print("\n❌ Instale as dependências faltantes primeiro!")
        return False
    
    print()
    
    # Corrigir matplotlib
    config_ok = corrigir_matplotlib()
    
    if not config_ok:
        print("\n❌ Não foi possível corrigir o matplotlib!")
        return False
    
    print()
    print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
    print("✅ Agora você pode executar o sistema normalmente:")
    print("   python sistema_completo_integrado.py")
    print("   python visualizacao_grafo.py")
    print("   python interface_completa.py")
    
    return True

if __name__ == "__main__":
    main()