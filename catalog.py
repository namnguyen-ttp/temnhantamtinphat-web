# -*- coding: utf-8 -*-
"""Danh mục sản phẩm theo 3 nhóm. Nguồn: Danh mục hàng + kho phôi xưởng TTP (11/2026) và các quy cách phổ biến trên thị trường.
Tình trạng: "sẵn" = hàng xưởng đang làm sẵn; "bế" = nhận bế theo yêu cầu."""

GROUPS = [
 {"slug": "san-pham-tem-be-trang", "name": "Tem bế trắng", "kind": "trang",
  "title": "Bảng mã tem bế trắng, decal nhiệt, decal giấy, giấy in bill có sẵn | Tâm Tín Phát",
  "desc": "Bảng mã tem bế trắng có sẵn tại xưởng: decal nhiệt 35x22, 40x30, 50x30, 58x40 lõi cân, 75x100, 100x150; decal giấy in ruy băng; giấy in bill K57, K80, K110. Nhận bế mọi kích thước.",
  "h1": "Tem bế trắng: đủ mã, có sẵn, nhận bế mọi khổ",
  "lead": "Decal nhiệt, decal giấy in ruy băng, tem vận đơn, tem cân và giấy in bill. Hàng có sẵn giao ngay, kích thước lạ xưởng bế riêng.",
  "cats": ["tem-nhan-trang", "giay-in-nhiet-giay-in-bill"]},
 {"slug": "san-pham-tem-mau", "name": "Tem nhãn màu", "kind": "mau",
  "title": "Các loại tem nhãn in màu: mỹ phẩm, thực phẩm, trà sữa, trang sức, xi bạc | Tâm Tín Phát",
  "desc": "Tổng hợp các loại tem nhãn in màu đang dùng trên thị trường: tem logo, mỹ phẩm, thực phẩm, chai nước, ly trà sữa, đông lạnh, trang sức, tem cân in sẵn logo, decal vỡ, xi bạc. In 1–6 màu, cán màng, bế hình.",
  "h1": "Tem nhãn màu cho mọi ngành hàng",
  "lead": "In 1–6 màu trên decal giấy, decal nhựa, decal trong, xi bạc hay decal vỡ. Cán màng bóng hoặc mờ, bế đúng hình logo. Chọn loại tem theo sản phẩm của anh/chị.",
  "cats": ["tem-nhan-mau", "decal-nhua-decal-trong", "decal-vo-tem-bao-hanh", "tem-nhan-theo-nganh", "tem-nhan-giay-fsc"]},
 {"slug": "thiet-bi-godex", "name": "Thiết bị GoDEX", "kind": "godex",
  "title": "Máy in mã vạch GoDEX: để bàn, công nghiệp, di động, ruy băng, đầu in | Tâm Tín Phát",
  "desc": "Máy in mã vạch GoDEX chính hãng: RT700, RT730, HD830i+, DT41, EZ520+, ZX430i+, ZX1200Xi Pro, GX4600i Pro, EZ6250i, MX30i. Ruy băng mực, đầu in thay thế. Bảo hành 12 tháng.",
  "h1": "Máy in mã vạch GoDEX chính hãng",
  "lead": "Một nơi mua cả máy in, tem và mực: máy GoDEX để bàn, công nghiệp, cầm tay, kèm decal đúng khổ và ruy băng phù hợp. Cài đặt, hướng dẫn in tem tận nơi.",
  "cats": []},
]

