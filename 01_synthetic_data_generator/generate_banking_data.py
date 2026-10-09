import os
import sys
import random
import datetime
import pandas as pd
import numpy as np

# Force UTF-8 terminal encoding
sys.stdout.reconfigure(encoding='utf-8')

# Set seed for reproducible synthetic banking data
np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_output'))
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Starting Enterprise Banking Synthetic Data Generation...")

# ==========================================================
# 1. DIM_BRANCH & REGION HIERARCHY
# ==========================================================
regions = [
    {"region_id": "VUNG_1", "region_name": "Vùng 1 - Hà Nội & Miền Bắc"},
    {"region_id": "VUNG_2", "region_name": "Vùng 2 - Miền Trung & Tây Nguyên"},
    {"region_id": "VUNG_3", "region_name": "Vùng 3 - TP. Hồ Chí Minh & Miền Nam"}
]

branches = []
branch_counter = 1
for r in regions:
    for b_idx in range(1, 9):  # 8 branches per region = 24 branches total
        b_id = f"DVKD_{branch_counter:03d}"
        tier = random.choice(["Hạng 1", "Hạng 2", "Hạng 3"])
        branches.append({
            "Ma_DVKD": b_id,
            "Ten_DVKD": f"Chi nhánh {r['region_name'].split('-')[1].strip()} - Phòng GD {b_idx}",
            "Ma_Vung": r["region_id"],
            "Ten_Vung": r["region_name"],
            "Hang_DVKD": tier,
            "Dia_Ban": "Đô thị loại 1" if tier == "Hạng 1" else "Đô thị loại 2"
        })
        branch_counter += 1

df_branches = pd.DataFrame(branches)
df_branches.to_csv(os.path.join(OUTPUT_DIR, "dim_dvkd_branch.csv"), index=False, encoding="utf-8-sig")
print(f"✓ Saved dim_dvkd_branch.csv ({len(df_branches)} rows)")

# ==========================================================
# 2. DIM_EMPLOYEE & SALES FORCE (CBNV, TBP, CBQL)
# ==========================================================
ho_list = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ"]
dem_list = ["Văn", "Thị", "Hải", "Đức", "Minh", "Thu", "Ngọc", "Thanh", "Hoàng", "Xuân", "Phương"]
ten_list = ["An", "Bình", "Cường", "Dũng", "Giang", "Hương", "Huy", "Khoa", "Linh", "Mai", "Nam", "Phúc", "Quân", "Sơn", "Thảo", "Trang", "Tuấn", "Vy"]

titles = [
    {"chuc_danh": "Quan hệ Khách hàng Cá nhân (RM)", "nhom_chuc_danh": "CBNV", "ratio": 0.55},
    {"chuc_danh": "Chuyên viên Khách hàng Ưu tiên (Premier RM)", "nhom_chuc_danh": "CBNV", "ratio": 0.15},
    {"chuc_danh": "Giao dịch viên & Phát triển KH (PBO/CSO)", "nhom_chuc_danh": "CBNV", "ratio": 0.15},
    {"chuc_danh": "Trưởng Bộ Phận Khách Hàng Cá Nhân (TBP)", "nhom_chuc_danh": "TBP", "ratio": 0.10},
    {"chuc_danh": "Giám Đốc Chi Nhánh / Đơn Vị (CBQL)", "nhom_chuc_danh": "CBQL", "ratio": 0.05}
]

employees = []
emp_id_counter = 1001

