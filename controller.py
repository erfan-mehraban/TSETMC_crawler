import logging

from anbar import AnbarFactory
from engine import AllNamaads, OverallHistoryRecordOfNamaad


anbar = AnbarFactory.with_sqlite("test.sqlite")
print("Anbar initialized")

all_namaad_engine = AllNamaads()
all_namaads = list(
        all_namaad_engine.fetch()
)
print("fetch all namaads completed")
anbar.batch_save(all_namaads)
print("  saved")

for namaad in all_namaads:
    overall_history_engine = OverallHistoryRecordOfNamaad(namaad)
    records = list(
        overall_history_engine.fetch()
    )
    print(f"fetch overall history of {namaad.name} completed")

    anbar.batch_save(records)
    print(f"  saved")