# ---------- Tem bế trắng ----------
# (mã, nhóm, tên, kích thước mm, cuộn, tem/hàng, đóng gói, tình trạng, dùng cho)
WHITE = [
 ("DN-3522-25-2", "nhiet", "Decal nhiệt 35×22", "35 × 22", "25 m", "2", "Thùng 100 cuộn", "sẵn", "Tem giá, phụ kiện nhỏ"),
 ("DN-3522-30-2", "nhiet", "Decal nhiệt 35×22", "35 × 22", "30 m", "2", "Thùng 100 cuộn", "sẵn", "Tem giá, phụ kiện nhỏ"),
 ("DN-4030-30-1", "nhiet", "Decal nhiệt 40×30", "40 × 30", "30 m", "1", "Thùng 100 cuộn", "sẵn", "Mã vạch bán lẻ"),
 ("DN-5030-25-1", "nhiet", "Decal nhiệt 50×30", "50 × 30", "25 m", "1", "Thùng 100 cuộn", "sẵn", "Mã vạch hàng hóa, kho"),
 ("DN-5030-30-1", "nhiet", "Decal nhiệt 50×30", "50 × 30", "30 m", "1", "Thùng 100 cuộn", "sẵn", "Mã vạch hàng hóa, kho"),
 ("DN-5030-50-1", "nhiet", "Decal nhiệt 50×30", "50 × 30", "50 m", "1", "Thùng 40 cuộn", "sẵn", "Kho, siêu thị"),
 ("DN-5030-50-2", "nhiet", "Decal nhiệt 50×30", "50 × 30", "50 m", "2", "Thùng 40 cuộn", "sẵn", "Máy in khổ rộng"),
 ("DN-5050-25-1", "nhiet", "Decal nhiệt 50×50", "50 × 50", "25 m", "1", "Thùng 100 cuộn", "sẵn", "Tem vuông, QR code"),
 ("DN-5840-30-LC", "nhiet", "Decal nhiệt 58×40 lõi cân", "58 × 40", "30 m", "1", "Thùng 100 cuộn", "sẵn", "Cân điện tử siêu thị"),
 ("DN-6040-30-1", "nhiet", "Decal nhiệt 60×40", "60 × 40", "30 m", "1", "Thùng 47 cuộn", "sẵn", "Tem có tên hàng, giá"),
 ("DN-7050-30-1", "nhiet", "Decal nhiệt 70×50", "70 × 50", "30 m", "1", "Thùng 100 cuộn", "sẵn", "Tem thùng nhỏ"),
 ("DN-7850-30-1", "nhiet", "Decal nhiệt 78×50", "78 × 50", "30 m", "1", "Thùng 100 cuộn", "sẵn", "Tem thông tin sản phẩm"),
 ("DN-8080-30-1", "nhiet", "Decal nhiệt 80×80", "80 × 80", "30 m", "1", "Thùng 100 cuộn", "sẵn", "Tem thùng, tem kệ"),
 ("DN-76LT-30", "nhiet", "Decal nhiệt liên tục khổ 76", "76 × liên tục", "30 m", "—", "Thùng 100 cuộn", "sẵn", "Máy cân, in độ dài tùy ý"),
 ("DN-75100-30-1", "van", "Decal nhiệt 75×100", "75 × 100", "30 m", "1", "Thùng 100 cuộn", "sẵn", "Vận đơn khổ nhỏ"),
 ("DN-75100-300", "van", "Decal nhiệt 75×100 cuộn 300 tem", "75 × 100", "300 tem", "1", "Thùng 100 cuộn", "sẵn", "Vận đơn A7"),
 ("DN-75105-X500", "van", "Decal nhiệt 75×105 xấp gấp", "75 × 105", "Xấp 500 tem", "1", "Thùng 50 xấp", "sẵn", "Vận đơn, máy in kho"),
 ("DN-75100-X500", "van", "Decal nhiệt 75×100 xấp gấp", "75 × 100", "Xấp 500 tem", "1", "Thùng 20 xấp", "sẵn", "Vận đơn A7"),
 ("DN-100150-350", "van", "Decal nhiệt 100×150", "100 × 150", "350 tem", "1", "Thùng 30 cuộn", "sẵn", "Vận đơn TMĐT"),
 ("DN-100150-50-1", "van", "Decal nhiệt 100×150", "100 × 150", "50 m", "1", "Thùng 40 cuộn", "sẵn", "Vận đơn số lượng lớn"),
 ("DN-100150-X500", "van", "Decal nhiệt 100×150 xấp gấp", "100 × 150", "Xấp 500 tem", "1", "Thùng 20 xấp", "sẵn", "Vận đơn A6, máy in kho"),
 ("DG-3522-50-3", "giay", "Decal giấy 35×22", "35 × 22", "50 m", "3", "Thùng 40 cuộn", "sẵn", "Tem mã vạch in ruy băng"),
 ("DG-5030-50-2", "giay", "Decal giấy 50×30", "50 × 30", "50 m", "2", "Thùng 40 cuộn", "sẵn", "Tem sản phẩm lưu kho lâu"),
 ("DG-10050-50-1", "giay", "Decal giấy 100×50", "100 × 50", "50 m", "1", "Thùng 40 cuộn", "sẵn", "Tem thùng, tem kệ"),
 ("DG-100100-50-1", "giay", "Decal giấy 100×100", "100 × 100", "50 m", "1", "Thùng 40 cuộn", "sẵn", "Tem thùng carton"),
 ("DG-100150-50-1", "giay", "Decal giấy 100×150", "100 × 150", "50 m", "1", "Thùng 40 cuộn", "sẵn", "Tem vận chuyển bền"),
 ("DG-80110-100-DM", "giay", "Decal giấy 80×110 bế demi", "80 × 110", "100 m", "1", "Theo đơn", "sẵn", "Tem pallet, tem thùng"),
 ("TS-DUOI-GAP", "dac", "Tem trang sức đuôi gập (tem vàng)", "Theo mẫu", "Cuộn", "1", "Theo đơn", "sẵn", "Tiệm vàng, trang sức, kính mắt"),
 ("BN-K5738", "bill", "Giấy in nhiệt K57", "Khổ 57, Ø38", "Cuộn", "—", "Thùng 100 cuộn", "sẵn", "Máy POS cầm tay"),
 ("BN-K8045", "bill", "Giấy in nhiệt K80", "Khổ 80, Ø45", "Cuộn", "—", "Thùng 100 cuộn", "sẵn", "Máy in hóa đơn quán"),
 ("BN-K8065", "bill", "Giấy in nhiệt K80", "Khổ 80, Ø65", "Cuộn", "—", "Thùng 50–100 cuộn", "sẵn", "Siêu thị, nhà hàng"),
 ("BN-K8080", "bill", "Giấy in nhiệt K80", "Khổ 80, Ø80", "Cuộn", "—", "Thùng 50 cuộn", "sẵn", "Siêu thị đông khách"),
 ("BN-K11045", "bill", "Giấy in nhiệt K110", "Khổ 110, Ø45", "Cuộn", "—", "Thùng 50 cuộn", "sẵn", "Máy in khổ rộng"),
 ("BK-K75-30", "bill", "Giấy in kim 2 liên K75", "Khổ 75", "30 m", "—", "Thùng 100 cuộn", "sẵn", "Máy in kim, phiếu 2 liên"),
 ("BK-K75-50", "bill", "Giấy in kim 2 liên K75", "Khổ 75", "50 m", "—", "Thùng 100 cuộn", "sẵn", "Máy in kim, phiếu 2 liên"),
]
WHITE_FILTERS = [("nhiet", "Decal nhiệt"), ("van", "Tem vận đơn"), ("giay", "Decal giấy (ruy băng)"), ("dac", "Tem đặc biệt"), ("bill", "Giấy in bill")]
# Kích thước thị trường hay đặt, xưởng nhận bế riêng
BESPOKE = ["20 × 10", "25 × 15", "30 × 15", "30 × 20", "40 × 20", "40 × 25", "50 × 20", "50 × 25", "50 × 40", "60 × 30", "70 × 30", "70 × 40", "100 × 30", "100 × 70", "100 × 75", "Tròn Ø20–Ø60", "Theo bản vẽ của khách"]

