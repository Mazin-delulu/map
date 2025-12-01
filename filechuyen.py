import pandas as pd
import json

# Tên file Excel
EXCEL_FILE = "dulie.xlsx"

# Tên file JSON xuất ra
OUTPUT_JSON = "data_nghiencuu_new.json"

# Đọc sheet
df_vung = pd.read_excel(EXCEL_FILE, sheet_name="vung")
df_diem = pd.read_excel(EXCEL_FILE, sheet_name="diem")

# Chuẩn hóa NaN thành None
df_vung = df_vung.where(pd.notnull(df_vung), None)
df_diem = df_diem.where(pd.notnull(df_diem), None)

result = []

# Lấy danh sách id_vùng duy nhất
for id_vung in df_vung["id_vung"].unique():

    df_sub = df_vung[df_vung["id_vung"] == id_vung]

    # --- VÙNG ---
    region_name = df_sub["vùng"].iloc[0]
    year = df_sub["năm"].iloc[0]
    rep_lat = df_sub["vĩ độ (lat) của điểm đại diện"].iloc[0]
    rep_lon = df_sub["kinh độ (lon) của điểm đại diện"].iloc[0]

    # --- DANH SÁCH FILE / TÀI LIỆU ---
    groups = {}
    for _, row in df_sub.iterrows():
        group = row["tên nhóm tài liệu"] or "Tài liệu"
        filename = row["tên file"]

        if group not in groups:
            groups[group] = []

        if filename:
            groups[group].append({
                "name": filename,
                "url": ""   # người dùng tự điền
            })

    list_groups = [
        {"group_name": g, "files": groups[g]}
        for g in groups
    ]

    # --- ĐIỂM ---
    df_points = df_diem[df_diem["id_vùng"] == id_vung]
    points = []
    for _, row in df_points.iterrows():
        points.append({
            "name": row["tên điểm"],
            "lat": row["vĩ độ điểm (lat)"],
            "lon": row["kinh độ điểm (lon)"]
        })

    # --- TẠO CẤU TRÚC JSON ---
    region_json = {
        "region": region_name,
        "id_region": id_vung,
        "year": year,
        "representative": {
            "lat": rep_lat,
            "lon": rep_lon
        },
        "links": list_groups,
        "points": points
    }

    result.append(region_json)

# Xuất JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("✔ Xuất JSON thành công:", OUTPUT_JSON)
