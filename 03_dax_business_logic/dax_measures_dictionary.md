# 🧮 Enterprise Retail Banking DAX Business Logic & Measures Library
> Tổng hợp toàn bộ công thức DAX nghiệp vụ tính toán cho 8 Dashboard Ngân hàng Bán lẻ (Khối KHCN).
> Được thiết kế chuẩn Star Schema, tối ưu hiệu năng VertiPaq và hỗ trợ Time Intelligence.

---

## 1. 📊 Nhóm Đo Lường KPI & Tiến Độ (Pacing / Run-rate)

### [Total Actual Sales]
```dax
Total Actual Lending = SUM(fact_kpi_actual_luy_ke[DS_tin_dung_TH])
Total Target Lending = SUM(fact_kpi_targets_monthly[Target_TIN_DUNG])

Total Actual CASA = SUM(fact_kpi_actual_luy_ke[DS_CASA_TH])
Total Target CASA = SUM(fact_kpi_targets_monthly[Target_CASA])

Total Actual Deposit FD = SUM(fact_kpi_actual_luy_ke[DS_CKH_TH])
Total Target Deposit FD = SUM(fact_kpi_targets_monthly[Target_FD])

Total Actual Bancassurance = SUM(fact_kpi_actual_luy_ke[DS_bao_hiem_TH])
Total Target Bancassurance = SUM(fact_kpi_targets_monthly[Target_BAO_HIEM])

Total Actual Credit Cards = SUM(fact_kpi_actual_luy_ke[DS_The_TD_TH])
Total Target Credit Cards = SUM(fact_kpi_targets_monthly[Target_THE_TD])
```

### [% Hoàn Thành Chỉ Tiêu (Achievement Rate)]
```dax
Lending Achievement % = 
DIVIDE([Total Actual Lending], [Total Target Lending], 0)

CASA Achievement % = 
DIVIDE([Total Actual CASA], [Total Target CASA], 0)

Banca Achievement % = 
DIVIDE([Total Actual Bancassurance], [Total Target Bancassurance], 0)
```

### [Tốc Độ Về Đích Dự Phóng (Projected Month-End Run-rate)]
```dax
Working Days Passed = 
CALCULATE(
    COUNTROWS(dim_calendar),
    dim_calendar[IsWorkingDay] = 1,
    dim_calendar[Full_Date] <= TODAY()
)

Total Working Days in Month = 
CALCULATE(
    COUNTROWS(dim_calendar),
    dim_calendar[IsWorkingDay] = 1,
    ALL(dim_calendar[Day])
)

Projected Month-End Lending Volume = 
VAR Passed = [Working Days Passed]
VAR TotalDays = [Total Working Days in Month]
VAR ActualMTD = [Total Actual Lending]
RETURN
IF(
    Passed > 0,
    DIVIDE(ActualMTD, Passed, 0) * TotalDays,
    BLANK()
)

Projected RunRate % = 
DIVIDE([Projected Month-End Lending Volume], [Total Target Lending], 0)
```

---

## 2. 🏆 Nhóm Điểm KPI Tổng Hợp & Ước Tính Thưởng (Incentive Engine)
> Bám sát theo Chính sách KPIs KHCN (Chính Sách KPI KHCN Chuẩn)

```dax
Weighted Composite KPI Score = 
VAR W_Lending = [Lending Achievement %] * 0.35
VAR W_CASA = [CASA Achievement %] * 0.25
VAR W_FD = DIVIDE([Total Actual Deposit FD], [Total Target Deposit FD], 0) * 0.15
VAR W_Banca = [Banca Achievement %] * 0.15
VAR W_Card = DIVIDE([Total Actual Credit Cards], [Total Target Credit Cards], 0) * 0.10
RETURN
(W_Lending + W_CASA + W_FD + W_Banca + W_Card) * 100

Estimated Incentive (Million VND) = 
SUM(fact_kpi_actual_luy_ke[Incentive_Du_Kien_Trieu_VND])

Rank Sales in Branch = 
RANKX(
    ALL(dim_employee_cbnv[Ho_ten_sale]),
    [Weighted Composite KPI Score],
    ,
    DESC,
    Dense
)
```

---

## 3. 🎯 Nhóm Phễu Tín Dụng (Lending Sales Funnel Metrics)

```dax
Total Applications Received = COUNTROWS(fact_credit_funnel_detail)

Total Loan Amount Requested (Billion VND) = 
DIVIDE(SUM(fact_credit_funnel_detail[So_Tien_De_Nghi_Trieu_VND]), 1000, 0)

Total Loan Disbursed (Billion VND) = 
DIVIDE(SUM(fact_credit_funnel_detail[So_Tien_Giai_Ngan_Trieu_VND]), 1000, 0)

Funnel Stage 1 to 2 % (Thẩm Định) = 
DIVIDE(SUM(fact_credit_funnel_detail[Buoc_2_Tham_Dinh]), [Total Applications Received], 0)

Funnel Stage 2 to 3 % (Phê Duyệt) = 
DIVIDE(SUM(fact_credit_funnel_detail[Buoc_3_Phe_Duyet]), SUM(fact_credit_funnel_detail[Buoc_2_Tham_Dinh]), 0)

Overall Conversion Rate % (Tiếp Nhận -> Giải Ngân) = 
DIVIDE(SUM(fact_credit_funnel_detail[Buoc_5_Giai_Ngan]), [Total Applications Received], 0)

Average Turnaround Time (TAT Days) = 
AVERAGE(fact_credit_funnel_detail[TAT_Ngay_Xu_Ly])
```

---

## 4. 👥 Nhóm Danh Mục Khách Hàng (CASA, FD, Thẻ & Reactive)

```dax
Total Retail Customers = COUNTROWS(fact_customer_portfolio_detail)

Total CASA Balance (Billion VND) = 
DIVIDE(SUM(fact_customer_portfolio_detail[So_Du_CASA_Trieu_VND]), 1000, 0)

Average CASA per Customer (Million VND) = 
AVERAGE(fact_customer_portfolio_detail[So_Du_CASA_Trieu_VND])

Credit Card Active Adoption Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS(fact_customer_portfolio_detail), fact_customer_portfolio_detail[Co_The_Tin_Dung] = "Có"),
    [Total Retail Customers],
    0
)

Cross-Sell Ratio (Avg Products per Customer) = 
AVERAGE(fact_customer_portfolio_detail[So_Luong_SP_Su_Dung])

Total Reactivated Customers = 
CALCULATE(
    COUNTROWS(fact_customer_portfolio_detail),
    fact_customer_portfolio_detail[Trang_Thai_Reactive] = "Đã kích hoạt lại thành công"
)
```