MATERIALS = [
 ("Decal nhiệt (giấy)", "In nhiệt trực tiếp, không cần ruy băng", "Vận đơn, tem giá, tem kho dùng ngắn ngày"),
 ("Decal nhiệt PP", "Nền nhựa in nhiệt, chống nước, chống rách", "Hàng lạnh, hàng gặp nước"),
 ("Decal nhiệt remove", "Bóc ra không để lại keo", "Tem tạm, dán lên hàng mới, kính"),
 ("Decal giấy thường", "In bằng ruy băng hoặc in màu, chữ bền", "Tem sản phẩm, tem thùng lưu kho lâu"),
 ("Decal PP trắng", "Nhựa dẻo, chống nước, bám bề mặt cong", "Chai lọ, mỹ phẩm, đồ uống"),
 ("Decal PP đông lạnh", "Keo chịu lạnh sâu, không bong khi đọng nước", "Thủy sản, thịt, hàng tủ đông"),
 ("Decal PP nữ trang", "Mỏng, dai, gấp đôi quanh móc", "Tem vàng, tem trang sức"),
 ("Decal PP remove", "Nhựa, bóc sạch không để keo", "Thiết bị điện tử, kính, đồ gia dụng"),
 ("Decal xi bạc", "Ánh kim loại, bền nhiệt", "Tem thông số máy, tem cao cấp"),
 ("Decal vỡ", "Bóc là vỡ vụn", "Tem bảo hành, niêm phong"),
]