for b in branches:
    # Each branch has ~10-14 staff
    num_staff = random.randint(10, 14)
    # Ensure 1 CBQL and 1-2 TBP per branch
    cbql_name = f"{random.choice(ho_list)} {random.choice(dem_list)} {random.choice(ten_list)}"
    cbql_cif = f"EMP_{emp_id_counter}"
    emp_id_counter += 1
    
    employees.append({
        "CIF_sale": cbql_cif,
        "Ho_ten_sale": cbql_name,
        "Chuc_danh_KPI": "Giám Đốc Chi Nhánh / Đơn Vị (CBQL)",
        "Nhom_chuc_danh": "CBQL",
        "Ma_DVKD": b["Ma_DVKD"],
        "Ma_Vung": b["Ma_Vung"],
        "CIF_TBP": None,
        "CIF_CBQL": cbql_cif,
        "Email_sale": f"{cbql_cif.lower()}@bankcorp.vn",
        "Trang_thai": "Đang làm việc"
    })
    
    # 2 TBP
    tbp_cifs = []
    for _ in range(2):
        tbp_name = f"{random.choice(ho_list)} {random.choice(dem_list)} {random.choice(ten_list)}"
        tbp_cif = f"EMP_{emp_id_counter}"
        emp_id_counter += 1
        tbp_cifs.append(tbp_cif)
        employees.append({
            "CIF_sale": tbp_cif,
            "Ho_ten_sale": tbp_name,
            "Chuc_danh_KPI": "Trưởng Bộ Phận Khách Hàng Cá Nhân (TBP)",
            "Nhom_chuc_danh": "TBP",
            "Ma_DVKD": b["Ma_DVKD"],
            "Ma_Vung": b["Ma_Vung"],
            "CIF_TBP": tbp_cif,
            "CIF_CBQL": cbql_cif,
            "Email_sale": f"{tbp_cif.lower()}@bankcorp.vn",
            "Trang_thai": "Đang làm việc"
        })
        
    # Remaining are RM / Premier RM / PBO
    for _ in range(num_staff - 3):
        emp_name = f"{random.choice(ho_list)} {random.choice(dem_list)} {random.choice(ten_list)}"
        emp_cif = f"EMP_{emp_id_counter}"
        emp_id_counter += 1
        t = random.choices(["Quan hệ Khách hàng Cá nhân (RM)", "Chuyên viên Khách hàng Ưu tiên (Premier RM)", "Giao dịch viên & Phát triển KH (PBO/CSO)"], weights=[0.65, 0.20, 0.15])[0]
        assigned_tbp = random.choice(tbp_cifs)
        employees.append({
            "CIF_sale": emp_cif,
            "Ho_ten_sale": emp_name,
            "Chuc_danh_KPI": t,
            "Nhom_chuc_danh": "CBNV",
            "Ma_DVKD": b["Ma_DVKD"],
            "Ma_Vung": b["Ma_Vung"],
            "CIF_TBP": assigned_tbp,
            "CIF_CBQL": cbql_cif,
            "Email_sale": f"{emp_cif.lower()}@bankcorp.vn",
            "Trang_thai": "Đang làm việc"
        })

df_employees = pd.DataFrame(employees)
df_employees.to_csv(os.path.join(OUTPUT_DIR, "dim_employee_cbnv.csv"), index=False, encoding="utf-8-sig")
print(f"✓ Saved dim_employee_cbnv.csv ({len(df_employees)} rows)")

# ==========================================================
# 3. DIM_DATE (Calendar for 2024 - 2025)
# ==========================================================
date_range = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
calendar = []
for d in date_range:
    is_work = 1 if d.weekday() < 5 else 0
    calendar.append({
        "Rptdate": d.strftime("%Y%m%d"),
        "Full_Date": d.strftime("%Y-%m-%d"),
        "Year": d.year,
        "Quarter": f"Q{d.quarter}",
        "YearMonth": d.strftime("%Y%m"),
        "Month": d.month,
        "Day": d.day,
        "DayOfWeek": d.strftime("%A"),
        "IsWorkingDay": is_work
    })
df_calendar = pd.DataFrame(calendar)
df_calendar.to_csv(os.path.join(OUTPUT_DIR, "dim_calendar.csv"), index=False, encoding="utf-8-sig")
print(f"✓ Saved dim_calendar.csv ({len(df_calendar)} rows)")

# ==========================================================
# 4. FACT_KPI_TARGETS (Chỉ tiêu Kế hoạch năm & tháng)
# ==========================================================
# Target metrics align directly with sales incentive policy:
# Huy động CKH (Term Deposit), CASA (KKH), Tín dụng (Lending), Thẻ tín dụng, Bảo hiểm (Banca APE), v.v.
kpi_products = [
    {"code": "CASA", "name": "Số dư bình quân CASA (KKH)", "unit": "Triệu VND"},
    {"code": "FD", "name": "Huy động Tiền gửi có kỳ hạn (CKH)", "unit": "Triệu VND"},
    {"code": "TIN_DUNG", "name": "Dư nợ Tín dụng bán lẻ", "unit": "Triệu VND"},
    {"code": "THE_TD", "name": "Số lượng Thẻ tín dụng kích hoạt mới", "unit": "Thẻ"},
    {"code": "BAO_HIEM", "name": "Doanh số Bảo hiểm Nhân thọ (APE)", "unit": "Triệu VND"},
    {"code": "REACTIVE", "name": "Số lượng KH ngủ đông kích hoạt lại", "unit": "Khách hàng"}
]

