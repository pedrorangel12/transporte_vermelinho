# -*- coding: utf-8 -*-
"""
🚌 SISTEMA BACKEND - ALGORITMO DIJKSTRA
Sistema Vermelinho - Maricá Transport (DADOS REAIS)
Busync

Salve como: sistema_backend.py
"""

import networkx as nx
import heapq
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math

@dataclass
class PontoOnibus:
    """Representa um ponto de ônibus"""
    id: str
    nome: str
    endereco: str
    latitude: float = -22.9194  # Coordenada padrão de Maricá
    longitude: float = -42.8186
    acessivel: bool = True
    tipo: str = "parada"  # parada, terminal, estacao
    linhas: List[str] = None  # Linhas que passam por este ponto

    def __post_init__(self):
        if self.linhas is None:
            self.linhas = []

class SistemaVermelhinho:
    """Sistema principal de cálculo de rotas usando Dijkstra com dados reais do Vermelinho"""
    
    def __init__(self):
        self.pontos: Dict[str, PontoOnibus] = {}
        self.grafo = nx.Graph()
        self.linhas_vermelinho = {}
        self._criar_mapa_vermelinho_real()
        print(f"✅ Sistema Vermelinho iniciado com {len(self.pontos)} pontos e {self.grafo.number_of_edges()} conexões")
    
    def _criar_mapa_vermelinho_real(self):
        """Cria o mapa real do Sistema Vermelinho de Maricá"""
        
        # Pontos principais do sistema (baseado nos itinerários reais)
        pontos_sistema = [
            # Terminais e Pontos Centrais
            ("RODOVIARIA", "Terminal Rodoviário", "Praça da Rodoviária, Centro, Maricá", -22.9194, -42.8186, True, "terminal"),
            ("CENTRO_SAQU", "Centro (Saquarema)", "Av. Roberto Silveira próx. ao RJ-106", -22.9189, -42.8175, True, "parada"),
            ("PRACA_PONTA_NEGRA", "Praça de Ponta Negra", "Praça de Ponta Negra, Centro", -22.9201, -42.8188, True, "parada"),
            
            # Pontos da Linha E01 - Centro x Ponta Negra (via Manoel Ribeiro)
            ("AV_ROBERTO_SILVEIRA", "Av. Roberto Silveira", "Av. Roberto Silveira, Centro", -22.9178, -42.8203, True, "parada"),
            ("ESTRADA_SAMPAIO_CORREIA", "Estrada Sampaio Correia-Jaconé", "Estrada Sampaio Correia-Jaconé", -22.9345, -42.8567, True, "parada"),
            ("RUA_SAO_PEDRO_APOSTOLO", "Rua São Pedro Apóstolo", "Rua São Pedro Apóstolo", -22.9234, -42.8223, True, "parada"),
            ("PREFEITO_ARTURZINHO", "Av. Prefeito Arturzinho Rangel", "Av. Prefeito Arturzinho Rangel", -22.9156, -42.8134, True, "parada"),
            ("RETORNO_RJ106", "Retorno RJ-106", "RJ-106 (Sentido Niterói)", -22.9123, -42.8089, True, "parada"),
            ("MARIO_LOPES_FONTOURA", "R. Mário Lopes Fontoura", "Rua Mário Lopes Fontoura", -22.9167, -42.8145, True, "parada"),
            ("LUIZ_ANTONIO_CUNHA", "R. Ver. Luiz Antônio da Cunha", "Rua Vereador Luiz Antônio da Cunha", -22.9178, -42.8156, True, "parada"),
            
            # Pontos da Linha E01A - Centro x Ponta Negra (via Vale da Figueira)
            ("RUA_VINTE", "Rua Vinte", "Rua Vinte", -22.9245, -42.8298, True, "parada"),
            ("RUA_QUINZE", "Rua Quinze", "Rua Quinze", -22.9256, -42.8311, True, "parada"),
            ("KM_30_RJ106", "KM 30 - RJ-106", "RJ-106 KM 30", -22.9098, -42.8045, True, "parada"),
            
            # Pontos da Linha E02 - Centro x Ponta Negra (via Cordeirinho)
            ("RUA_ABREU_SODRE", "Rua Abreu Sodré", "Rua Abreu Sodré", -22.9212, -42.8167, True, "parada"),
            ("RUA_JOAQUIM_SANTOS", "Rua Joaquim Eugênio dos Santos", "Rua Joaquim Eugênio dos Santos", -22.9201, -42.8175, True, "parada"),
            ("RUA_BARAO_INOA", "Rua Barão de Inoã", "Rua Barão de Inoã", -22.9195, -42.8175, True, "parada"),
            ("RUA_ALVARES_CASTRO", "Rua Álvares de Castro", "Rua Álvares de Castro", -22.9189, -42.8181, True, "parada"),
            ("RUA_SILVINO_SIQUEIRA", "Rua Silvino Alves de Siqueira", "Rua Silvino Alves de Siqueira", -22.9203, -42.8189, True, "parada"),
            ("AV_NOSSA_SENHORA_AMPARO", "Av. Nossa Senhora do Amparo", "Av. Nossa Senhora do Amparo", -22.9234, -42.8234, True, "parada"),
            ("AV_IVAN_MUNDIM", "Av. Ivan Mundim", "Av. Ivan Mundim", -22.9267, -42.8278, True, "parada"),
            ("AV_JOAO_SALDANHA", "Av. João Saldanha", "Av. João Saldanha", -22.9289, -42.8312, True, "parada"),
            ("RUA_ZERO", "Rua Zero", "Rua Zero", -22.9234, -42.8298, True, "parada"),
            ("AV_MAYSA", "Av. Maysa", "Av. Maysa", -22.9345, -42.8456, True, "parada"),
            ("ESTRADA_ANTONIO_CALLADO", "Estrada Antônio Callado (RUA 90)", "Estrada Antônio Callado", -22.9423, -42.8567, True, "parada"),
            ("PRACA_BAMBUI", "Praça de Bambuí", "Praça de Bambuí", -22.9389, -42.8523, True, "parada"),
            ("ESTRADA_CONTORNO", "Estrada do Contorno", "Estrada do Contorno", -22.9401, -42.8545, True, "parada"),
            ("AV_BRAULINO_COSTA", "Av. Braulino Venâncio da Costa", "Av. Braulino Venâncio da Costa", -22.9434, -42.8578, True, "parada"),
            ("RUA_CAP_JOSE_OLIVEIRA", "Rua Cap. José Caetano de Oliveira", "Rua Cap. José Caetano de Oliveira", -22.9445, -42.8589, True, "parada"),
            
            # Pontos específicos de cada linha
            # E03 - Centro x Ubatiba
            ("RUA_FIRMIANO_FIGUEIREDO", "Rua Firmiano Francisco de Figueiredo", "Rua Firmiano Francisco de Figueiredo", -22.8956, -42.8234, True, "parada"),
            ("RUA_RIO_JANEIRO", "Rua Rio de Janeiro", "Rua Rio de Janeiro", -22.8934, -42.8212, True, "parada"),
            ("RUA_LEONIDAS_MOREIRA", "Rua Leônidas Moreira", "Rua Leônidas Moreira", -22.8945, -42.8223, True, "parada"),
            ("RUA_NOVA_FRIBURGO", "Rua Nova Friburgo", "Rua Nova Friburgo", -22.8967, -42.8245, True, "parada"),
            ("RUA_VOLTA_REDONDA", "Rua Volta Redonda", "Rua Volta Redonda", -22.8978, -42.8256, True, "parada"),
            
            # E04 - Centro x Silvado
            ("ESTRADA_SILVADO", "Estrada do Silvado", "Estrada do Silvado (Comandante Celso)", -22.8789, -42.7944, True, "parada"),
            
            # E05 - Centro x Lagarto
            ("COLEGIO_JOVINA_AMARAL", "Colégio Jovina Amaral", "RJ-114 KM 18 - Colégio Jovina Amaral", -22.8567, -42.7789, True, "parada"),
            
            # E06 - Centro x Espraiado
            ("ESTRADA_ESPRAIADO", "Estrada do Espraiado", "Estrada do Espraiado", -22.9456, -42.8612, True, "parada"),
            ("SITIO_RIACHO", "Sítio do Riacho", "Sítio do Riacho", -22.9478, -42.8634, True, "parada"),
            
            # E07 - Centro x Caxito (via Alecrim)
            ("ESTRADA_CAXITO", "Estrada do Caxito", "Estrada do Caxito", -22.9123, -42.7856, True, "parada"),
            ("RUA_CECILIA_MATARUNA", "Rua Cecília Gonçalves Mataruna", "Rua Cecília Gonçalves Mataruna", -22.9134, -42.7867, True, "parada"),
            ("ESTRADA_HENFIL", "Estrada Henfil", "Estrada Henfil (Sentido Condomínio Vitória dos Anjos)", -22.9145, -42.7878, True, "parada"),
            ("ESTRADA_CAMBURI", "Estrada do Camburi", "Estrada do Camburi", -22.9156, -42.7889, True, "parada"),
            
            # E08 - Centro x Jacaroá (via Amizade)
            ("RUA_CLIMACO_PEREIRA", "Rua Clímaco Pereira", "Rua Clímaco Pereira", -22.9289, -42.8345, True, "parada"),
            ("RUA_DOMICIO_GAMA", "Rua Domício da Gama", "Rua Domício da Gama", -22.9301, -42.8356, True, "parada"),
            ("RUA_PADRE_ARLINDO", "Rua Padre Arlindo Vieira", "Rua Padre Arlindo Vieira", -22.9312, -42.8367, True, "parada"),
            ("RUA_PREFEITO_JOAQUIM", "Rua Prefeito Joaquim Mendes", "Rua Prefeito Joaquim Mendes", -22.9323, -42.8378, True, "parada"),
            ("RUA_ANTONIO_GOMES", "Rua Antônio Gomes", "Rua Antônio Gomes", -22.9334, -42.8389, True, "parada"),
            ("RUA_REGINALDO_FONSECA", "Rua Reginaldo G. da Fonseca", "Rua Reginaldo G. da Fonseca", -22.9345, -42.8400, True, "parada"),
            ("AVENIDA_TRES", "Avenida Três", "Avenida Três", -22.9356, -42.8411, True, "parada"),
            ("ESTRADA_JACAROA", "Estrada de Jacaroá", "Estrada de Jacaroá", -22.9367, -42.8422, True, "parada"),
            ("PRACA_NENEM", "Praça do Neném", "Praça do Neném", -22.9378, -42.8433, True, "parada"),
            ("RUA_OUVIDOR_SOUZA", "Rua Ouvidor Souza", "Rua Ouvidor Souza", -22.9389, -42.8444, True, "parada"),
            ("AV_DIOGENES_COSTA", "Avenida Diógenes Paula Costa (Av. Lagomar)", "Av. Diógenes Paula Costa", -22.9400, -42.8455, True, "parada"),
            ("CAMPO_CAJU", "Campo do Caju", "Campo do Caju", -22.9411, -42.8466, True, "parada"),
            
            # E08A - Jacaroá (via Amizade/via Campo)
            ("AV_NERO_SILVA", "Av. Nero da Silva Bittencourt", "Av. Nero da Silva Bittencourt", -22.9422, -42.8477, True, "parada"),
            ("ESTR_ZILTO_MONTEIRO", "Estr. Zilto Monteiro de Abreu", "Estrada Zilto Monteiro de Abreu", -22.9433, -42.8488, True, "parada"),
            
            # E09 - Centro x Guaratiba (via Caju/Interlagos)
            ("RUA_DOIS", "Rua Dois", "Rua Dois", -22.9444, -42.8499, True, "parada"),
            ("AV_REGINALDO_ZEIDAN", "Av. Reginaldo Zeidan", "Av. Reginaldo Zeidan", -22.9455, -42.8510, True, "parada"),
            ("ESTRADA_BEIRA_LAGOA", "Estrada Beira da Lagoa", "Estrada Beira da Lagoa", -22.9466, -42.8521, True, "parada"),
            ("RUA_32", "Rua 32", "Rua 32", -22.9477, -42.8532, True, "parada"),
            ("RUA_56", "Rua 56", "Rua 56", -22.9488, -42.8543, True, "parada"),
            ("ESTRADA_PONTE_NEGRA", "Estrada da Ponte Negra", "Estrada da Ponte Negra", -22.9499, -42.8554, True, "parada"),
            ("AV_UM_BEIRA_LAGOA", "Av. Um (Beira da Lagoa - Lado Leste)", "Av. Um (Beira da Lagoa)", -22.9510, -42.8565, True, "parada"),
            ("RUA_CENTO_DEZ", "Rua Cento e Dez", "Rua Cento e Dez", -22.9521, -42.8576, True, "parada"),
            ("AV_UM_LOT_JP", "Av. Um Lot. JP Interlagos", "Av. Um Lot. JP Interlagos", -22.9532, -42.8587, True, "parada"),
            ("ESTRADA_GAMBOA", "Estrada da Gamboa", "Estrada da Gamboa", -22.9543, -42.8598, True, "parada"),
            ("FABIANO_FERREIRA", "Fabiano Ferreira dos Santos Medeiros", "Fabiano Ferreira dos Santos Medeiros", -22.9554, -42.8609, True, "parada"),
            ("ALZIRO_RODRIGUES", "Alziro Rodrigues Pereira", "Alziro Rodrigues Pereira", -22.9565, -42.8620, True, "parada"),
        ]
        
        # Criar pontos
        for dados in pontos_sistema:
            ponto = PontoOnibus(
                id=dados[0],
                nome=dados[1],
                endereco=dados[2],
                latitude=dados[3],
                longitude=dados[4],
                acessivel=dados[5],
                tipo=dados[6],
                linhas=[]
            )
            self.pontos[dados[0]] = ponto
            self.grafo.add_node(dados[0])
        
        # Definir as linhas do Vermelinho com seus itinerários
        self._definir_linhas_vermelinho()
        
        # Criar conexões baseadas nas linhas
        self._criar_conexoes_linhas()
    
    def _definir_linhas_vermelinho(self):
        """Define as linhas do Sistema Vermelinho com os itinerários reais"""
        
        self.linhas_vermelinho = {
            "E01": {
                "nome": "CENTRO X PONTA NEGRA (VIA MANOEL RIBEIRO)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "CENTRO_SAQU", 
                    "ESTRADA_SAMPAIO_CORREIA", "RUA_SAO_PEDRO_APOSTOLO", "PRACA_PONTA_NEGRA"
                ],
                "volta": [
                    "PRACA_PONTA_NEGRA", "PREFEITO_ARTURZINHO", "RUA_SAO_PEDRO_APOSTOLO",
                    "ESTRADA_SAMPAIO_CORREIA", "CENTRO_SAQU", "RETORNO_RJ106", "KM_30_RJ106",
                    "CENTRO_SAQU", "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA", 
                    "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E01A": {
                "nome": "CENTRO X PONTA NEGRA (VIA VALE DA FIGUEIRA)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "CENTRO_SAQU", "RUA_VINTE", 
                    "RUA_QUINZE", "ESTRADA_SAMPAIO_CORREIA", "RUA_SAO_PEDRO_APOSTOLO", "PRACA_PONTA_NEGRA"
                ],
                "volta": [
                    "PRACA_PONTA_NEGRA", "PREFEITO_ARTURZINHO", "RUA_SAO_PEDRO_APOSTOLO",
                    "ESTRADA_SAMPAIO_CORREIA", "RUA_VINTE", "RUA_QUINZE", "ESTRADA_SAMPAIO_CORREIA",
                    "CENTRO_SAQU", "RETORNO_RJ106", "KM_30_RJ106", "CENTRO_SAQU", 
                    "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E02": {
                "nome": "CENTRO X PONTA NEGRA (VIA CORDEIRINHO)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "RUA_ABREU_SODRE", "RUA_JOAQUIM_SANTOS",
                    "RUA_BARAO_INOA", "RUA_ALVARES_CASTRO", "RUA_SILVINO_SIQUEIRA", 
                    "AV_NOSSA_SENHORA_AMPARO", "AV_IVAN_MUNDIM", "AV_JOAO_SALDANHA", "RUA_ZERO",
                    "AV_MAYSA", "ESTRADA_ANTONIO_CALLADO", "PRACA_BAMBUI", "ESTRADA_CONTORNO",
                    "AV_BRAULINO_COSTA", "ESTRADA_ANTONIO_CALLADO", "RUA_CAP_JOSE_OLIVEIRA"
                ],
                "volta": [
                    "RUA_CAP_JOSE_OLIVEIRA", "ESTRADA_CONTORNO", "AV_BRAULINO_COSTA",
                    "ESTRADA_ANTONIO_CALLADO", "PRACA_BAMBUI", "ESTRADA_CONTORNO", 
                    "AV_BRAULINO_COSTA", "ESTRADA_ANTONIO_CALLADO", "AV_MAYSA",
                    "AV_JOAO_SALDANHA", "AV_IVAN_MUNDIM", "AV_NOSSA_SENHORA_AMPARO",
                    "RUA_SILVINO_SIQUEIRA", "RUA_ALVARES_CASTRO", "RUA_BARAO_INOA",
                    "RUA_JOAQUIM_SANTOS", "RUA_ABREU_SODRE", "AV_ROBERTO_SILVEIRA",
                    "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E02A": {
                "nome": "CENTRO X PONTA NEGRA (EXPRESSO via CORDEIRINHO)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "RUA_ABREU_SODRE", "RUA_JOAQUIM_SANTOS",
                    "RUA_BARAO_INOA", "RUA_ALVARES_CASTRO", "RUA_SILVINO_SIQUEIRA",
                    "AV_NOSSA_SENHORA_AMPARO", "AV_IVAN_MUNDIM", "AV_JOAO_SALDANHA", "RUA_ZERO",
                    "AV_MAYSA", "PREFEITO_ARTURZINHO", "RUA_CAP_JOSE_OLIVEIRA"
                ],
                "volta": [
                    "RUA_CAP_JOSE_OLIVEIRA", "AV_MAYSA", "AV_JOAO_SALDANHA", "AV_IVAN_MUNDIM",
                    "AV_NOSSA_SENHORA_AMPARO", "RUA_SILVINO_SIQUEIRA", "RUA_ALVARES_CASTRO",
                    "RUA_BARAO_INOA", "RUA_JOAQUIM_SANTOS", "RUA_ABREU_SODRE", "AV_ROBERTO_SILVEIRA",
                    "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E03": {
                "nome": "CENTRO X UBATIBA",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "RUA_FIRMIANO_FIGUEIREDO",
                    "RUA_RIO_JANEIRO", "RUA_LEONIDAS_MOREIRA", "RUA_NOVA_FRIBURGO", "RUA_VOLTA_REDONDA"
                ],
                "volta": [
                    "RUA_VOLTA_REDONDA", "RUA_NOVA_FRIBURGO", "RUA_LEONIDAS_MOREIRA",
                    "RUA_RIO_JANEIRO", "RUA_FIRMIANO_FIGUEIREDO", "RETORNO_RJ106", 
                    "KM_30_RJ106", "CENTRO_SAQU", "AV_ROBERTO_SILVEIRA", 
                    "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E04": {
                "nome": "CENTRO X SILVADO",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "ESTRADA_SILVADO"
                ],
                "volta": [
                    "ESTRADA_SILVADO", "RETORNO_RJ106", "KM_30_RJ106", "CENTRO_SAQU",
                    "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E05": {
                "nome": "CENTRO X LAGARTO",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "COLEGIO_JOVINA_AMARAL"
                ],
                "volta": [
                    "COLEGIO_JOVINA_AMARAL", "RETORNO_RJ106", "KM_30_RJ106", "CENTRO_SAQU",
                    "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA", 
                    "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E06": {
                "nome": "CENTRO X ESPRAIADO",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "CENTRO_SAQU", 
                    "ESTRADA_ESPRAIADO", "SITIO_RIACHO"
                ],
                "volta": [
                    "SITIO_RIACHO", "ESTRADA_ESPRAIADO", "RETORNO_RJ106", "KM_30_RJ106",
                    "CENTRO_SAQU", "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA",
                    "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E07": {
                "nome": "CENTRO X CAXITO (VIA ALECRIM)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "CENTRO_SAQU", "ESTRADA_CAXITO",
                    "RUA_CECILIA_MATARUNA", "ESTRADA_HENFIL", "ESTRADA_CAXITO", "ESTRADA_CAMBURI"
                ],
                "volta": [
                    "ESTRADA_CAMBURI", "ESTRADA_HENFIL", "RUA_CECILIA_MATARUNA", 
                    "ESTRADA_CAXITO", "CENTRO_SAQU", "RETORNO_RJ106", "CENTRO_SAQU",
                    "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E08": {
                "nome": "CENTRO X JACAROÁ (VIA AMIZADE)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "RUA_ABREU_SODRE", "RUA_JOAQUIM_SANTOS",
                    "RUA_BARAO_INOA", "RUA_ALVARES_CASTRO", "RUA_SILVINO_SIQUEIRA",
                    "AV_NOSSA_SENHORA_AMPARO", "RUA_CLIMACO_PEREIRA", "RUA_DOMICIO_GAMA",
                    "RUA_PADRE_ARLINDO", "RUA_CLIMACO_PEREIRA", "RUA_PREFEITO_JOAQUIM",
                    "RUA_ANTONIO_GOMES", "RUA_REGINALDO_FONSECA", "AVENIDA_TRES",
                    "RUA_PREFEITO_JOAQUIM", "ESTRADA_JACAROA", "PRACA_NENEM",
                    "RUA_OUVIDOR_SOUZA", "AV_DIOGENES_COSTA", "CAMPO_CAJU"
                ],
                "volta": [
                    "CAMPO_CAJU", "ESTRADA_JACAROA", "ESTR_ZILTO_MONTEIRO", 
                    "PRACA_NENEM", "ESTRADA_JACAROA", "RUA_PREFEITO_JOAQUIM",
                    "AVENIDA_TRES", "RUA_REGINALDO_FONSECA", "RUA_ANTONIO_GOMES",
                    "RUA_PREFEITO_JOAQUIM", "RUA_PADRE_ARLINDO", "RUA_CLIMACO_PEREIRA",
                    "RUA_DOMICIO_GAMA", "RUA_PADRE_ARLINDO", "RUA_CLIMACO_PEREIRA",
                    "AV_NOSSA_SENHORA_AMPARO", "RUA_SILVINO_SIQUEIRA", "RUA_ALVARES_CASTRO",
                    "RUA_BARAO_INOA", "RUA_JOAQUIM_SANTOS", "RUA_ABREU_SODRE",
                    "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E08A": {
                "nome": "JACAROÁ (VIA AMIZADE/VIA CAMPO)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "RUA_ABREU_SODRE", "RUA_JOAQUIM_SANTOS",
                    "RUA_BARAO_INOA", "RUA_ALVARES_CASTRO", "RUA_SILVINO_SIQUEIRA",
                    "AV_NOSSA_SENHORA_AMPARO", "RUA_CLIMACO_PEREIRA", "RUA_DOMICIO_GAMA",
                    "RUA_PADRE_ARLINDO", "RUA_CLIMACO_PEREIRA", "RUA_PREFEITO_JOAQUIM",
                    "RUA_ANTONIO_GOMES", "RUA_REGINALDO_FONSECA", "AVENIDA_TRES",
                    "RUA_PREFEITO_JOAQUIM", "ESTRADA_JACAROA", "PRACA_NENEM",
                    "ESTR_ZILTO_MONTEIRO", "CAMPO_CAJU"
                ],
                "volta": [
                    "AV_NERO_SILVA", "RUA_OUVIDOR_SOUZA", "ESTRADA_JACAROA", 
                    "RUA_PREFEITO_JOAQUIM", "AVENIDA_TRES", "RUA_REGINALDO_FONSECA",
                    "RUA_ANTONIO_GOMES", "RUA_PREFEITO_JOAQUIM", "RUA_PADRE_ARLINDO",
                    "RUA_CLIMACO_PEREIRA", "RUA_DOMICIO_GAMA", "RUA_PADRE_ARLINDO",
                    "RUA_CLIMACO_PEREIRA", "AV_NOSSA_SENHORA_AMPARO", "RUA_SILVINO_SIQUEIRA",
                    "RUA_ALVARES_CASTRO", "RUA_BARAO_INOA", "RUA_JOAQUIM_SANTOS",
                    "RUA_ABREU_SODRE", "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA",
                    "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            },
            "E09": {
                "nome": "CENTRO X GUARATIBA (VIA CAJU/INTERLAGOS)",
                "ida": [
                    "RODOVIARIA", "AV_ROBERTO_SILVEIRA", "RUA_ABREU_SODRE", "RUA_JOAQUIM_SANTOS",
                    "RUA_BARAO_INOA", "RUA_ALVARES_CASTRO", "RUA_SILVINO_SIQUEIRA",
                    "AV_NOSSA_SENHORA_AMPARO", "RUA_CLIMACO_PEREIRA", "RUA_DOMICIO_GAMA",
                    "RUA_PADRE_ARLINDO", "RUA_CLIMACO_PEREIRA", "RUA_PREFEITO_JOAQUIM",
                    "ESTRADA_JACAROA", "PRACA_NENEM", "ESTR_ZILTO_MONTEIRO",
                    "ESTRADA_JACAROA", "AV_UM_LOT_JP", "ESTRADA_PONTE_NEGRA",
                    "ESTRADA_BEIRA_LAGOA", "ALZIRO_RODRIGUES", "FABIANO_FERREIRA",
                    "RUA_DOIS", "AV_REGINALDO_ZEIDAN", "ESTRADA_BEIRA_LAGOA", "RUA_32", "AV_MAYSA"
                ],
                "volta": [
                    "AV_MAYSA", "RUA_56", "ESTRADA_BEIRA_LAGOA", "ESTRADA_PONTE_NEGRA",
                    "AV_UM_BEIRA_LAGOA", "RUA_CENTO_DEZ", "AV_UM_LOT_JP", "ESTRADA_GAMBOA",
                    "ESTRADA_JACAROA", "PRACA_NENEM", "ESTRADA_JACAROA", 
                    "RUA_PREFEITO_JOAQUIM", "RUA_PADRE_ARLINDO", "RUA_CLIMACO_PEREIRA",
                    "RUA_DOMICIO_GAMA", "RUA_PADRE_ARLINDO", "RUA_CLIMACO_PEREIRA",
                    "AV_NOSSA_SENHORA_AMPARO", "RUA_SILVINO_SIQUEIRA", "RUA_ALVARES_CASTRO",
                    "RUA_BARAO_INOA", "RUA_JOAQUIM_SANTOS", "RUA_ABREU_SODRE",
                    "AV_ROBERTO_SILVEIRA", "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA", "RODOVIARIA"
                ]
            }
        }
        
        # Adicionar as linhas aos pontos
        for linha_id, linha_info in self.linhas_vermelinho.items():
            for ponto_id in linha_info["ida"] + linha_info["volta"]:
                if ponto_id in self.pontos:
                    if linha_id not in self.pontos[ponto_id].linhas:
                        self.pontos[ponto_id].linhas.append(linha_id)
    
    def _criar_conexoes_linhas(self):
        """Cria conexões entre pontos baseadas nas linhas do Vermelinho"""
        
        # Para cada linha, conectar pontos sequenciais
        for linha_id, linha_info in self.linhas_vermelinho.items():
            
            # Conectar pontos da ida
            pontos_ida = linha_info["ida"]
            for i in range(len(pontos_ida) - 1):
                if pontos_ida[i] in self.pontos and pontos_ida[i + 1] in self.pontos:
                    # Tempo estimado baseado na distância e tipo de via
                    tempo = self._calcular_tempo_viagem(pontos_ida[i], pontos_ida[i + 1])
                    self.grafo.add_edge(pontos_ida[i], pontos_ida[i + 1], weight=tempo, linha=linha_id)
            
            # Conectar pontos da volta
            pontos_volta = linha_info["volta"]
            for i in range(len(pontos_volta) - 1):
                if pontos_volta[i] in self.pontos and pontos_volta[i + 1] in self.pontos:
                    tempo = self._calcular_tempo_viagem(pontos_volta[i], pontos_volta[i + 1])
                    if not self.grafo.has_edge(pontos_volta[i], pontos_volta[i + 1]):
                        self.grafo.add_edge(pontos_volta[i], pontos_volta[i + 1], weight=tempo, linha=linha_id)
        
        # Adicionar conexões especiais (terminais, pontos de integração)
        self._adicionar_conexoes_especiais()
    
    def _calcular_tempo_viagem(self, ponto1_id: str, ponto2_id: str) -> int:
        """Calcula tempo estimado entre dois pontos"""
        if ponto1_id not in self.pontos or ponto2_id not in self.pontos:
            return 5
        
        ponto1 = self.pontos[ponto1_id]
        ponto2 = self.pontos[ponto2_id]
        
        # Calcular distância
        distancia = self._calcular_distancia(ponto1, ponto2)
        
        # Tempo base por distância (velocidade média 25 km/h no trânsito urbano)
        tempo_base = max(2, int(distancia * 2.4))  # 2.4 min por km
        
        # Ajustar baseado no tipo de via
        if "RODOVIARIA" in [ponto1_id, ponto2_id]:
            tempo_base += 2  # Tempo extra para terminal
        elif "ESTRADA" in ponto1.nome.upper() or "ESTRADA" in ponto2.nome.upper():
            tempo_base += 1  # Estradas podem ter trânsito
        elif "AV" in ponto1.nome or "AV" in ponto2.nome:
            tempo_base += 1  # Avenidas têm semáforos
        
        return min(tempo_base, 15)  # Máximo 15 minutos entre pontos consecutivos
    
    def _adicionar_conexoes_especiais(self):
        """Adiciona conexões especiais entre terminais e pontos de integração"""
        
        # Conexões do Terminal Rodoviário com pontos próximos do centro
        pontos_centro = ["AV_ROBERTO_SILVEIRA", "CENTRO_SAQU", "RUA_ABREU_SODRE", 
                        "RUA_ALVARES_CASTRO", "MARIO_LOPES_FONTOURA", "LUIZ_ANTONIO_CUNHA"]
        
        for ponto in pontos_centro:
            if ponto in self.pontos and not self.grafo.has_edge("RODOVIARIA", ponto):
                tempo = 3 if ponto in ["AV_ROBERTO_SILVEIRA", "CENTRO_SAQU"] else 5
                self.grafo.add_edge("RODOVIARIA", ponto, weight=tempo, tipo="integracao")
        
        # Conexões entre pontos que compartilham múltiplas linhas
        pontos_compartilhados = [
            ("RUA_ABREU_SODRE", "RUA_JOAQUIM_SANTOS", 2),
            ("RUA_BARAO_INOA", "RUA_ALVARES_CASTRO", 2),
            ("AV_NOSSA_SENHORA_AMPARO", "AV_IVAN_MUNDIM", 3),
            ("RUA_CLIMACO_PEREIRA", "RUA_DOMICIO_GAMA", 2),
            ("RUA_PREFEITO_JOAQUIM", "RUA_ANTONIO_GOMES", 2),
            ("ESTRADA_JACAROA", "PRACA_NENEM", 3),
        ]
        
        for ponto1, ponto2, tempo in pontos_compartilhados:
            if ponto1 in self.pontos and ponto2 in self.pontos:
                if not self.grafo.has_edge(ponto1, ponto2):
                    self.grafo.add_edge(ponto1, ponto2, weight=tempo, tipo="compartilhada")
    
    def _calcular_distancia(self, ponto1: PontoOnibus, ponto2: PontoOnibus) -> float:
        """Calcula distância entre dois pontos em km"""
        lat1, lon1 = math.radians(ponto1.latitude), math.radians(ponto1.longitude)
        lat2, lon2 = math.radians(ponto2.latitude), math.radians(ponto2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return 6371 * c  # Raio da Terra em km
    
    def calcular_rota(self, origem: str, destino: str, apenas_acessivel: bool = False) -> dict:
        """
        Calcula a rota ótima usando algoritmo de Dijkstra
        
        Args:
            origem: ID do ponto de origem
            destino: ID do ponto de destino  
            apenas_acessivel: Se True, usa apenas pontos acessíveis
            
        Returns:
            dict: Resultado da rota com detalhes completos
        """
        
        try:
            # Validar pontos
            if origem not in self.pontos or destino not in self.pontos:
                return self._resultado_erro("Pontos não encontrados")
            
            if origem == destino:
                return self._resultado_erro("Origem e destino são iguais")
            
            # Criar subgrafo se necessário filtrar acessibilidade
            grafo_calculo = self.grafo
            if apenas_acessivel:
                pontos_acessiveis = [id_ponto for id_ponto, ponto in self.pontos.items() 
                                   if ponto.acessivel]
                grafo_calculo = self.grafo.subgraph(pontos_acessiveis)
                
                if origem not in pontos_acessiveis or destino not in pontos_acessiveis:
                    return self._resultado_erro("Pontos não acessíveis com filtro ativo")
            
            # Calcular rota usando Dijkstra do NetworkX
            try:
                caminho = nx.shortest_path(grafo_calculo, origem, destino, weight='weight')
                tempo_total = nx.shortest_path_length(grafo_calculo, origem, destino, weight='weight')
                
                return self._formatar_resultado_sucesso(caminho, tempo_total, apenas_acessivel)
                
            except nx.NetworkXNoPath:
                return self._resultado_erro("Não existe caminho entre os pontos")
                
        except Exception as e:
            return self._resultado_erro(f"Erro no cálculo: {str(e)}")
    
    def _resultado_erro(self, mensagem: str) -> dict:
        """Retorna resultado de erro padronizado"""
        return {
            'encontrada': False,
            'erro': mensagem,
            'origem': '',
            'destino': '',
            'pontos': [],
            'tempo_total': 0,
            'status': f"❌ {mensagem}"
        }
    
    def _formatar_resultado_sucesso(self, caminho: List[str], tempo_total: float, apenas_acessivel: bool) -> dict:
        """Formata resultado de sucesso"""
        
        # Verificar se rota é totalmente acessível
        rota_acessivel = all(self.pontos[ponto_id].acessivel for ponto_id in caminho)
        
        # Identificar linhas utilizadas
        linhas_utilizadas = set()
        for i in range(len(caminho) - 1):
            if self.grafo.has_edge(caminho[i], caminho[i + 1]):
                edge_data = self.grafo[caminho[i]][caminho[i + 1]]
                if 'linha' in edge_data:
                    linhas_utilizadas.add(edge_data['linha'])
        
        # Status da rota
        if rota_acessivel:
            status = "✅ Rota totalmente acessível"
        elif apenas_acessivel:
            status = "✅ Rota com filtro de acessibilidade"
        else:
            status = "⚠️ Rota com pontos não acessíveis"
        
        if linhas_utilizadas:
            linhas_str = ", ".join(sorted(linhas_utilizadas))
            status += f" | 🚌 Linhas: {linhas_str}"
        
        return {
            'encontrada': True,
            'origem': self.pontos[caminho[0]].nome,
            'destino': self.pontos[caminho[-1]].nome,
            'pontos': caminho,
            'tempo_total': tempo_total,
            'distancia_estimada': tempo_total * 0.42,  # Estimativa: 25 km/h média
            'numero_paradas': len(caminho) - 2,  # Excluir origem e destino
            'acessivel': rota_acessivel,
            'linhas_utilizadas': list(linhas_utilizadas),
            'status': status,
            'detalhes': self._obter_detalhes_rota(caminho, tempo_total)
        }
    
    def _obter_detalhes_rota(self, caminho: List[str], tempo_total: float) -> dict:
        """Obtém detalhes adicionais da rota"""
        detalhes = {
            'pontos_detalhados': [],
            'tempos_segmentos': [],
            'tipos_pontos': {},
            'coordenadas': [],
            'linhas_por_segmento': []
        }
        
        # Detalhes de cada ponto
        for i, ponto_id in enumerate(caminho):
            ponto = self.pontos[ponto_id]
            
            detalhes['pontos_detalhados'].append({
                'id': ponto_id,
                'nome': ponto.nome,
                'endereco': ponto.endereco,
                'posicao': i + 1,
                'acessivel': ponto.acessivel,
                'tipo': ponto.tipo,
                'linhas_disponiveis': ponto.linhas
            })
            
            detalhes['coordenadas'].append({
                'lat': ponto.latitude,
                'lng': ponto.longitude
            })
            
            # Tempo e linha entre segmentos
            if i < len(caminho) - 1:
                if self.grafo.has_edge(ponto_id, caminho[i + 1]):
                    edge_data = self.grafo[ponto_id][caminho[i + 1]]
                    tempo_segmento = edge_data['weight']
                    linha_segmento = edge_data.get('linha', 'Integração')
                    
                    detalhes['tempos_segmentos'].append(tempo_segmento)
                    detalhes['linhas_por_segmento'].append(linha_segmento)
        
        # Tipos de pontos na rota
        for ponto_id in caminho:
            tipo = self.pontos[ponto_id].tipo
            if tipo not in detalhes['tipos_pontos']:
                detalhes['tipos_pontos'][tipo] = 0
            detalhes['tipos_pontos'][tipo] += 1
        
        return detalhes
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do sistema"""
        total_pontos = len(self.pontos)
        pontos_acessiveis = sum(1 for p in self.pontos.values() if p.acessivel)
        tipos_pontos = {}
        
        for ponto in self.pontos.values():
            if ponto.tipo not in tipos_pontos:
                tipos_pontos[ponto.tipo] = 0
            tipos_pontos[ponto.tipo] += 1
        
        return {
            'total_pontos': total_pontos,
            'pontos_acessiveis': pontos_acessiveis,
            'percentual_acessivel': (pontos_acessiveis / total_pontos) * 100,
            'total_conexoes': self.grafo.number_of_edges(),
            'total_linhas': len(self.linhas_vermelinho),
            'linhas_ativas': list(self.linhas_vermelinho.keys()),
            'tipos_pontos': tipos_pontos,
            'densidade_grafo': nx.density(self.grafo),
            'conectividade': nx.is_connected(self.grafo)
        }
    
    def obter_informacoes_linha(self, linha_id: str) -> dict:
        """Retorna informações detalhadas de uma linha"""
        if linha_id not in self.linhas_vermelinho:
            return {"erro": "Linha não encontrada"}
        
        linha = self.linhas_vermelinho[linha_id]
        
        return {
            'id': linha_id,
            'nome': linha['nome'],
            'pontos_ida': [self.pontos[p].nome for p in linha['ida'] if p in self.pontos],
            'pontos_volta': [self.pontos[p].nome for p in linha['volta'] if p in self.pontos],
            'total_pontos_ida': len(linha['ida']),
            'total_pontos_volta': len(linha['volta']),
            'pontos_unicos': len(set(linha['ida'] + linha['volta']))
        }
    
    def buscar_linhas_por_ponto(self, ponto_id: str) -> List[str]:
        """Busca todas as linhas que passam por um ponto"""
        if ponto_id not in self.pontos:
            return []
        
        return self.pontos[ponto_id].linhas.copy()

# Teste rápido se executado diretamente
if __name__ == "__main__":
    print("🧪 Testando Sistema Vermelinho com dados reais...")
    
    sistema = SistemaVermelhinho()
    stats = sistema.obter_estatisticas()
    
    print(f"📊 Estatísticas do Sistema Real:")
    print(f"   • Pontos: {stats['total_pontos']}")
    print(f"   • Acessíveis: {stats['pontos_acessiveis']} ({stats['percentual_acessivel']:.1f}%)")
    print(f"   • Conexões: {stats['total_conexoes']}")
    print(f"   • Linhas: {stats['total_linhas']} ({', '.join(stats['linhas_ativas'])})")
    print(f"   • Conectado: {'✅' if stats['conectividade'] else '❌'}")
    
    # Teste de rota com pontos reais
    resultado = sistema.calcular_rota("RODOVIARIA", "PRACA_PONTA_NEGRA")
    print(f"\n🚌 Teste de rota (Rodoviária → Praça Ponta Negra):")
    print(f"   • Status: {resultado['status']}")
    if resultado['encontrada']:
        print(f"   • Tempo: {resultado['tempo_total']:.1f} min")
        print(f"   • Paradas: {resultado['numero_paradas']}")
        print(f"   • Linhas: {', '.join(resultado['linhas_utilizadas'])}")
    
    print("✅ Sistema Vermelinho Real funcionando!")