# ---------- Tem nhãn màu: các loại trên thị trường ----------
# (loại, chất liệu khuyên dùng, kích thước hay dùng, hoàn thiện, link danh mục)
COLOR_TYPES = [
 ("Tem logo shop, thương hiệu", "Decal giấy hoặc PP", "Tròn Ø30–Ø50, chữ nhật 50×30", "In 2–6 màu, cán bóng hoặc mờ", "tem-nhan-mau"),
 ("Tem mỹ phẩm (chai, hũ, tuýp)", "Decal PP trắng, PP trong, xi bạc", "Theo thân chai, thường 40–90 mm", "Cán mờ, bế bo góc", "decal-nhua-decal-trong"),
 ("Tem thực phẩm, bánh kẹo, nông sản", "Decal giấy, PP", "60×40, 80×50, 100×70", "In màu đủ thông tin nhãn", "tem-nhan-theo-nganh"),
 ("Tem chai nước, đồ uống", "Decal PP chống nước", "Quấn thân chai", "Cán màng, chịu ẩm", "decal-nhua-decal-trong"),
 ("Tem ly trà sữa, cà phê", "Decal PP", "Tròn Ø40–Ø60", "In logo nhiều màu", "tem-nhan-mau"),
 ("Tem hàng đông lạnh, thủy sản", "Decal PP đông lạnh", "Theo khay, túi", "Keo chịu lạnh", "tem-nhan-theo-nganh"),
 ("Tem trang sức, tem vàng", "Decal PP nữ trang", "Tem đuôi gập quanh móc", "In logo, chừa ô in giá", "tem-nhan-theo-nganh"),
 ("Tem cân điện tử in sẵn logo", "Decal nhiệt", "58×40 lõi cân và theo máy cân", "In sẵn khung màu, phần trắng in nhiệt", "tem-nhan-trang"),
 ("Tem vận đơn in sẵn logo shop", "Decal nhiệt", "100×150, 75×100", "In logo, phần trắng in vận đơn", "tem-nhan-trang"),
 ("Tem bảo hành, niêm phong", "Decal vỡ", "Tròn Ø8–Ø15, chữ nhật", "In logo, ô ghi ngày", "decal-vo-tem-bao-hanh"),
 ("Tem bóc không để lại keo", "Decal PP remove", "Theo sản phẩm", "In màu, keo remove", "decal-nhua-decal-trong"),
 ("Tem xi bạc, tem thông số máy", "Decal xi bạc", "Theo thiết bị", "In đen hoặc màu trên nền bạc", "decal-nhua-decal-trong"),
]
COLOR_OPTIONS = [
 ("Số màu in", "1 màu, 2 màu, 3–4 màu, 5–6 màu"),
 ("Cách lên màu", "Pha màu theo mã Pantone hoặc in 4 màu CMYK"),
 ("Màu nền", "Trắng, trong suốt, xi bạc"),
 ("Hoàn thiện", "Cán màng bóng, cán màng mờ, không cán"),
 ("Hình dạng", "Tròn, oval, vuông, chữ nhật bo góc, theo hình logo"),
 ("Quy cách giao", "Cuộn (hợp máy dán, máy in) hoặc tờ (dán tay)"),
]

