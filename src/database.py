import sqlite3
from pathlib import Path


class Database:
    def __init__(self):

        # Database access
        self.path = self.get_path()
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

        # Database setup
        self.set_table()

    @staticmethod
    def get_path() -> Path:  # --------------------------------------

        # Chemins supposés
        directory = Path().home() / "AppData" / "Local" / "sprite-task"
        file = directory / "tasks.db"

        # le dossier n'existe pas
        if not directory.exists():
            directory.mkdir()

        # la base de donnée n'existe pas
        if not file.exists():
            file.touch()

        return directory / file

    def set_table(self):  # -----------------------------------------
        sql_table = """
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY,
            fini BLOB NOT NULL,
            nom TEXT,
            description TEXT,
            difficulte INTEGER,
            longueur INTEGER
        );
        """
        self.cursor.execute(sql_table)
        self.connection.commit()

    def insert_task(self, task: dict):  # ---------------------------
        if "id" in task.keys():
            self.update_task(task)
        else:
            self.add_task(task)

    def add_task(self, task: dict):  # ------------------------------
        sql = f"""
        INSERT INTO Tasks (fini, nom, description, difficulte, longueur)
        VALUES (?, ?, ?, ?, ?);
        """

        values = (
            int(task["fini"]),
            task["nom"],
            task["description"],
            task["difficulte"],
            task["longueur"]
        )

        self.cursor.execute(sql, values)
        self.connection.commit()

    def update_task(self, task: dict):  # ---------------------------
        sql = """
        UPDATE Tasks SET
            fini = ?,
            nom = ?,
            description = ?,
            difficulte = ?,
            longueur = ?
        WHERE id = ?;
        """

        values = (
            int(task["fini"]),
            task["nom"],
            task["description"],
            task["difficulte"],
            task["longueur"],
            task["id"]
        )

        self.cursor.execute(sql, values)
        self.connection.commit()

    def rm_task(self, task):  # -------------------------------------
        sql = """
        DELETE FROM Tasks WHERE id = ?;
        """

        self.cursor.execute(sql, (task["id"],))
        self.connection.commit()

    def select(self, conditions: dict) -> list:  # --------
        sql = """
        SELECT * FROM Tasks WHERE
            fini = ?
            AND difficulte >= ?
            AND difficulte <= ?
            AND longueur >= ?
            AND longueur <= ?
        ;
        """

        values = (
            conditions["fini"],
            conditions["diff_min"],
            conditions["diff_max"],
            conditions["long_min"],
            conditions["long_max"]
        )

        self.cursor.execute(sql, values)
        format_data = self.get_data_as_dict(self.cursor.fetchall())

        return format_data

    @staticmethod
    def get_data_as_dict(data: list[tuple]) -> list[dict]:  # -------
        res = []

        for task in data:
            tmp_dict = {
                "id": task[0],
                "fini": bool(task[1]),
                "nom": task[2],
                "description": task[3],
                "difficulte": task[4],
                "longueur": task[5]
            }
            res.append(tmp_dict)

        return res

    def close(self):  # ---------------------------------------------
        self.connection.close()