months_2024_2025 = [
    "202401", "202402", "202403", "202404", "202405", "202406",
    "202407", "202408", "202409", "202410", "202411", "202412",
    "202501", "202502", "202503", "202504", "202505", "202506"
]

targets = []
for ym in months_2024_2025:
    for _, emp in df_employees.iterrows():
        # Assigned targets based on role
        chuc_danh = emp["Chuc_danh_KPI"]
        multiplier = 1.4 if "Premier" in chuc_danh else (1.0 if "RM" in chuc_danh else 0.6)
        
        targets.append({
            "YearMonth": ym,
            "CIF_sale": emp["CIF_sale"],
            "Ma_DVKD": emp["Ma_DVKD"],
            "Ma_Vung": emp["Ma_Vung"],
            "Target_CASA": round(1500 * multiplier * random.uniform(0.9, 1.2), 2),
            "Target_FD": round(8000 * multiplier * random.uniform(0.85, 1.25), 2),
            "Target_TIN_DUNG": round(12000 * multiplier * random.uniform(0.9, 1.3), 2),
            "Target_THE_TD": int(round(15 * multiplier * random.uniform(0.8, 1.2))),
            "Target_BAO_HIEM": round(250 * multiplier * random.uniform(0.7, 1.4), 2),
            "Target_REACTIVE": int(round(8 * multiplier * random.uniform(0.8, 1.3)))
        })

df_targets = pd.DataFrame(targets)
df_targets.to_csv(os.path.join(OUTPUT_DIR, "fact_kpi_targets_monthly.csv"), index=False, encoding="utf-8-sig")
print(f"✓ Saved fact_kpi_targets_monthly.csv ({len(df_targets)} rows)")

# ==========================================================
# 5. FACT_ACTUAL_KPI_LUY_KE (Thực hiện lũy kế & Điểm KPI theo Stored Proc)
# ==========================================================
actuals = []
for idx, row in df_targets.iterrows():
    # Performance distribution: 20% Top performers (>120%), 60% On-track (85-115%), 20% Underperforming (40-80%)
    perf_tier = random.choices(["top", "normal", "low"], weights=[0.20, 0.65, 0.15])[0]
    perf_factor = random.uniform(1.2, 1.6) if perf_tier == "top" else (random.uniform(0.88, 1.15) if perf_tier == "normal" else random.uniform(0.45, 0.78))
    
    act_casa = round(row["Target_CASA"] * perf_factor * random.uniform(0.95, 1.05), 2)
    act_fd = round(row["Target_FD"] * perf_factor * random.uniform(0.92, 1.08), 2)
    act_td = round(row["Target_TIN_DUNG"] * perf_factor * random.uniform(0.90, 1.10), 2)
    act_the = int(round(row["Target_THE_TD"] * perf_factor * random.uniform(0.85, 1.15)))
    act_bh = round(row["Target_BAO_HIEM"] * perf_factor * random.uniform(0.80, 1.25), 2)
    act_reactive = int(round(row["Target_REACTIVE"] * perf_factor * random.uniform(0.80, 1.20)))
    
    # Calculate % completion
    pct_casa = min(200.0, round((act_casa / max(1, row["Target_CASA"])) * 100, 1))
    pct_fd = min(200.0, round((act_fd / max(1, row["Target_FD"])) * 100, 1))
    pct_td = min(200.0, round((act_td / max(1, row["Target_TIN_DUNG"])) * 100, 1))
    pct_the = min(200.0, round((act_the / max(1, row["Target_THE_TD"])) * 100, 1))
    pct_bh = min(200.0, round((act_bh / max(1, row["Target_BAO_HIEM"])) * 100, 1))
    pct_re = min(200.0, round((act_reactive / max(1, row["Target_REACTIVE"])) * 100, 1))
    
    # Weighted composite KPI score (aligning with Sales Incentive Policy)
    # Weights: Tín dụng 35%, CASA 25%, Tiền gửi 15%, Bảo hiểm 15%, Thẻ 10%
    score_kpi = round(pct_td * 0.35 + pct_casa * 0.25 + pct_fd * 0.15 + pct_bh * 0.15 + pct_the * 0.10, 2)
    
    # Incentive estimation (VND million)
    incentive_est = 0
    if score_kpi >= 130:
        incentive_est = round(random.uniform(18, 35), 2)
    elif score_kpi >= 100:
        incentive_est = round(random.uniform(8, 17), 2)
    elif score_kpi >= 80:
        incentive_est = round(random.uniform(2, 6), 2)
    else:
        incentive_est = 0.0

    actuals.append({
        "YearMonth": row["YearMonth"],
        "CIF_sale": row["CIF_sale"],
        "Ma_DVKD": row["Ma_DVKD"],
        "Ma_Vung": row["Ma_Vung"],
        "DS_CASA_TH": act_casa,
        "DS_CKH_TH": act_fd,
        "DS_tin_dung_TH": act_td,
        "DS_The_TD_TH": act_the,
        "DS_bao_hiem_TH": act_bh,
        "DS_KH_reactive_TH": act_reactive,
        "Ty_le_HT_CASA": pct_casa,
        "Ty_le_HT_CKH": pct_fd,
        "Ty_le_HT_Tin_dung": pct_td,
        "Ty_le_HT_The": pct_the,
        "Ty_le_HT_Bao_hiem": pct_bh,
        "Ty_le_HT_Reactive": pct_re,
        "Diem_KPI_Tong_Hop": score_kpi,
        "Incentive_Du_Kien_Trieu_VND": incentive_est,
        "Xep_Hang_KPI": "A - Xuất sắc" if score_kpi >= 120 else ("B - Đạt" if score_kpi >= 90 else ("C - Cần nỗ lực" if score_kpi >= 70 else "D - Không đạt"))
    })