# ---------- Thiết bị GoDEX (máy xưởng đang có trong danh mục) ----------
# (model, nhóm, độ phân giải, kiểu in, khổ, ghi chú, dùng cho)
# Thông số theo brochure/tài liệu chính hãng GoDEX (tra 24/11/2026). "—" = chưa có số chính thức.
# (model, nhóm, dpi, kiểu in, tốc độ, khổ in tối đa, kết nối/điểm nổi bật, dùng cho, ảnh)
GODEX = [
 ("GoDEX RT700", "ban", "203 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "108 mm (4,25\")", "Ruy băng 300 m, cuộn tem Ø127 mm", "Shop, kho, siêu thị", ""),
 ("GoDEX RT730", "ban", "300 dpi", "Nhiệt trực tiếp + ruy băng", "4 ips (102 mm/s)", "105,7 mm (4,16\")", "Chữ nét cho tem nhỏ", "Tem trang sức, linh kiện", ""),
 ("GoDEX RT730i Pro", "ban", "300 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "105,7 mm (4,16\")", "Màn hình màu, USB, RS-232, Ethernet, USB Host", "Văn phòng, kho, y tế", ""),
 ("GoDEX GM620 Pro", "ban", "203 dpi", "Nhiệt trực tiếp + ruy băng", "8 ips (203 mm/s)", "108 mm (4,25\")", "16 GB Flash, 512 MB RAM, USB, RS-232, Ethernet", "Bán lẻ, kho", ""),
 ("GoDEX GM630 Pro", "ban", "300 dpi", "Nhiệt trực tiếp + ruy băng", "6 ips (152 mm/s)", "108 mm (4,25\")", "16 GB Flash, 512 MB RAM, USB, RS-232, Ethernet", "Tem sản phẩm, tem nhỏ", ""),
 ("GoDEX EZ520+", "ban", "203 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "108 mm (4,25\")", "Phổ thông, in liên tục ổn định", "Sản xuất nhỏ, kho", ""),
 ("GoDEX EZ530+", "ban", "300 dpi", "Nhiệt trực tiếp + ruy băng", "4 ips (102 mm/s)", "105,7 mm (4,16\")", "Phổ thông, chữ nét", "Tem sản phẩm", ""),
 ("GoDEX DT41", "ban", "203 dpi", "Nhiệt trực tiếp (không ruy băng)", "5 ips (127 mm/s)", "104 mm", "Nhỏ gọn, siêu nhẹ, cổng USB", "Vận đơn TMĐT", ""),
 ("GoDEX ZX430i+", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "105,7 mm (4,16\")", "Khung đúc kim loại, ruy băng 450 m", "Nhà máy, logistics", ""),
 ("GoDEX ZX1200Xi Pro", "cn", "203 dpi", "Nhiệt trực tiếp + ruy băng", "14 ips (356 mm/s)", "104 mm", "Ruy băng 450 m, CPU 32-bit RISC", "Nhà máy, kho lớn", ""),
 ("GoDEX ZX1300Xi Pro", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "—", "105,7 mm", "Công nghiệp tốc độ cao, chữ nét", "Nhà máy FDI", ""),
 ("GoDEX GX4200i Pro", "cn", "203 dpi", "Nhiệt trực tiếp + ruy băng", "16 ips (406 mm/s)", "104 mm", "Màn hình cảm ứng 5\", khung nhôm đúc", "Logistics, sản xuất", ""),
 ("GoDEX GX4300i Pro", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "12 ips (305 mm/s)", "105,7 mm", "Màn hình cảm ứng 5\", khung nhôm đúc", "Tem linh kiện, điện tử", ""),
 ("GoDEX GX4600i Pro", "cn", "600 dpi", "Ruy băng (in chuyển nhiệt)", "8 ips (203 mm/s)", "105,6 mm", "16 GB Flash, 2 GB RAM, cảm ứng 5\"", "Linh kiện điện tử, PCB", ""),
 ("GoDEX EZ6250i", "cn", "203 dpi", "Nhiệt trực tiếp + ruy băng", "7 ips (177 mm/s)", "168 mm (6,61\")", "Khổ rộng, ruy băng 450 m, cuộn tem Ø8\"", "Tem thùng, pallet lớn", ""),
 ("GoDEX EZ6350i", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "168 mm (6,61\")", "Khổ rộng, chữ nét", "Tem thùng, tem hóa chất", ""),
 ("GoDEX HD830i+", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "219,5 mm (8,64\")", "Khổ 8 inch, 256 MB bộ nhớ", "Tem khổ lớn, pallet, công trình", ""),
 ("GoDEX MX30i", "dd", "203 dpi", "Nhiệt trực tiếp", "4 ips (102 mm/s)", "72 mm (2,8\")", "Pin Li-ion, Bluetooth, USB, RS-232, nặng ~670 g", "Giao hàng, kiểm kho", ""),
]

# Thông số bổ sung cho các model khác trên namnguyeninfotech.com (theo brochure GoDEX)
GODEX += [
 ("GoDEX RT700i+", "ban", "203 dpi", "Nhiệt trực tiếp + ruy băng", "7 ips (178 mm/s)", "108 mm (4,25\")", "Màn hình màu, 3 cổng USB Host, Ethernet", "Bán lẻ, kho", ""),
 ("GoDEX RT730i+", "ban", "300 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "105,7 mm (4,16\")", "Màn hình màu, Ethernet", "Tem nhỏ, chữ nét", ""),
 ("GoDEX RT730i", "ban", "300 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "105,7 mm (4,16\")", "USB, RS-232, Ethernet", "Bán lẻ", ""),
 ("GoDEX ZX420i+", "cn", "203 dpi", "Nhiệt trực tiếp + ruy băng", "6 ips (152 mm/s)", "108 mm (4,25\")", "Khung đúc kim loại, ruy băng 450 m", "Nhà máy", ""),
 ("GoDEX ZX420i", "cn", "203 dpi", "Nhiệt trực tiếp + ruy băng", "6 ips (152 mm/s)", "108 mm (4,25\")", "Ruy băng 450 m", "Nhà máy", ""),
 ("GoDEX ZX430i", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "4 ips (102 mm/s)", "105,7 mm (4,16\")", "Ruy băng 450 m", "Nhà máy", ""),
 ("GoDEX GX4600i", "cn", "600 dpi", "Ruy băng (in chuyển nhiệt)", "8 ips (203 mm/s)", "104 mm", "Màn hình 5\"", "Linh kiện điện tử", ""),
 ("GoDEX EZ2250i", "cn", "203 dpi", "Nhiệt trực tiếp + ruy băng", "7 ips (177 mm/s)", "104 mm", "Ruy băng 450 m", "Nhà máy, kho", ""),
 ("GoDEX EZ2350i", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "104 mm", "Ruy băng 450 m", "Nhà máy", ""),
 ("GoDEX HD830i", "cn", "300 dpi", "Nhiệt trực tiếp + ruy băng", "4 ips (102 mm/s)", "219,5 mm (8,64\")", "Khổ 8 inch, màn hình cảm ứng", "Tem khổ lớn", ""),
 ("GoDEX MX30", "dd", "203 dpi", "Nhiệt trực tiếp", "4 ips (102 mm/s)", "72 mm (2,8\")", "Pin Li-ion, Bluetooth", "Giao hàng, kiểm kho", ""),
 ("GoDEX G500", "ban", "203 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "108 mm (4,25\")", "Ruy băng 300 m", "Shop, kho", ""),
 ("GoDEX GE300", "ban", "203 dpi", "Nhiệt trực tiếp + ruy băng", "5 ips (127 mm/s)", "108 mm", "Phổ thông", "Shop", ""),
 ("GoDEX GE330", "ban", "300 dpi", "Nhiệt trực tiếp + ruy băng", "4 ips (102 mm/s)", "105,7 mm", "Phổ thông, chữ nét", "Shop", ""),
]

GODEX_FILTERS = [("ban", "Để bàn"), ("cn", "Công nghiệp"), ("dd", "Cầm tay")]
SUPPLIES = [
 ("Ruy băng Wax/Resin 110 mm × 300 m", "Dòng Premium, in trên decal giấy, bám tốt", "Tem sản phẩm, tem kho"),
 ("Ruy băng Resin 110 mm × 300 m", "Chống trầy, chống cồn, hóa chất", "Decal nhựa PP, xi bạc, tem linh kiện"),
 ("Ruy băng Resin 80 mm × 100 m", "Cuộn nhỏ cho máy để bàn", "Tem nhựa khổ nhỏ"),
 ("Đầu in thay thế dòng G500 / RT700 / DT4 / GE300 / EZ520", "Đầu in 203 dpi chính hãng", "Thay khi đầu in mòn"),
 ("Đầu in ZX430i+, ZX1300Xi Pro, HD830i+, GX420i Pro", "Đầu in cho máy công nghiệp", "Bảo trì máy nhà máy"),
 ("Dao cắt (cutter) cho G500 / EZ500+", "Cắt tem tự động sau khi in", "Tem rời, tem không bế"),
 ("Máy cuốn tem T-10 Rewinder", "Cuốn lại tem sau khi in thành cuộn gọn", "Nhà máy in tem số lượng lớn"),
 ("Module RFID cho GX400i Pro", "Nâng máy GX400i Pro lên in và mã hóa tem RFID", "Kho, logistics dùng RFID"),
 ("Linh kiện: trục cao su (platen), dẫn cuộn tem", "Phụ tùng thay thế", "Sửa chữa, bảo trì"),
]

# Ảnh thật tại kho (đã chỉnh màu, gắn nhãn) — file trong src/img
PHOTOS_WHITE = [
 ("banner-sale-35x22", "Khuyến mãi decal 35×22×30 m"),
 ("thung-decal-tem-nhiet", "Thùng Decal tem nhiệt"),
 ("cuon-35x22x25", "Decal nhiệt 35×22, cuộn 25 m"),
 ("cuon-35x22-duong-kinh", "Cuộn 35×22 lõi 1 inch"),
 ("tem-35x22-thuoc", "Tem 35×22 đo bằng thước"),
 ("tem-35x22-ke-sat", "Tem 35×22 bo góc"),
 ("thung-cuon-100x150", "Thùng cuộn 100×150"),
 ("tem-100x150-thuoc", "Tem vận đơn 100×150 đo thực tế"),
 ("tem-trang-suc", "Tem trang sức đuôi gập"),
 ("a6-cuon-100x150x350", "Decal nhiệt 100×150, cuộn 350 tem"),
 ("thung-100x150x350", "Thùng 30 cuộn 100×150"),
 ("a7-cuon-75x100x300", "Decal nhiệt 75×100, cuộn 300 tem"),
 ("thung-75x100x300", "Thùng 100 cuộn 75×100"),
 ("a7-xap-75x105x500", "Decal nhiệt 75×105 xấp gấp 500 tem"),
 ("thung-75x105x500", "Thùng 50 xấp 75×105"),
 ("cuon-35x22x30", "Decal nhiệt 35×22, cuộn 30 m"),
 ("tem-2-hang-thuoc-do", "Tem 35×22, 2 tem mỗi hàng"),
 ("tem-1-hang-thuoc-do", "Tem bế sẵn bo góc"),
 ("nhiet-lien-tuc-76", "Decal nhiệt liên tục khổ 76"),
 ("thung-nhiet-lien-tuc-76", "Thùng 100 cuộn decal 76 liên tục"),
 ("thung-cuon-decal", "Cuộn decal bọc màng trong thùng"),
]
