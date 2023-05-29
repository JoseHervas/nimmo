import os
import sqlite3
import tempfile
import time
from datetime import datetime, timedelta
import atexit

class TempFolder:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.temp_folder = "tmp"
        os.makedirs(self.temp_folder, exist_ok=True)
        self.file_timestamps = 60 * 60 # seconds
        self.db_conn = sqlite3.connect(":memory:")
        self._create_table()
        self._start_cleanup_cron()

    def _create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS files (name TEXT PRIMARY KEY, lifespan INTEGER)")
        self.db_conn.commit()

    def _start_cleanup_cron(self):
        atexit.register(self._cleanup)

    def _cleanup(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT name FROM files WHERE lifespan < ?", (int(time.time()),))
        expired_files = cursor.fetchall()

        for file in expired_files:
            file_path = os.path.join(self.temp_folder, file[0])
            if os.path.isfile(file_path):
                os.remove(file_path)

        cursor.execute("DELETE FROM files WHERE lifespan < ?", (int(time.time()),))
        self.db_conn.commit()

    def create_file(self, name, content):
        file_path = os.path.join(self.temp_folder, name)
        with open(file_path, "w") as file:
            file.write(content)

        cursor = self.db_conn.cursor()
        cursor.execute("INSERT INTO files (name, lifespan) VALUES (?, ?)", (name, int(time.time()) + self.file_timestamps))
        self.db_conn.commit()

    def list_files(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT name FROM files")
        files = cursor.fetchall()
        return [file[0] for file in files]

    def read_file(self, name):
        file_path = os.path.join(self.temp_folder, name)
        with open(file_path, "r") as file:
            content = file.read()

        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE files SET lifespan = ? WHERE name = ?", (int(time.time()) + self.file_timestamps, name))
        self.db_conn.commit()

        return content