df_actuals = pd.DataFrame(actuals)
df_actuals.to_csv(os.path.join(OUTPUT_DIR, "fact_kpi_actual_luy_ke.csv"), index=False, encoding="utf-8-sig")
print(f"✓ Saved fact_kpi_actual_luy_ke.csv ({len(df_actuals)} rows)")

# ==========================================================
# 6. FACT_CREDIT_FUNNEL (Phễu Bán Hàng Tín Dụng)
# ==========================================================
# Stages: 1. Tiếp nhận hồ sơ -> 2. Thẩm định tín dụng -> 3. Phê duyệt rủi ro -> 4. Hoàn thiện thủ tục TSĐB -> 5. Giải ngân thành công
funnel_records = []
loan_types = ["Vay Mua Nhà Đất", "Vay Mua Ô Tô", "Vay Sản Xuất Kinh Doanh", "Vay Tiêu Dùng Thế Chấp"]
channels = ["Direct Sales (RM)", "Đối tác Showroom/Bất động sản", "Khách hàng cũ giới thiệu", "Kênh Digital / Website"]

for year in [2024, 2025]:
    for month in range(1, 13 if year == 2024 else 7):
        ym = f"{year}{month:02d}"
        for _, b in df_branches.iterrows():
            num_apps = random.randint(25, 45)
            for app_idx in range(num_apps):
                app_id = f"HS_{ym}_{b['Ma_DVKD']}_{app_idx:03d}"
                amount_req = round(random.uniform(500, 4500), 1) # Triệu VND
                loan_t = random.choice(loan_types)
                chnl = random.choice(channels)
                
                # Conversion steps
                pass_step1 = True # Tiếp nhận
                pass_step2 = random.random() < 0.88 # Thẩm định
                pass_step3 = pass_step2 and (random.random() < 0.82) # Phê duyệt
                pass_step4 = pass_step3 and (random.random() < 0.94) # Ký HĐ & TSĐB
                pass_step5 = pass_step4 and (random.random() < 0.95) # Giải ngân
                
                status = "5. Đã giải ngân" if pass_step5 else (
                    "4. Đang làm thủ tục TSBĐ" if pass_step4 else (
                        "3. Đã phê duyệt, chờ khách chốt" if pass_step3 else (
                            "2. Đang thẩm định hồ sơ" if pass_step2 else "Từ chối / Khách rút hồ sơ"
                        )
                    )
                )
                
                disbursed_amt = amount_req if pass_step5 else 0.0
                tat_days = random.randint(3, 14) # Turnaround time (ngày)
                
                funnel_records.append({
                    "Ma_Ho_So": app_id,
                    "YearMonth": ym,
                    "Ma_DVKD": b["Ma_DVKD"],
                    "Ma_Vung": b["Ma_Vung"],
                    "Loai_Vay": loan_t,
                    "Kenh_Tiep_Nhan": chnl,
                    "So_Tien_De_Nghi_Trieu_VND": amount_req,
                    "So_Tien_Giai_Ngan_Trieu_VND": disbursed_amt,
                    "Trang_Thai_Phe_Duyet": status,
                    "Buoc_1_Tiep_Nhan": 1,
                    "Buoc_2_Tham_Dinh": 1 if pass_step2 else 0,
                    "Buoc_3_Phe_Duyet": 1 if pass_step3 else 0,
                    "Buoc_4_Thu_Tuc": 1 if pass_step4 else 0,
                    "Buoc_5_Giai_Ngan": 1 if pass_step5 else 0,
                    "TAT_Ngay_Xu_Ly": tat_days
                })

