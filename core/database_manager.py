import sqlite3
from typing import Any, List, Optional, Tuple


class DatabaseManager:
    def __init__(self, db_name: str = "manutencaoOficina.db") -> None:
        self.db_name = db_name

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        if params is None:
            params = ()
        with self.connect() as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple]:
        if params is None:
            params = ()
        with self.connect() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Tuple]:
        if params is None:
            params = ()
        with self.connect() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()