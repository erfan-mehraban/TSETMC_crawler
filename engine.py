import logging
from datetime import datetime
from typing import Iterator
from pytz import utc

import requests

from models import Namaad, OverallHistoryRecord


class DataFetcher:
    resource_page: str = ''

    def _get_resource_content(self) -> str:
        response = requests.get(self.resource_page)
        content = response.content.decode('utf-8')
        return content

    def fetch(self):
        raise NotImplemented()


class AllNamaads(DataFetcher):
    resource_page = 'http://www.tsetmc.com/tsev2/data/MarketWatchInit.aspx'

    def fetch(self) -> Iterator[Namaad]:
        content = self._get_resource_content()
        # filter and split namaads data from resource
        raw_namaads_data = content\
            .split('@')[2]\
            .split(';')
        # parse and fill Namaad
        for namaad_data in raw_namaads_data:
            parsed_namaad_data = namaad_data.split(',')
            yield Namaad(i=int(parsed_namaad_data[0]),
                         name=parsed_namaad_data[2])


def float_string_to_int(s: str) -> int:
    return int(float(s))

class OverallHistoryRecordOfNamaad(DataFetcher):
    resource_page = 'http://members.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i=%s&Top=999999&A=1'

    def __init__(self, namaad: Namaad):
        self.namaad = namaad

    def fetch(self) -> Iterator[OverallHistoryRecord]:
        self.resource_page = self.resource_page % self.namaad.i
        content = self._get_resource_content()
        for record_raw_data in content.split(';'):
            if record_raw_data == '':
                continue
            d = record_raw_data.split('@')
            date = None
            if d[0]:
                date = utc.localize(
                    datetime.strptime(d[0], '%Y%m%d')
                )
            yield OverallHistoryRecord(
                namaad_id=self.namaad.i,
                max_value=float_string_to_int(d[1]),
                min_value=float_string_to_int(d[2]),
                closing_price=float_string_to_int(d[3]),
                last_trade_price=float_string_to_int(d[4]),
                first_price=float_string_to_int(d[5]),
                yesterday_price=float_string_to_int(d[6]),
                value=float_string_to_int(d[7]),
                volume=float_string_to_int(d[8]),
                count=float_string_to_int(d[9]),
                date=date,
            )
