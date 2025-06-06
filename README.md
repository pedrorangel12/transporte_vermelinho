# 🚇 Sistema de Otimização de Transporte Público - Maricá/RJ

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)  
![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-green.svg)  
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Busync** - Solucionando problemas computacionais complexos

## 📋 Sobre o Projeto

Este projeto foi desenvolvido por **Pedro Rangel Silva** como parte de um trabalho integrador das disciplinas de **Estrutura de Dados Avançados com Python** e **Processo de Desenvolvimento de Software**.

> ⚠️ **Nota**: O projeto foi desenvolvido individualmente, por isso a metodologia Scrum não foi aplicada de forma completa.

## 🎯 Objetivo

Criar um sistema inteligente que utiliza o **Algoritmo de Dijkstra** para encontrar rotas ótimas no sistema de transporte público de Maricá/RJ, considerando critérios como **tempo de viagem** e **acessibilidade**.

## 🌊 Por que Maricá?

Maricá é uma cidade em rápido crescimento no estado do Rio de Janeiro, conhecida por suas belas praias e desenvolvimento urbano acelerado. Com a expansão populacional e aumento do turismo, surge a necessidade de otimizar o transporte público municipal.

## 🗺️ Funcionalidades

- ✅ Algoritmo de Dijkstra personalizado para menor tempo de trajeto  
- ✅ Interface gráfica profissional com Tkinter  
- ✅ Visualização interativa da cidade com **Folium**  
- ✅ Dados realistas com pontos turísticos e relevantes de Maricá  
- ✅ Simulação automática de rotas  
- ✅ Análise detalhada de tempo, distância e acessibilidade

## 🏗️ Arquitetura

```
sistema-vermelhinho/
├── sistema_vermelhinho.py       # Backend com algoritmo e dados
├── interface_profissional.py    # Interface gráfica com Tkinter
├── mapa/                        # Mapas interativos gerados
├── assets/                      # Ícones e arquivos visuais
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos

```bash
Python 3.10+
pip
```

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/sistema-vermelhinho.git
cd sistema-vermelhinho

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o sistema
python interface_profissional.py
```

### Dependências

```
networkx>=3.0
folium>=0.14.0
tkinter (incluso no Python)
```

## 🎮 Como Usar

1. Selecione o ponto de origem e destino.
2. Marque a opção “Somente rotas acessíveis” se necessário.
3. Clique em “Calcular Rota Mais Rápida”.
4. Veja a rota textual ou visualize no mapa.

## 📌 Visualização do Grafo com Matplotlib

É possível adicionar visualização usando `matplotlib` e `networkx` para visualizar o grafo de forma simplificada:

```python
import matplotlib.pyplot as plt
import networkx as nx

G = sistema.grafo
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_size=500, font_size=8)
plt.title("Visualização do Grafo - Sistema Vermelinho")
plt.show()
```

## 🧑‍💻 Autor

**Pedro Rangel Silva**  
Desenvolvido de forma independente e com dedicação total em todas as etapas.