from history_db_tables import Url, Visit, VisitSource
import pandas as pd
from sqlalchemy import create_engine, desc, func
from sqlalchemy.sql import label
from sqlalchemy.orm import sessionmaker
import datetime
import os
import numpy as np
import argparse
from columnar import columnar


def start_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# transition type lookup table
transition_df = pd.DataFrame({
    "transition": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "transition_desc": ['LINK', 'TYPED', 'AUTO_BOOKMARK', 'AUTO_SUBFRAME',
               'MANUAL_SUBFRAME', 'GENERATED', 'START_PAGE',
               'FORM_SUBMIT', 'RELOAD', 'KEYWORD', 'KEYWORD_GENERATED']
})


def fetch_history_logs(db_engine):
    """
    fetch all webpage visits from the History database 
    """

    session = start_session(engine = db_engine)
    
    # url for from_visit id listed in visit table
    sub_query = session.query(
        Visit.id,
        label('from_url', Url.url)
    ).join(
       Url, Visit.url == Url.id 
    ).subquery()
    
    query = session.query(
        label('visit_time_utc', Visit.visit_time),
        Url.title,
        Url.url,
        label('url_id', Url.id),
        Visit.visit_duration,
        Visit.from_visit,
        Visit.transition,
        sub_query.c.from_url
    ).join(
        Visit, Url.id == Visit.url
    ).join(
        sub_query, Visit.from_visit == sub_query.c.id, isouter=True
    ).order_by(
            desc(Visit.visit_time)
    )
    
    df = pd.read_sql(query.statement, db_engine)
    
    session.close()
    
    # date/time formatting
    df['visit_time_utc'] = [datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp) for timestamp in df['visit_time_utc']]
    df['visit_duration_min'] = [np.round(x / 60000000, decimals=2) for x in df['visit_duration']]
    
    # transition lookup
    df['transition'] = [int(hex(x & 0x000000FF), 16) for x in df['transition']]
    df = pd.merge(df, transition_df, how = 'left', on = 'transition')
    
    # remove unneeded columns
    df = df[['visit_time_utc', 'visit_duration_min', 'title', 'url', 'url_id', 'transition', 'transition_desc', 'from_url']]
    
    return df


def fetch_history_summary(db_engine):
    """
    fetch summary metrics for each url in History database
    """

    session = start_session(engine=db_engine)
    
    # first visit timestamp for each url
    first_visit_sub_query = session.query(
        Url.url,
        label('first_visit_time', func.min(Visit.visit_time))
    ).join(
        Visit, Url.id == Visit.url
    ).group_by(
        Url.url
    ).subquery()
    
    query = session.query(
        label('url_id', Url.id),
        Url.title,
        Url.url,
        Url.visit_count,
        Url.typed_count,
        Url.hidden,
        first_visit_sub_query.c.first_visit_time,
        Url.last_visit_time
    ).join(
        first_visit_sub_query, Url.url == first_visit_sub_query.c.url
    ).order_by(
        desc(Url.visit_count)
    )

    df = pd.read_sql(query.statement, engine)
    
    session.close()
    
    df['last_visit_time'] = [datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp) for timestamp in df['last_visit_time']]
    df['first_visit_time'] = [datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp) for timestamp in df['first_visit_time']]

    return df


def console_print(df, headers):
    """
    print every 5 rows of query
    """
    
    size = 5
    df_list = [df.loc[x:x+size-1,:] for x in range(0, len(df), size)]
    n = 0
    l = len(df_list)
    while n <= l-1:
        print('')
        col_df = df_list[n]
        col_df = col_df.values.tolist()
        print(columnar(col_df, headers=headers))
        print('')
        additional = str(input('...')) # print next 15 lines
        n += 1
        if additional != '':
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('chrome_history_db', type=str, metavar='CHROME_HISTORY_DB', help='path of Chrome History database')
    parser.add_argument('-l', '--logs', action='store_true', help='gather historical webpage visits stored in History database')
    parser.add_argument('-s', '--summary', action='store_true', help='gather summary metrics for every url in History database')
    parser.add_argument('-o', '--outfile', action='store_true', help='output data to csv file (saved in cwd)')
    parser.add_argument('-op', '--outfilepath', help='output data to csv file (saved in specified path)', type=str)

    args = parser.parse_args()
    chrome_history_db = args.chrome_history_db
    logs = args.logs
    summary = args.summary
    outfile = args.outfile
    outfilepath = args.outfilepath

    if os.path.isfile(chrome_history_db):
        db_path = chrome_history_db     
    else:
        print(f'\n[!] Unable to find History database: {chrome_history_db}')

    engine = create_engine(rf'sqlite:///{db_path}')

    if logs:
        df = fetch_history_logs(db_engine=engine)
        header = '\n[+] Chrome History Logs:'
        col_names = ['visit_time_utc', 'visit_duration_min', 'title', 'url', 'url_id', 'transition', 'transition_desc', 'from_url']
        file_name = 'out_chrome_history_logs.csv'

    if summary:
        df = fetch_history_summary(db_engine=engine)
        header = '\n[+] Chrome History Summary:'
        col_names = ['url_id', 'title', 'url', 'visit_count', 'typed_count', 'hidden', 'first_visit_time', 'last_visit_time']
        file_name = 'out_chrome_history_summary.csv'
    
    if outfile:
        path = f'{os.getcwd()}/{file_name}'
        df.to_csv(path, index=False, encoding='utf-8')
        print(f'\n[+] CSV saved to: {path}\n')
    elif outfilepath:
        path = outfilepath
        df.to_csv(path, index=False, encoding='utf-8')
        print(f'\n[+] CSV saved to: {path}\n')
    else:
        print(header)
        console_print(df=df, headers = col_names)


    
    
    

