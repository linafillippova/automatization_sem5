from sqlalchemy import create_engine, inspect

def get_schema(path):
    engine = create_engine(f"sqlite:///{path}")
    inspector = inspect(engine)
    schema = {}

    for table in inspector.get_table_names():
        columns = inspector.get_columns(table)
        col_info = [(col["name"], str(col["type"])) for col in columns]
        schema[table] = sorted(col_info)

    return schema

db1 = "app1.db"   # локальная база с ВМ1
db2 = "app2.db"   # база, скопированная с ВМ2

schema1 = get_schema(db1)
schema2 = get_schema(db2)

if schema1 == schema2:
    print("✔ Схемы полностью совпадают.")
    exit(0)
else:
    print("❌ Схемы отличаются!")
    print("\n--- ВМ1 ---")
    print(schema1)
    print("\n--- ВМ2 ---")
    print(schema2)
    exit(1)
