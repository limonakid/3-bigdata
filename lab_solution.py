import os
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST', 'localhost')
POSTGRESQL_PORT = int(os.getenv('POSTGRESQL_PORT', '5433'))
POSTGRESQL_DB = os.getenv('POSTGRESQL_DB', 'demo')
POSTGRESQL_USER = os.getenv('POSTGRESQL_USER', 'demo')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD', 'demo')


def get_conn():
    return psycopg2.connect(
        dbname=POSTGRESQL_DB,
        user=POSTGRESQL_USER,
        password=POSTGRESQL_PASSWORD,
        host=POSTGRESQL_HOST,
        port=POSTGRESQL_PORT,
    )


def query_df(sql: str):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('SET search_path TO bookings, public;')
            cur.execute(sql)
            if cur.description is None:
                return pd.DataFrame()
            rows = cur.fetchall()
            if not rows:
                return pd.DataFrame(columns=[desc[0] for desc in cur.description])
            return pd.DataFrame([dict(r) for r in rows])


queries = {
    'Первые 5 мест': 'SELECT * FROM seats LIMIT 5;',
    'Тарифы': '''
        SELECT DISTINCT fare_conditions
        FROM ticket_flights
        ORDER BY fare_conditions;
    ''',
    'Выручка по тарифам': '''
        SELECT fare_conditions, SUM(amount) AS total_revenue
        FROM ticket_flights
        GROUP BY fare_conditions
        ORDER BY total_revenue DESC;
    ''',
    'Максимальный доход по тарифу': '''
        SELECT fare_conditions, SUM(amount) AS total_revenue
        FROM ticket_flights
        GROUP BY fare_conditions
        ORDER BY total_revenue DESC
        LIMIT 1;
    ''',
    'Самый дорогой перелет': '''
        WITH flight_revenue AS (
            SELECT tf.flight_id, SUM(tf.amount) AS final_amount
            FROM ticket_flights tf
            GROUP BY tf.flight_id
        )
        SELECT fr.flight_id, fr.final_amount
        FROM flight_revenue fr
        ORDER BY fr.final_amount DESC
        LIMIT 1;
    ''',
}

for title, sql in queries.items():
    print('\n' + '=' * 80)
    print(title)
    print('=' * 80)
    df = query_df(sql)
    print(df.to_string(index=False) if not df.empty else '[пустой результат]')
