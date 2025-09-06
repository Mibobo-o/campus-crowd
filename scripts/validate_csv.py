import csv, sys, pathlib

OK = True
root = pathlib.Path(__file__).resolve().parents[1]
loc = root / "data" / "locations_master.csv"
mea = root / "data" / "measurements.csv"

def expect_header(path, header):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        h = next(reader, [])
    return h == header

# 1) 헤더 검사
OK &= expect_header(loc, ["id","name","type","lat","lon","capacity"])
OK &= expect_header(mea, ["timestamp","location_id","occupancy_rate","occupancy_level","weekday","weather","source"])

# 2) 값 범위 검사 (샘플 전수)
with open(mea, newline='', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for i,row in enumerate(r, start=2):
        try:
            rate = float(row["occupancy_rate"])
            if not (0.0 <= rate <= 1.0):
                print(f"[measurements.csv:{i}] occupancy_rate out of range: {rate}")
                OK = False
        except:
            print(f"[measurements.csv:{i}] invalid occupancy_rate: {row['occupancy_rate']}")
            OK = False

if not OK:
    sys.exit(1)
print("CSV schema & range check OK")
