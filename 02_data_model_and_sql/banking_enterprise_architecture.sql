-- ========================================================================================
-- ENTERPRISE RETAIL BANKING - DATA MODEL & ADVANCED ETL ARCHITECTURE
-- Database Schema: DWH_RETAIL_BANKING & MIS_SALES_ANALYTICS
-- Engine: Microsoft SQL Server / Azure Synapse / PostgreSQL
-- ========================================================================================

-- ========================================================================================
-- 1. DATA MASKING UTILITY FUNCTION (Bảo Vệ Thông Tin Khách Hàng - PII Protection)
-- Ref: function.sql in Bank Production System
-- ========================================================================================
CREATE OR ALTER FUNCTION [dbo].[fn_MaskCustomerName] (@Ten_KH NVARCHAR(200))
RETURNS NVARCHAR(200)
AS
BEGIN
    -- Che mờ tên đệm, chỉ để lại ký tự đầu và tên cuối cùng (Ví dụ: "Nguyễn Văn A" -> "Nguyễn * * A")
    IF @Ten_KH IS NULL OR LEN(TRIM(@Ten_KH)) = 0
        RETURN N'KHẨN DANH';

    DECLARE @FirstWord NVARCHAR(50), @LastWord NVARCHAR(50), @Result NVARCHAR(200);
    SET @Ten_KH = LTRIM(RTRIM(@Ten_KH));
    
    IF CHARINDEX(' ', @Ten_KH) = 0
        RETURN LEFT(@Ten_KH, 1) + '***';

    SET @FirstWord = SUBSTRING(@Ten_KH, 1, CHARINDEX(' ', @Ten_KH) - 1);
    SET @LastWord = RIGHT(@Ten_KH, CHARINDEX(' ', REVERSE(@Ten_KH)) - 1);
    
    SET @Result = @FirstWord + N' * * ' + @LastWord;
    RETURN @Result;
END;
GO

-- ========================================================================================
-- 2. ENTERPRISE ROW-LEVEL SECURITY (RLS) MATRIX VIEW (Phân Quyền Ma Trận Chi Nhánh/Vùng)
-- Dynamic Row-Level Security Matrix for Branch & Regional Hierarchies
-- Level: ALL (Khối/MIS), VUNG (GĐ Vùng), CBQL (GĐ Chi nhánh), TBP (Trưởng bộ phận), SALE (RM)
-- ========================================================================================
CREATE OR ALTER VIEW [dbo].[vw_Security_Branch_Hierarchy] AS
WITH UserSecurity AS (
    -- Lấy thông tin phiên đăng nhập của người dùng qua hàm User Security
    -- (Trong Power BI, ánh xạ với USERPRINCIPALNAME())
    SELECT 
        'ALL' AS SecurityLevel, 'HO' AS UserGroup, 'ALL' AS SecurityRight
    UNION ALL
    SELECT 'DVKD', 'VUNG', 'VUNG_1'
    UNION ALL
    SELECT 'DVKD', 'CBQL', 'EMP_1001'
    UNION ALL
    SELECT 'DVKD', 'TBP', 'EMP_1002'
    UNION ALL
    SELECT 'DVKD', 'SALE', 'EMP_1004'
),
BaseEmployeeData AS (
    SELECT 
        emp.CIF_sale,
        emp.Ho_ten_sale,
        emp.Chuc_danh_KPI,
        emp.Nhom_chuc_danh,
        emp.Ma_DVKD,
        b.Ten_DVKD,
        emp.Ma_Vung,
        b.Ten_Vung,
        emp.CIF_TBP,
        emp.CIF_CBQL
    FROM [dbo].[dim_employee_cbnv] emp
    LEFT JOIN [dbo].[dim_dvkd_branch] b ON emp.Ma_DVKD = b.Ma_DVKD
)
SELECT DISTINCT 
    b.*,
    sec.SecurityLevel,
    sec.UserGroup
