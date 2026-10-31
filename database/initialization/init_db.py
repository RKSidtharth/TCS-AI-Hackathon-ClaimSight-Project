"""
CLAIMSIGHT AI - Database Initialization Entry Point
Initializes MongoDB indexes and seeds demonstration scenarios across all 22 collections.
"""

import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, DB_DIR)

from indexes.setup_indexes import create_all_indexes
from seed.seed_data import seed_database

def initialize():
    print("==================================================")
    print("      CLAIMSIGHT AI - DATABASE INITIALIZATION      ")
    print("==================================================")
    create_all_indexes()
    print("--------------------------------------------------")
    seed_database()
    print("==================================================")
    print("   DATABASE INITIALIZATION COMPLETED SUCCESSFULLY  ")
    print("==================================================")

if __name__ == "__main__":
    initialize()

