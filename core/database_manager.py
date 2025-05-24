import sqlite3
from typing import Any, List, Optional, Tuple, Dict


class DatabaseManager:
    def __init__(self, db_name: str = '../oficina_db/oficina_manutencoes.db') -> None:
        self.db_name = db_name

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        if params is None:
            params = ()
        with self.connect() as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict]:
        if params is None:
            params = ()
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Dict[str, Any]:
        if params is None:
            params = ()
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else {}
        
    def fetch_exists(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> bool:
        if params is None:
            params = ()
        with self.connect() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone() is not None