df_funnel = pd.DataFrame(funnel_records)
df_funnel.to_csv(os.path.join(OUTPUT_DIR, "fact_credit_funnel_detail.csv"), index=False, encoding="utf-8-sig")
print(f"✓ Saved fact_credit_funnel_detail.csv ({len(df_funnel)} rows)")

# ==========================================================
# 7. FACT_CUSTOMER_PORTFOLIO (CASA, FD, Thẻ Tín Dụng, Reactive)
# ==========================================================
customers = []
cust_segments = ["Mass", "Mass Affluent", "Priority VIP", "Private Banking"]
card_tiers = ["Classic Standard", "Gold Visa", "Platinum CashBack", "Signature Infinite"]

for i in range(1, 4001):  # 4,000 synthetic banking customers
    cid = f"KH_{i:06d}"
    c_name = f"{random.choice(ho_list)} {random.choice(dem_list)} {random.choice(ten_list)}"
    # Masked name in compliance with function.sql
    masked_name = c_name.split()[0] + " * * " + c_name.split()[-1]
    
    seg = random.choices(cust_segments, weights=[0.60, 0.25, 0.12, 0.03])[0]
    assigned_branch = random.choice(branches)["Ma_DVKD"]
    
    # Financial metrics
    casa_bal = round(float(np.random.exponential(scale=35 if seg == "Mass" else 280)), 2)
    has_fd = random.random() < (0.35 if seg == "Mass" else 0.75)
    fd_bal = round(random.uniform(100, 2500) if has_fd else 0.0, 2)
    
    has_card = random.random() < 0.65
    c_tier = random.choice(card_tiers) if has_card else "Chưa mở thẻ"
    card_spend = round(random.uniform(5, 45) if has_card else 0.0, 2)
    
    # Reactive program flag
    is_reactive = random.random() < 0.12
    reactive_status = "Đã kích hoạt lại thành công" if is_reactive and casa_bal > 10 else ("Đang tiếp cận" if is_reactive else "Bình thường")

    customers.append({
        "Ma_KH": cid,
        "Ten_KH_Masked": masked_name,
        "Phan_Khuc_KH": seg,
        "Ma_DVKD": assigned_branch,
        "So_Du_CASA_Trieu_VND": casa_bal,
        "Co_Tien_Gui_FD": "Có" if has_fd else "Không",
        "So_Du_FD_Trieu_VND": fd_bal,
        "Co_The_Tin_Dung": "Có" if has_card else "Không",
        "Hang_The_TD": c_tier,
        "Doanh_So_Chi_Tieu_The_Trieu_VND": card_spend,
        "Trang_Thai_Reactive": reactive_status,
        "So_Luong_SP_Su_Dung": (1 if casa_bal > 0 else 0) + (1 if has_fd else 0) + (1 if has_card else 0)
    })

df_cust = pd.DataFrame(customers)
df_cust.to_csv(os.path.join(OUTPUT_DIR, "fact_customer_portfolio_detail.csv"), index=False, encoding="utf-8-sig")
print(f"✓ Saved fact_customer_portfolio_detail.csv ({len(df_cust)} rows)")

print("\n🎉 ALL 6 ENTERPRISE BANKING SYNTHETIC DATASETS GENERATED SUCCESSFULLY!")
