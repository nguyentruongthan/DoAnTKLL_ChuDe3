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
  + Input: sử dụng cảm biến hồng ngoại đặt kế bên động cơ piston đẩy vật thể
  + Output: nhận biết vật thể đi qua
  + Chức năng: Phát tín hiệu khi có vật thể đi qua, tín hiệu được dùng để điều khiển động cơ đẩy vật thể vào
đúng vị trí
  + Phần cứng sử dụng: cảm biến vật cản hồng ngoại lm393, stm32f103c8t6
  + Ưu điểm phần cứng: giá thành rẻ, độ nhạy cao nhận biết được vật thể chuyển động nhanh, stm32 có 
nhiều chân đa chức năng hơn adruino, chức năng vừa đủ để có thể xử lý nhiệm vụ đề ra.
  + Nhược điểm: 
  - Cảm biến hồng ngoại lm393: 
	Rất khó phát hiện được vật thể có màu đen, vì xử dụng việc phát và thu tín hiệu hồng ngoại 
nên tín hiệu dễ bị hấp thụ bởi vật thể tối màu, màu càng tối hấp thụ tín hiệu hồng ngoại càng tốt thì 
gần như không thể phát hiện được.
	Dù lọc được ánh sáng mặt trời nhưng nếu để tiếp xúc trực tiếp với ánh sáng mặt trời mạnh sẽ gây
mất tín hiệu hồng ngoại.
- Distribute item
- Motor
- Screen
  + Chức năng: hiển thị vật phẩm và số lượng tương ứng ra màn hình
  + Phần cứng sử dụ: vi điều khiển và màn hình LCD
