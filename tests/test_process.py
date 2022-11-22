from src.VendorDB import VendorDatabase, create_database
from src.config import VENDOR_DATABASE_CONFIG
from sqlite_utils import Database
import pytest

def test_memory_db():
    db = create_database(True)
    assert isinstance(db, Database)

def test_db_creation(): 
    db = VendorDatabase()
    db.insert_transaction(
        {
            "id": "Youtube",
            "duration": 200
        }
    )
    assert db.get_vendor(vendor_id='Youtube') is not None