FROM BaseEmployeeData b
INNER JOIN UserSecurity sec ON 
    sec.SecurityLevel = 'ALL' -- Hội sở & MIS thấy toàn bộ ngân hàng
    OR (sec.SecurityLevel = 'DVKD' AND sec.UserGroup = 'VUNG' AND b.Ma_Vung = sec.SecurityRight) -- Giám đốc Vùng
    OR (sec.SecurityLevel = 'DVKD' AND sec.UserGroup = 'CBQL' AND b.CIF_CBQL = sec.SecurityRight) -- Giám đốc Chi nhánh
    OR (sec.SecurityLevel = 'DVKD' AND sec.UserGroup = 'TBP'  AND b.CIF_TBP = sec.SecurityRight)  -- Trưởng bộ phận
    OR (sec.SecurityLevel = 'DVKD' AND sec.UserGroup = 'SALE' AND b.CIF_sale = sec.SecurityRight);-- Cán bộ bán hàng (RM)
GO

-- ========================================================================================
-- 3. STORED PROCEDURE: TÍNH TOÁN DOANH SỐ THỰC HIỆN LŨY KẾ & TỶ LỆ HOÀN THÀNH KPI
-- Automated Cumulative Sales Performance & Incentive Calculation Engine
-- ========================================================================================
CREATE OR ALTER PROCEDURE [dbo].[sp_Calculate_Sales_KPI_LuyKe]
    @ReportMonth VARCHAR(6) -- Ví dụ: '202506'
AS
BEGIN
    SET NOCOUNT ON;

    PRINT N'Bắt đầu tính toán lũy kế KPI Khối KHCN cho tháng: ' + @ReportMonth;

    -- CTE tổng hợp chỉ tiêu & thực hiện
    WITH MonthlyPerformance AS (
        SELECT 
            act.YearMonth,
            act.CIF_sale,
            emp.Ho_ten_sale,
            emp.Chuc_danh_KPI,
            act.Ma_DVKD,
            b.Ten_DVKD,
            act.Ma_Vung,
            b.Ten_Vung,
            -- Chỉ tiêu
            tgt.Target_CASA,
            tgt.Target_FD,
            tgt.Target_TIN_DUNG,
            tgt.Target_THE_TD,
            tgt.Target_BAO_HIEM,
            tgt.Target_REACTIVE,
            -- Thực hiện
            act.DS_CASA_TH,
            act.DS_CKH_TH,
            act.DS_tin_dung_TH,
            act.DS_The_TD_TH,
            act.DS_bao_hiem_TH,
            act.DS_KH_reactive_TH,
            -- % Hoàn thành
            act.Ty_le_HT_CASA,
            act.Ty_le_HT_CKH,
            act.Ty_le_HT_Tin_dung,
            act.Ty_le_HT_The,
            act.Ty_le_HT_Bao_hiem,
            act.Ty_le_HT_Reactive,
            -- Điểm tổng hợp & Incentive
            act.Diem_KPI_Tong_Hop,
            act.Incentive_Du_Kien_Trieu_VND,
            act.Xep_Hang_KPI
        FROM [dbo].[fact_kpi_actual_luy_ke] act
        INNER JOIN [dbo].[fact_kpi_targets_monthly] tgt 
            ON act.YearMonth = tgt.YearMonth AND act.CIF_sale = tgt.CIF_sale
        INNER JOIN [dbo].[dim_employee_cbnv] emp 
            ON act.CIF_sale = emp.CIF_sale
        INNER JOIN [dbo].[dim_dvkd_branch] b 
            ON act.Ma_DVKD = b.Ma_DVKD
        WHERE act.YearMonth = @ReportMonth
    ),
    RankingByRole AS (
        SELECT 
            *,
            -- Xếp hạng theo Chức danh trong toàn hệ thống
            DENSE_RANK() OVER (
                PARTITION BY Chuc_danh_KPI 
                ORDER BY Diem_KPI_Tong_Hop DESC
            ) AS Rank_Toan_He_Thong,
            -- Xếp hạng nội bộ trong Chi nhánh
            DENSE_RANK() OVER (
                PARTITION BY Ma_DVKD, Chuc_danh_KPI 
                ORDER BY Diem_KPI_Tong_Hop DESC
            ) AS Rank_Chi_Nhanh
        FROM MonthlyPerformance
    )
    SELECT * 
    FROM RankingByRole
    ORDER BY Ma_Vung, Ma_DVKD, Diem_KPI_Tong_Hop DESC;

    PRINT N'Hoàn tất tổng hợp KPI.';
END;
GO
