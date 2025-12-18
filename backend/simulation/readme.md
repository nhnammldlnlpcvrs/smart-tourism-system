1. Identify the system
    Notebook nhận biết hệ thống:
    Các địa điểm du lịch
    Điều kiện thời tiết
    Giới hạn sức chứa từng ngày
    Hành vi khách (ưu tiên – chọn ngẫu nhiên có trọng số)
    Trong notebook, phần này diễn ra ở:
    Cell load dữ liệu JSONL
    Cell mô tả data model

2. Define variables
    Notebook định nghĩa:
    province
    NUM_TOURISTS
    NUM_DAYS
    PREFERENCE_WEIGHT
    WEATHER_WEIGHT
    dữ liệu địa điểm
    giới hạn tải ngày
    => xác định thông số mô phỏng.

3. Define rules & behaviors
    Notebook mô hình hóa hành vi khách:
    Chọn điểm du lịch ưu tiên trước
    Tránh nơi xấu trời
    Nếu vượt capacity → thất bại (log lại)
    Mỗi khách quyết định mỗi ngày

4. Run the simulation
    Notebook chạy hàm:
    sim.run()
    Trong đó:
    Tạo log chi tiết cho từng khách
    Ghi lý do tại sao khách chọn hoặc không chọn điểm đó
    Sinh lịch trình thực tế của N khách trong M ngày
    
5. Collect output & analyze
    Notebook:
    Tạo summary_df tổng hợp lượt ghé thăm
    Vẽ biểu đồ thống kê
    Xuất file JSON chứa toàn bộ dữ liệu simulation
    Vẽ sơ đồ luồng (flow diagram)
