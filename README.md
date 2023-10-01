# DoAnTKLL_ChuDe3
Đồ án Thiết kế luận lý: Chủ đề 3 <br />
---------------------20.9.2023---------------------<br />
Phân chia công việc:
- Quốc Vũ: Tìm hiểu động cơ, cách chuyển động cơ từ xoay sang đẩy hướng ngang
- Quang Vũ: Tìm hiểu mạch phát hiện vật phẩm đi qua ứng với từng động cơ
- Thản: Tìm hiểu vi điều khiển ESP32 CAM

---------------------1.10.2023---------------------<br />
Sơ đồ hệ thống:
![system_diagram](https://github.com/nguyentruongthan/DoAnTKLL_ChuDe3/assets/112642014/93a02c42-b852-4458-aa7a-a61be5dd1061)
Mô tả từng module:
- Camera handle
  + Input: module sử dụng camera được đặt cố định để quay tại một vị trí cụ thể trên băng chuyền
  + Output: tín hiệu xác định loại vật phẩm
  + Chức năng: xác định loại vật phẩm đi qua vị trí camera quay lại 
  + Phần cứng sử dụng: ESP32-CAM
- Detect object through
  + Input: 
  + Output: 
- Distribute item
- Motor
- Screen
