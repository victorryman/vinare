import pandas as pd
from sqlalchemy import create_engine

# Save the final DataFrame to a CSV file
final_df = pd.read_csv('alla_viner.csv')

# Post it to local sql server for visualization purposes
connection_string = 'postgresql://tf_superset:tf_superset@192.168.33.130:5432/dw_1'
engine = create_engine(connection_string)
final_df.to_sql('vinare_data', engine, if_exists='replace', index=False)
engine.dispose()
