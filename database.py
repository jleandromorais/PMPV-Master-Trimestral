# -*- coding: utf-8 -*-
"""
Módulo de Banco de Dados SQLite para a Calculadora PMPV
Permite salvar e carregar dados entre sessões
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional


class DatabasePMPV:
    """Gerenciador de banco de dados para o sistema PMPV"""
    
    def __init__(self, db_path: str = "pmpv_data.db"):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._conectar()
        self._criar_tabelas()
    
    def _conectar(self):
        """Estabelece conexão com o banco de dados"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # Permite acessar colunas por nome
        self.conn.row_factory = sqlite3.Row
    
    def _criar_tabelas(self):
        """Cria as tabelas necessárias se não existirem"""
        
        # Tabela de sessões (trimestres salvos)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                observacoes TEXT
            )
        """)
        
        # Tabela de dados por mês
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dados_mes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER NOT NULL,
                mes INTEGER NOT NULL,  -- 1, 2 ou 3
                empresa TEXT NOT NULL,
                molecula REAL,
                transporte REAL,
                logistica REAL,
                volume REAL,
                FOREIGN KEY (sessao_id) REFERENCES sessoes (id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de resultados calculados
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id INTEGER NOT NULL,
                volume_total REAL,
                pmpv_trimestral REAL,
                custo_total REAL,
                data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sessao_id) REFERENCES sessoes (id) ON DELETE CASCADE
            )
        """)
        
        self.conn.commit()
    
    def criar_sessao(self, nome: str, observacoes: str = "") -> int:
        """
        Cria uma nova sessão (trimestre).
        
        Args:
            nome: Nome da sessão (ex: "Trimestre Q1 2026")
            observacoes: Observações opcionais
            
        Returns:
            ID da sessão criada
        """
        self.cursor.execute(
            "INSERT INTO sessoes (nome, observacoes) VALUES (?, ?)",
            (nome, observacoes)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def salvar_dados_mes(self, sessao_id: int, mes: int, dados: List[Dict]) -> bool:
        """
        Salva os dados de um mês específico.
        
        Args:
            sessao_id: ID da sessão
            mes: Número do mês (1, 2 ou 3)
            dados: Lista de dicionários com os dados das empresas
            
        Returns:
            True se salvou com sucesso
        """
        try:
            # Remove dados anteriores deste mês
            self.cursor.execute(
                "DELETE FROM dados_mes WHERE sessao_id = ? AND mes = ?",
                (sessao_id, mes)
            )
            
            # Insere novos dados
            for linha in dados:
                self.cursor.execute("""
                    INSERT INTO dados_mes 
                    (sessao_id, mes, empresa, molecula, transporte, logistica, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    sessao_id,
                    mes,
                    linha.get('empresa', ''),
                    linha.get('molecula', 0.0),
                    linha.get('transporte', 0.0),
                    linha.get('logistica', 0.0),
                    linha.get('volume', 0.0)
                ))
            
            # Atualiza data de modificação
            self.cursor.execute(
                "UPDATE sessoes SET data_modificacao = CURRENT_TIMESTAMP WHERE id = ?",
                (sessao_id,)
            )
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            self.conn.rollback()
            return False
    
    def carregar_dados_mes(self, sessao_id: int, mes: int) -> List[Dict]:
        """
        Carrega os dados de um mês específico.
        
        Args:
            sessao_id: ID da sessão
            mes: Número do mês (1, 2 ou 3)
            
        Returns:
            Lista de dicionários com os dados
        """
        self.cursor.execute("""
            SELECT empresa, molecula, transporte, logistica, volume
            FROM dados_mes
            WHERE sessao_id = ? AND mes = ?
            ORDER BY id
        """, (sessao_id, mes))
        
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def salvar_resultado(self, sessao_id: int, volume_total: float, 
                        pmpv: float, custo_total: float) -> bool:
        """
        Salva o resultado do cálculo trimestral.
        
        Args:
            sessao_id: ID da sessão
            volume_total: Volume total calculado
            pmpv: PMPV calculado
            custo_total: Custo total calculado
            
        Returns:
            True se salvou com sucesso
        """
        try:
            self.cursor.execute("""
                INSERT INTO resultados 
                (sessao_id, volume_total, pmpv_trimestral, custo_total)
                VALUES (?, ?, ?, ?)
            """, (sessao_id, volume_total, pmpv, custo_total))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")
            return False
    
    def listar_sessoes(self) -> List[Dict]:
        """
        Lista todas as sessões salvas.
        
        Returns:
            Lista de dicionários com informações das sessões
        """
        self.cursor.execute("""
            SELECT s.id, s.nome, s.data_criacao, s.data_modificacao, s.observacoes,
                   r.volume_total, r.pmpv_trimestral, r.custo_total
            FROM sessoes s
            LEFT JOIN resultados r ON s.id = r.sessao_id
            ORDER BY s.data_modificacao DESC
        """)
        
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def deletar_sessao(self, sessao_id: int) -> bool:
        """
        Deleta uma sessão e todos os seus dados.
        
        Args:
            sessao_id: ID da sessão a deletar
            
        Returns:
            True se deletou com sucesso
        """
        try:
            self.cursor.execute("DELETE FROM sessoes WHERE id = ?", (sessao_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar sessão: {e}")
            return False
    
    def exportar_para_dict(self, sessao_id: int) -> Dict:
        """
        Exporta todos os dados de uma sessão para um dicionário.
        Útil para exportar para JSON ou Excel.
        
        Args:
            sessao_id: ID da sessão
            
        Returns:
            Dicionário com todos os dados
        """
        # Informações da sessão
        self.cursor.execute("SELECT * FROM sessoes WHERE id = ?", (sessao_id,))
        sessao = dict(self.cursor.fetchone())
        
        # Dados dos 3 meses
        dados_meses = {}
        for mes in [1, 2, 3]:
            dados_meses[f"mes_{mes}"] = self.carregar_dados_mes(sessao_id, mes)
        
        # Resultado
        self.cursor.execute(
            "SELECT * FROM resultados WHERE sessao_id = ? ORDER BY data_calculo DESC LIMIT 1",
            (sessao_id,)
        )
        resultado_row = self.cursor.fetchone()
        resultado = dict(resultado_row) if resultado_row else None
        
        return {
            'sessao': sessao,
            'dados': dados_meses,
            'resultado': resultado
        }
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destrutor - garante que a conexão seja fechada"""
        self.fechar()


# Funções auxiliares para facilitar o uso

def criar_backup(db_path: str = "pmpv_data.db", backup_path: str = None):
    """
    Cria um backup do banco de dados.
    
    Args:
        db_path: Caminho do banco original
        backup_path: Caminho do backup (se None, usa timestamp)
    """
    import shutil
    
    if backup_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"pmpv_backup_{timestamp}.db"
    
    shutil.copy2(db_path, backup_path)
    print(f"Backup criado: {backup_path}")
    return backup_path


# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    db = DatabasePMPV("teste_pmpv.db")
    
    # Criar uma sessão
    sessao_id = db.criar_sessao("Teste Trimestre Q1", "Dados de teste")
    print(f"Sessão criada: {sessao_id}")
    
    # Salvar dados do Mês 1
    dados_mes1 = [
        {'empresa': 'Fornecedor 1', 'molecula': 10.50, 'transporte': 0.50, 'logistica': 0.30, 'volume': 100000},
        {'empresa': 'Fornecedor 2', 'molecula': 11.20, 'transporte': 0.45, 'logistica': 0.25, 'volume': 80000},
    ]
    db.salvar_dados_mes(sessao_id, 1, dados_mes1)
    print("Dados do Mês 1 salvos!")
    
    # Carregar dados
    dados_carregados = db.carregar_dados_mes(sessao_id, 1)
    print(f"Dados carregados: {dados_carregados}")
    
    # Listar sessões
    sessoes = db.listar_sessoes()
    print(f"Sessões: {sessoes}")
    
    db.fechar()
    print("Teste concluído!")
