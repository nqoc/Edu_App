# EduQuest

Ứng dụng desktop hỗ trợ quản lý học tập, tài khoản học sinh và giáo viên, dữ liệu điểm danh và các tiện ích học tập. Dự án được xây dựng chủ yếu bằng Python, PyQt5 và FastAPI, chạy trên Windows.

> **Trạng thái:** Đây là dự án học tập/prototype. Một số đường dẫn, cấu hình và thành phần phụ thuộc vào môi trường Windows của tác giả; cần kiểm tra và điều chỉnh trước khi triển khai thực tế.

## Tính năng chính

- Ứng dụng desktop với giao diện PyQt5.
- Đăng nhập và phân quyền theo loại tài khoản.
- Quản lý thông tin người dùng bằng SQLite.
- API cục bộ sử dụng FastAPI và Uvicorn.
- Quản lý dữ liệu học sinh, lớp học, điểm số và tình trạng vắng mặt.
- Lưu trữ liên kết phòng học trực tuyến.
- Các tiện ích hỗ trợ email, biểu đồ, mã QR và công cụ học tập.

## Công nghệ

- **Python** 3.10 được khuyến nghị.
- **PyQt5** cho giao diện desktop.
- **FastAPI** và **Uvicorn** cho API cục bộ.
- **SQLite** cho dữ liệu ứng dụng.
- OpenCV, MediaPipe, dlib và các thư viện xử lý dữ liệu/hình ảnh.
- PowerShell cho một số script chạy trên Windows.

## Yêu cầu hệ thống

- Windows 10/11.
- Python 3.10 64-bit.
- Quyền cài đặt package và chạy ứng dụng cục bộ.
- Visual C++ Build Tools có thể cần thiết nếu cài các package native thất bại.

## Cài đặt

### 1. Tạo virtual environment

Mở PowerShell tại thư mục dự án:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script, chỉ thay đổi policy trong phạm vi người dùng hiện tại:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 2. Cài dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirementsequirements.txt
```

File `requirementsequirements.txt` có package dlib dạng wheel dành cho CPython 3.10 trên Windows. Nếu môi trường Python khác phiên bản, cần thay wheel tương thích trước khi cài.

### 3. Cài font tùy chọn

Các font giao diện nằm trong thư mục `requirements`. Chỉ cài những font cần thiết cho giao diện; không cài file `requirements.txt` như một font.

## Khởi chạy

Ứng dụng sử dụng API cục bộ và giao diện desktop. Mở hai cửa sổ PowerShell tại thư mục dự án, kích hoạt cùng virtual environment trong cả hai cửa sổ.

### Cửa sổ 1: API server

```powershell
python mainAPI-SERVER.py
```

API mặc định lắng nghe tại `http://127.0.0.1:8000`. Endpoint kiểm tra nhanh:

```text
http://127.0.0.1:8000/check
```

### Cửa sổ 2: ứng dụng desktop

```powershell
python loginUi4.py
```

Một số script PowerShell trong repository có thể được dùng để chạy giao diện hoặc static server, nhưng cần kiểm tra lại đường dẫn tuyệt đối trước khi sử dụng.

## Cấu trúc thư mục

```text
Edu_App/
├── code/                 # Các module và tiện ích hỗ trợ
├── database/             # SQLite database của ứng dụng
├── email/                # Thành phần liên quan đến email
├── icons/                # Icon giao diện
├── Include/ Lib/ Scripts/# Môi trường Python Windows được lưu trong repo
├── login/                # Thành phần màn hình đăng nhập
├── requirements/         # Dependencies và font
├── resources/            # Tài nguyên runtime
├── tools/                # Công cụ hỗ trợ
├── database.py           # Khởi tạo và thao tác database
├── mainAPI-SERVER.py     # FastAPI/Uvicorn entry point
├── loginUi4.py           # Entry point giao diện đăng nhập
├── GUI.py                # Entry point giao diện chính
└── server.py             # Tiện ích static server cục bộ
```

## Database

Ứng dụng sử dụng SQLite trong thư mục `database`. Khi chạy lần đầu, hãy bảo đảm file database và schema phù hợp với phiên bản mã nguồn hiện tại.

Không commit dữ liệu người dùng thật, mật khẩu, token, private key hoặc file cấu hình chứa thông tin bí mật. Dữ liệu trong database nên được thay bằng dữ liệu mẫu trước khi chia sẻ repository.

## Cấu hình và bảo mật

- Không sử dụng tài khoản/mật khẩu được lưu trong README hoặc source code.
- Không đưa secret, private key, file `.env`, database người dùng thật hoặc thông tin email vào commit.
- API hiện được thiết kế để chạy cục bộ trên `127.0.0.1`; không mở ra mạng công cộng nếu chưa bổ sung xác thực, phân quyền và kiểm tra input.
- Các file cấu hình có đường dẫn máy cá nhân cần được thay bằng đường dẫn tương đối hoặc biến môi trường.

## Xử lý sự cố

### Không cài được dlib

Kiểm tra đúng Python 3.10 64-bit và kiến trúc Windows. Nếu vẫn lỗi, cài Visual C++ Build Tools hoặc thay file wheel bằng bản tương thích.

### API không khởi động

- Kiểm tra virtual environment đã được kích hoạt.
- Kiểm tra database tồn tại trong thư mục `database`.
- Đảm bảo port `8000` và `3003` chưa bị chương trình khác sử dụng.
- Chạy lại bằng `python mainAPI-SERVER.py` để xem log lỗi đầy đủ.

### Giao diện không tải tài nguyên

Chạy lệnh từ thư mục gốc repository để các đường dẫn tương đối tới `resources`, `icons` và `database` được resolve chính xác.

## Đóng góp

1. Tạo branch mới cho thay đổi.
2. Mô tả rõ mục tiêu và cách kiểm thử.
3. Không gửi dữ liệu cá nhân hoặc secret trong pull request.
4. Mở pull request với ảnh chụp màn hình nếu thay đổi giao diện.

## License

Repository hiện chưa khai báo license. Hãy bổ sung file `LICENSE` trước khi phân phối hoặc cho phép sử dụng lại dự án.
