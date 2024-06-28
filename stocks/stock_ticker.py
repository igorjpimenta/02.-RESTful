import requests
import pandas as pd
# from datetime import datetime
from bs4 import BeautifulSoup
from decouple import config


class StockTicker:
    def __init__(self, ticker):
        self.url = f"{config('STOCK_TICKER_URL')}/{ticker}"

    def get_yield(self):
        route = '/dividendos'
        labels = ['class', 'value', 'granted_on', 'exercised_on', 'paid_on']

        data = self.get_data(route, labels)

        return data

    def get_bonuses(self):
        route = '/bonificacoes'
        labels = ['aproved_on', 'granted_on', 'exercised_on', 'ratio']

        data = self.get_data(route, labels)

        return data

    def get_splits(self):
        route = '/desdobramentos'
        labels = ['aproved_on', 'granted_on', 'exercised_on', 'ratio']

        data = self.get_data(route, labels)

        return data

    def get_data(self, route, labels):
        r = requests.get(self.url + route)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('table')

        data = []
        for tr in table.find('tbody').find_all('tr'):  # type: ignore
            cells = tr.find_all('td')
            row = [cell.text.strip() for cell in cells]
            data.append(row)

        df = pd.DataFrame(data, columns=labels)

        for col in df.columns:
            if col.endswith('_on'):
                # df[col] = df[col].apply(self.convert_date)
                df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')
                df[col] = df[col].dt.tz_localize('America/Sao_Paulo')

        if 'ratio' in labels:
            df['ratio'] = df['ratio'].apply(self.convert_ratio)

        return df

    @staticmethod
    def convert_ratio(ratio):
        num, denom = ratio.split(':')
        decimal_ratio = float(denom) / float(num)

        return decimal_ratio
