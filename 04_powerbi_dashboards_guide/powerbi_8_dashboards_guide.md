# 📘 Hướng Dẫn Chi Tiết: Tái Hiện 8 Dashboard Ngân Hàng Bán Lẻ
> Tài liệu hướng dẫn thao tác trên Power BI Desktop để dựng thành 8 Dashboard chuyên nghiệp từ bộ dữ liệu mẫu sạch trong thư mục `data_output/`.

---

## 🌟 1. BÁO CÁO HOẠT ĐỘNG KINH DOANH (HDKD)
* **Mục tiêu:** Cung cấp góc nhìn toàn cảnh về tăng trưởng quy mô (Quy mô huy động, Quy mô tín dụng, Doanh số thu phí) cho Ban Giám đốc Khối & Vùng.
* **Các trang báo cáo:**
  1. **Trang `Overview` (Tổng quan Khối):**
     * Thẻ KPI Cards: Tổng Dư nợ Tín dụng (Ngàn tỷ), Tổng Huy động (CASA + FD), Doanh số Bảo hiểm APE, Số lượng Thẻ mới.
     * Biểu đồ Clustered Bar Chart: So sánh Thực hiện vs Kế hoạch theo 3 Vùng (Miền Bắc, Miền Trung, Miền Nam).
     * Slicer: Năm/Tháng (`YearMonth`), Vùng (`Ten_Vung`), Hạng ĐVKD (`Hang_DVKD`).
  2. **Trang `Chi Tiết SP` (Cơ cấu Sản phẩm):**
     * Biểu đồ Donut Chart: Cơ cấu Huy động vốn (Tỷ trọng CASA vs Tiền gửi có kỳ hạn FD).
     * Line Chart: Xu hướng tăng trưởng dư nợ theo tháng (MoM Growth Trend).
  3. **Trang `Tín Dụng` (Lending Deep-dive):**
     * Biểu đồ Treemap: Dư nợ phân bổ theo từng loại gói vay (Vay mua nhà đất, Vay mua ô tô, Vay SXKD).
     * Bảng ma trận Matrix Table: Chi tiết Dư nợ từng Chi nhánh, Tỷ lệ hoàn thành % và Xếp hạng.

---

## ⚡ 2. BÁO CÁO DAILY CBNV (DAILY SALES PACING & RUN-RATE)
* **Mục tiêu:** Giúp Giám đốc Chi nhánh và Trưởng bộ phận theo dõi tốc độ bán hàng hàng ngày, phát hiện nguy cơ hụt chỉ tiêu trước khi hết tháng.
* **Các Visual chính:**
  1. **Thước đo Pacing Bullet Chart / Gauge:**
     * Kim chỉ: Doanh số thực tế MTD.
     * Vạch đích: Target tháng.
     * Vạch mốc dự kiến (Run-rate benchmark): Tỷ lệ ngày làm việc đã qua trong tháng.
  2. **Dự báo cuối tháng (Month-End Forecast Line):** Đường thẳng dự phóng điểm rơi doanh số nếu duy trì tốc độ hiện tại.
  3. **Heatmap Table:** Ma trận theo dõi ngày bán hàng tích cực vs ngày không phát sinh số của từng RM.

---

## 🎯 3. BÁO CÁO PHỄU BÁN HÀNG TÍN DỤNG (LENDING SALES FUNNEL)
* **Mục tiêu:** Theo dõi luồng xử lý hồ sơ vay từ lúc RM tiếp nhận đến khi giải ngân, xác định điểm nghẽn rớt hồ sơ.
* **Dataset sử dụng:** `fact_credit_funnel_detail.csv`
* **Các Visual chính:**
  1. **Funnel Visual (Biểu đồ phễu 5 tầng):**
     * Tầng 1: Hồ sơ tiếp nhận (100%)
     * Tầng 2: Thẩm định tín dụng thông qua (~88%)
     * Tầng 3: Phê duyệt rủi ro cấp tín dụng (~72%)
     * Tầng 4: Hoàn tất ký HĐ & Thủ tục thế chấp (~68%)
     * Tầng 5: Giải ngân thành công (~64%)
  2. **Gauge / Card Visual: Tỷ lệ chuyển đổi tổng thể (Overall Conversion Rate %)**
  3. **Bar Chart: Thời gian xử lý trung bình (TAT - Turnaround Time tính bằng ngày):**
     * Phân loại theo kênh tiếp nhận (Direct Sales vs Đối tác Showroom vs Digital).
  4. **Matrix Table:** Danh sách các hồ sơ bị từ chối / khách rút hồ sơ và nguyên nhân chính.

---

## 🏆 4. BÁO CÁO KPI & INCENTIVE CÁC CHỨC DANH
* **Mục tiêu:** Bảng điểm minh bạch tính toán hiệu suất cá nhân và ước tính tiền thưởng động lực (Incentive) cho nhân sự.
* **Dataset sử dụng:** `fact_kpi_actual_luy_ke.csv` kết hợp `dim_employee_cbnv.csv`
* **Các trang báo cáo:**
  1. **Trang `Vùng, ĐVKD, CBQL`:**
     * Bảng xếp hạng Chi nhánh (Leaderboard): Xếp hạng theo Điểm KPI Tổng Hợp.
     * Phân bổ hạng hiệu suất: Biểu đồ cột đếm số lượng nhân sự đạt loại A (Xuất sắc), B (Đạt), C (Cần nỗ lực), D (Chưa đạt).
  2. **Trang `TBP, CBNV` (Bảng điểm từng nhân sự):**
     * Search Box / Slicer chọn tên Cán bộ (RM/PBO).
     * Radar / Spider Chart: Radar đo lường độ hoàn thiện 5 cánh hoa sản phẩm (Tín dụng, CASA, Tiền gửi, Thẻ, Bảo hiểm).
     * Card Visual: Tiền thưởng Incentive dự kiến tháng này (Triệu VND).

---

## 👥 5. BỘ 4 DASHBOARD DANH MỤC KHÁCH HÀNG 2025 (CUSTOMER PORTFOLIOS)
* **Dataset sử dụng:** `fact_customer_portfolio_detail.csv`

### 5.1. Dashboard Danh Mục CASA (Tiền Gửi Không Kỳ Hạn):
* **Visual:** Phân khúc số dư CASA theo nhóm khách hàng (Mass vs Mass Affluent vs VIP).
* **Metric:** Số dư CASA bình quân/khách hàng, Tỷ lệ CASA chiếm dụng chi phí vốn rẻ.

### 5.2. Dashboard Danh Mục FD (Tiền Gửi Có Kỳ Hạn):
* **Visual:** Cơ cấu tiền gửi theo kỳ hạn và quy mô gửi tiết kiệm.
* **Tỷ lệ Retention:** Tỷ lệ khách hàng tái tục sổ tiết kiệm khi đến hạn.

### 5.3. Dashboard Danh Mục Thẻ Tín Dụng (TTD):
* **Visual:** Số lượng thẻ phát hành vs Thẻ kích hoạt có chi tiêu (Active Rate %).
* **Cơ cấu chi tiêu:** Doanh số quẹt thẻ bình quân theo từng phân hạng thẻ (Classic vs Platinum vs Signature).

### 5.4. Dashboard Danh Mục Khách Hàng REACTIVE:
* **Visual:** Hiệu quả chiến dịch "Đánh thức khách hàng ngủ đông".
* **Phễu:** Danh sách KH không giao dịch >6 tháng $\rightarrow$ Tiếp cận thành công $\rightarrow$ Phát sinh số dư/giao dịch mới.
