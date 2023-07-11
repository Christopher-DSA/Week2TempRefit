import re

class QueryBuilder:
    def __init__(self):
        self.query = ""
        self.where_used = False
        self.select_used = False

    def select(self, column: str, table: str):
        if self.select_used:
            raise Exception("Cannot use 'select' method multiple times.")

        self.query += f"SELECT {column} FROM {table}"
        return self

    def insert_into(self, table: str, values: str):
        if self.query:
            raise Exception("Cannot use 'insert_into' method after any other query methods.")

        self.query += f"INSERT INTO {table} VALUES ({', '.join(str(v) for v in values)})"
        return self

    def update(self, table: str):
        if self.query:
            raise Exception("Cannot use 'update' method after any other query methods.")

        self.query += f"UPDATE {table} "
        return self

    def set(self, column: str, value: str):
        if not self.query.startswith("UPDATE"):
            raise Exception("Must call 'update' method before using 'set' method.")

        self.query += f"SET {column} = {value} "
        return self

    def delete_from(self, table):
        if self.query:
            raise Exception("Cannot use 'delete_from' method after any other query methods.")

        self.query += f"DELETE FROM {table} "
        return self

    def join(self, table, condition):
        if not self.query.startswith("SELECT"):
            raise Exception("Must call 'select' method before using 'join' method.")

        self.query += f"JOIN {table} ON {condition}"
        return self

    def where(self, condition):
        if self.where_used:
            raise Exception("Cannot use 'where' method multiple times in the same query.")

        self.query += f"WHERE {condition} "
        self.where_used = True
        return self

    def and_(self, condition):
        if not self.where_used:
            raise Exception("Cannot use 'and_' method before 'where' method.")

        self.query += f"AND {condition} "
        return self

    def or_(self, condition):
        if not self.where_used:
            raise Exception("Cannot use 'or_' method before 'where' method.")

        self.query += f"OR {condition} "
        return self

    def order_by(self, column):
        self.query += f"ORDER BY {column} "
        return self

    def limit(self, limit):
        self.query += f"LIMIT {limit} "
        return self

    def count(self, table: str):
        if self.select_used:
            raise Exception("Cannot use 'count' method with 'select' method.")

        self.query = f"SELECT COUNT(*) { self.query[self.query.index('FROM'):] } "
        self.select_used = True

    def sum(self, column):
        if self.select_used:
            raise Exception("Cannot use 'sum' method with 'select' method.")

        self.query = f"SELECT SUM ({column}) {self.query[self.query.index('FROM'):]} "
        self.select_used = True
        return self

    def avg(self, column):
        if self.select_used:
            raise Exception("Cannot use 'avg' method with 'select' method.")

        self.query = f"SELECT AVG({column}) {self.query[self.query.index('FROM')]} "
        self.select_used = True
        return self

    def min(self, column):
        if self.select_used:
            raise Exception("Cannot use 'min' method with 'select' method.")

        self.query = f"SELECT MIN({column}) {self.query[self.query.index('FROM'):]} "
        self.select_used = True
        return self

    def max(self, column):
        if self.select_used:
            raise Exception("Cannot use 'max' method with 'select' method.")

        self.query = f"SELECT MAX({column}) {self.query[self.query.index('FROM'):]} "
        self.select_used = True

    def remove(self):
        if self.select_used:
            raise Exception("Cannot use 'remove' method with 'select' method.")

        self.query += f"DELETE {self.query[self.query.index('FROM'):]} "
        self.select_used = True
        return self

    def build(self):
        if self.query[-1] == " ":
            self.query = self.query[:-1] + ";"
        else:
            self.query += ";"
        return self.query