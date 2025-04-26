from datetime import datetime

import pytz


def to_brasilia(self, iso_utc_str):
        utc_dt = datetime.strptime(iso_utc_str, '%Y-%m-%dT%H:%M:%SZ')
        utc_dt = utc_dt.replace(tzinfo=pytz.UTC)
        brasilia_tz = pytz.timezone('America/Sao_Paulo')
        brasilia_dt = utc_dt.astimezone(brasilia_tz)
        
        data_hora = brasilia_dt.strftime('%d/%m/%Y %H:%M:%S')
        return f"{data_hora} Horário de Brasília"