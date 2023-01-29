import argparse,time
import pandas as pd
from sqlalchemy import create_engine
import os

def extract_data(file:str):
    df_itter = pd.read_csv(file,iterator=True,chunksize=100000)
    return df_itter

def main(params):
    os.system(f'wget {params.url}')
    conn = f'postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}'
    df = extract_data(params.url.split("/")[-1])
    load_data(df,conn)


def load_data(df_i:pd.DataFrame,conn:str):
    df = next(df_i)
    df.to_sql(name="yello_taxi",con=conn,if_exists="replace")
    while True:
        try:
            t_start = time.time()
            
            df = next(df_i)
            df.to_sql(name="yellow_taxi",con=conn,if_exists="replace")

            t_end = time.time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("job finished !")
            break

if __name__ == '__main__':
    args = argparse.ArgumentParser(description="Ingestion data with chunk data")

    args.add_argument("-i","--url",help="url csv download")
    args.add_argument("-u","--user",help="User database")
    args.add_argument("-p","--password",help="password database")
    args.add_argument("-s","--host",help="hostname database")
    args.add_argument("-v","--port",help="port database")
    args.add_argument("-d","--db",help="database database")

    args = args.parse_args()
    main(args)