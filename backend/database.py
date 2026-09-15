"""
backend/database.py

Local SQLite database for the Inuka prototype.

This module is responsible for:
1. Creating the SQLite database.
2. Creating required tables.
3. Saving inventory records.
4. Saving replenishment decisions.
5. Reading inventory and decision records.
"""

import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# DATABASE LOCATION
# ---------------------------------------------------------

# Store the SQLite database inside the backend folder.
DATABASE_PATH = Path(__file__).resolve().parent / "inuka.db"


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

def get_connection():
    """
    Open a connection to the SQLite database.

    row_factory=sqlite3.Row allows us to access database
    columns by their names and easily convert rows to dictionaries.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------

def initialize_database():
    """
    Create the required database tables if they do not exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # -------------------------------------------------
        # INVENTORY TABLE
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                depot TEXT NOT NULL,
                product TEXT NOT NULL,
                current_stock_m3 REAL NOT NULL,
                average_daily_demand_m3 REAL NOT NULL,
                tank_capacity_m3 REAL NOT NULL
            )
        """)

        # -------------------------------------------------
        # REPLENISHMENT DECISIONS TABLE
        # -------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS replenishment_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                depot TEXT NOT NULL,
                product TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                recommended_volume_m3 REAL NOT NULL,
                replenishment_method TEXT NOT NULL,
                dispatch_priority TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


# ---------------------------------------------------------
# INVENTORY FUNCTIONS
# ---------------------------------------------------------

def get_inventory():
    """
    Return all inventory records.

    Records are ordered by depot and product.
    """

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT *
            FROM inventory
            ORDER BY depot, product
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def save_inventory(item: dict):
    """
    Save one inventory record.
    """

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO inventory (
                depot,
                product,
                current_stock_m3,
                average_daily_demand_m3,
                tank_capacity_m3
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                item["depot"],
                item["product"],
                item["current_stock_m3"],
                item["average_daily_demand_m3"],
                item["tank_capacity_m3"],
            ),
        )

        connection.commit()

    finally:
        connection.close()


# ---------------------------------------------------------
# DECISION FUNCTIONS
# ---------------------------------------------------------

def save_decision(decision: dict):
    """
    Save a simulated replenishment decision.

    IMPORTANT:
    The field names here match the output produced by
    decision_engine.engine.make_inventory_decision().
    """

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO replenishment_decisions (
                depot,
                product,
                risk_level,
                recommended_volume_m3,
                replenishment_method,
                dispatch_priority
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                decision["depot"],
                decision["product"],
                decision["risk_level"],
                decision["recommended_volume_m3"],
                decision["preferred_mode"],
                decision["priority"],
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_decisions():
    """
    Return all saved replenishment decisions.

    Newest decisions are returned first.
    """

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT *
            FROM replenishment_decisions
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()
