from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://admin:admin@data_storage:5432/portfolio_data"
engine = create_engine(DATABASE_URL)

def save_data(ticker, data):
    data.to_sql(ticker.lower(), engine, if_exists='replace', index=False)

def fetch_data(ticker):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {ticker.lower()}"))
        return result.fetchall()
