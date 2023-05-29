from typing import Any, Optional
import sqlite3
from langchain.memory.entity import BaseEntityStore

# while waiting for https://github.com/hwchase17/langchain/pull/5129 to be merged
class EntitySqliteMemory(BaseEntityStore):
    """SQLite-backed Entity store"""

    session_id: str = "default"
    table_name: str = "memory_store"

    def __init__(
        self,
        session_id: str = "default",
        db_file: str = "entities.db",
        table_name: str = "memory_store",
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)

        self.conn = sqlite3.connect(db_file)
        self.session_id = session_id
        self.table_name = table_name
        self._create_table_if_not_exists()

    @property
    def full_table_name(self) -> str:
        return f"{self.table_name}_{self.session_id}"

    def _create_table_if_not_exists(self) -> None:
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.full_table_name} (
                key TEXT PRIMARY KEY,
                value TEXT,
                expiration INTEGER
            )
        """
        with self.conn:
            self.conn.execute(create_table_query)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        query = f"""
            SELECT value
            FROM {self.full_table_name}
            WHERE key = ? AND expiration >= strftime('%s', 'now')
        """
        cursor = self.conn.execute(query, (key))
        result = cursor.fetchone()
        if result is not None:
            value = result[0]
            self._extend_expiration(key)
            return value
        return default

    def set(self, key: str, value: Optional[str]) -> None:
        if not value:
            return self.delete(key)
        query = f"""
            INSERT OR REPLACE INTO {self.full_table_name} (key, value, expiration)
            VALUES (?, ?, strftime('%s', 'now') + ?)
        """
        with self.conn:
            self.conn.execute(query, (key, value))

    def delete(self, key: str) -> None:
        query = f"""
            DELETE FROM {self.full_table_name}
            WHERE key = ?
        """
        with self.conn:
            self.conn.execute(query, (key,))

    def exists(self, key: str) -> bool:
        query = f"""
            SELECT 1
            FROM {self.full_table_name}
            WHERE key = ? AND expiration >= strftime('%s', 'now')
            LIMIT 1
        """
        cursor = self.conn.execute(query, (key,))
        result = cursor.fetchone()
        return result is not None

    def clear(self) -> None:
        query = f"""
            DELETE FROM {self.full_table_name}
        """
        with self.conn:
            self.conn.execute(query)

    def _extend_expiration(self, key: str) -> None:
        query = f"""
            UPDATE {self.full_table_name}
            SET expiration = strftime('%s', 'now') + ?
            WHERE key = ?
        """
        with self.conn:
            self.conn.execute(query, (key))
