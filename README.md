# Website temnhantamtinphat.com

Web tĩnh của Công ty TNHH SX TM Tâm Tín Phát.
- Sửa nội dung: `content.py` (danh mục, bài viết), `catalog.py` (bảng mã, GoDEX), `godex_list.py` (sản phẩm GoDEX).
- Ảnh: `src/img/` (ảnh thật, WebP).
- Mỗi lần đẩy lên nhánh `main`, GitHub Actions tự sinh lại web và đăng lên GitHub Pages.
- Bật phần FSC: sửa `FSC["status"]` trong `content.py` thành `"active"` và điền mã chứng chỉ.
