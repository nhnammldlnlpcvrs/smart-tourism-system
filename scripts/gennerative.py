import csv, random

places = [
    "Hà Nội", "Hồ Gươm", "Hồ Tây", "Phố cổ Hà Nội", "Làng cổ Đường Lâm", "Sa Pa", "Lào Cai",
    "Hạ Long", "Vịnh Hạ Long", "Cát Bà", "Ninh Bình", "Tràng An", "Tam Cốc", "Bái Đính",
    "Hoa Lư", "Chùa Hương", "Mai Châu", "Mộc Châu", "Sơn La", "Điện Biên", "Hà Giang",
    "Đồng Văn", "Lũng Cú", "Quản Bạ", "Bắc Kạn", "Ba Bể", "Tuyên Quang", "Thái Nguyên",
    "Hà Nam", "Nam Định", "Thái Bình", "Quảng Ninh", "Yên Bái", "Mù Cang Chải", "Lào Cai", "Lạng Sơn", "Cao Bằng",
    "Thác Bản Giốc", "Hồ Ba Bể", "Tam Đảo",

    "Huế", "Đại Nội Huế", "Lăng Tự Đức", "Đà Nẵng", "Bà Nà Hills", "Ngũ Hành Sơn", "Hội An",
    "Quảng Nam", "Mỹ Sơn", "Quảng Bình", "Phong Nha – Kẻ Bàng", "Quảng Trị", "Đồng Hới",
    "Thanh Hóa", "Sầm Sơn", "Nghệ An", "Biển Cửa Lò", "Hà Tĩnh", "Thiên Cầm",
    "Quảng Ngãi", "Bình Định", "Eo Gió", "Kỳ Co", "Phú Yên", "Ghềnh Đá Đĩa",
    "Nha Trang", "Khánh Hòa", "Cam Ranh", "Bình Thuận", "Phan Thiết", "Mũi Né",
    "Ninh Thuận", "Vịnh Vĩnh Hy", "Kon Tum", "Pleiku", "Gia Lai", "Buôn Ma Thuột", "Đắk Lắk",

    "Đà Lạt", "Lâm Đồng", "Cần Thơ", "Bạc Liêu", "Sóc Trăng", "Trà Vinh", "Bến Tre", "Vĩnh Long",
    "Cà Mau", "Đất Mũi", "Côn Đảo", "Vũng Tàu", "Long Hải", "Phan Rang", "Phú Quốc", "Kiên Giang",
    "Rạch Giá", "Hà Tiên", "An Giang", "Núi Sam", "Châu Đốc", "Long An", "Tây Ninh", "Núi Bà Đen",
    "Bình Dương", "Đồng Nai", "Hồ Trị An", "Thành phố Hồ Chí Minh", "Chợ Bến Thành", "Nhà thờ Đức Bà",

    "Vườn quốc gia Cúc Phương", "Vườn quốc gia Cát Tiên", "Vườn quốc gia Bạch Mã",
    "Vườn quốc gia Phong Nha – Kẻ Bàng", "Đảo Lý Sơn", "Đảo Nam Du", "Đảo Cù Lao Chàm",
    "Đảo Bình Ba", "Đảo Bình Hưng", "Đảo Phú Quý", "Đảo Hòn Mun", "Đảo Hòn Tằm", "Đảo Hòn Tre",
    "Đảo Cát Bà", "Đảo Cô Tô", "Đảo Quan Lạn", "Đảo Hòn Sơn", "Đảo Thạnh An",
    "Suối Tiên", "Đại Nam", "Vinpearl Land", "Sun World Hạ Long", "Asia Park", "Fansipan",
    "Thác Datanla", "Thác Pongour", "Thung lũng Tình yêu", "Cầu Vàng Đà Nẵng",
    "Nhà thờ con gà Đà Lạt", "Chợ Đà Lạt", "Chợ nổi Cái Răng", "Làng hoa Sa Đéc"
]


info_templates = [
    "Bạn có thể giới thiệu về {place} không?",
    "{place} có gì nổi tiếng vậy?",
    "Ở {place} có địa điểm nào nên ghé thăm ạ?",
    "Tôi muốn biết thêm thông tin về {place}.",
    "{place} có đặc sản gì không nhỉ?",
    "Bạn có thể kể lịch sử của {place} không?",
    "Ở {place} có phong cảnh đẹp không?",
    "{place} có gì thú vị thế?",
    "Du khách thường làm gì khi đến {place}?",
    "Review cho tôi về {place} với.",
    "Nếu tôi đến {place} thì nên đi đâu đầu tiên?",
    "{place} có bãi biển nào đẹp không?",
    "Bạn có thể gợi ý những điểm check-in đẹp ở {place} không?",
    "{place} có gần biển không?",
    "Nên đi {place} vào mùa nào là đẹp nhất?",
    "Tôi nên ở bao lâu khi đi {place}?",
    "Ở {place} có gì mới mở không?",
    "Bạn ơi, {place} có gì vui không?",
    "Có tour nào đi {place} 3 ngày 2 đêm không?",
    "Tôi muốn đi phượt {place}, có nguy hiểm không?",

    "Đặc sản nổi tiếng ở {place} là gì vậy?",
    "Có món ăn nào nhất định phải thử ở {place} không?",
    "Bạn có thể giới thiệu vài quán ăn ngon ở {place} không?",
    "Ở {place} có quán cà phê đẹp nào không?",
    "Tôi muốn ăn hải sản ở {place}, bạn gợi ý giúp nhé?",
    "{place} có món nào hợp với người ăn chay không?",
    "Giá đồ ăn ở {place} có đắt không?",
    "Có thể mua đặc sản {place} làm quà ở đâu?",
    "Món ăn truyền thống của {place} là gì?",
    "Ở {place} có chợ đêm bán đồ ăn không?",

    "Từ Hà Nội đến {place} đi bằng gì tiện nhất?",
    "Có chuyến bay nào thẳng đến {place} không?",
    "Từ Sài Gòn đi {place} mất bao lâu?",
    "Có tàu lửa đi {place} không bạn?",
    "Tôi có thể thuê xe máy ở {place} được không?",
    "Đường đến {place} có dễ đi không?",
    "Có xe buýt đi {place} không?",
    "Đi {place} vào cuối tuần có kẹt xe không?",
    "Tôi cần đặt vé tàu đi {place}, bạn biết chỗ nào uy tín không?",
    "Từ sân bay đến trung tâm {place} bao xa?",

    "Ở {place} có khách sạn nào gần trung tâm không?",
    "Bạn gợi ý giúp tôi vài homestay đẹp ở {place} nhé.",
    "Giá phòng trung bình ở {place} là bao nhiêu?",
    "Có resort nào ven biển ở {place} không?",
    "Tôi nên đặt phòng ở khu nào khi đến {place}?",
    "Có khách sạn nào ở {place} phù hợp cho gia đình không?",
    "Homestay ở {place} có phục vụ ăn sáng không?",
    "Tôi có thể cắm trại ở {place} được không?",
    "Bạn có biết chỗ nghỉ nào view đẹp ở {place} không?",
    "Ở {place} có khách sạn nào gần điểm du lịch chính không?",

    "Thời tiết ở {place} tháng này thế nào?",
    "Nếu đi {place} vào mùa mưa có sao không?",
    "Tháng mấy là mùa đẹp nhất ở {place}?",
    "Tôi nên mang gì khi đi {place} mùa này?",
    "Ở {place} có lạnh vào ban đêm không?",
    "{place} có bị ảnh hưởng bởi bão không?",
    "Mùa xuân ở {place} có gì đặc biệt?",
    "Trời có thường mưa khi đi {place} tháng 8 không?",
    "Nhiệt độ trung bình ở {place} khoảng bao nhiêu?",
    "Có nên đi {place} vào mùa hè không?",

    "Ở {place} có lễ hội gì nổi tiếng không?",
    "Lễ hội ở {place} thường diễn ra vào tháng mấy?",
    "Tôi muốn trải nghiệm văn hóa địa phương ở {place}, nên đi đâu?",
    "{place} có hoạt động truyền thống nào thú vị không?",
    "Có thể xem múa rối nước ở {place} không?",
    "Tôi nghe nói {place} có lễ hội rất đông, đúng không?",
    "Người dân {place} có phong tục đặc biệt gì?",
    "Lễ hội lớn nhất ở {place} là gì?",
    "Ở {place} có di tích lịch sử nào nên tham quan?",
    "Bạn có thể kể vài truyền thuyết liên quan đến {place} không?",

    "Bạn có thể chia sẻ kinh nghiệm du lịch {place} không?",
    "Đi {place} nên mang theo những gì?",
    "Ở {place} có cần đặt vé trước không?",
    "Tôi nên đi tour hay tự túc khi du lịch {place}?",
    "Đi {place} có an toàn cho trẻ nhỏ không?",
    "Có nên thuê hướng dẫn viên khi đi {place} không?",
    "Du lịch {place} cần lưu ý điều gì?",
    "Tôi nên đi {place} bao nhiêu ngày là hợp lý?",
    "Có thể thanh toán bằng thẻ ở {place} không?",
    "Tôi có thể đổi tiền ở đâu khi đến {place}?"
]


service_templates = [
    "Thời tiết ở {place} hôm nay thế nào?",
    "Giá vé vào {place} là bao nhiêu ạ?",
    "Ở {place} có khách sạn nào tốt không?",
    "Có tour nào đi {place} không bạn?",
    "Từ Hà Nội đi {place} mất bao lâu vậy?",
    "Tôi nên đi {place} mùa nào đẹp nhất?",
    "Có sự kiện gì đang diễn ra ở {place} không?",
    "Phí tham quan {place} là bao nhiêu vậy?",
    "Ở {place} có resort nào đẹp không ạ?",
    "Tôi muốn đặt vé đi {place}, bạn giúp được không?"
]

none_templates = [
    "Bạn có biết lập trình Python không?",
    "Cách cài đặt Visual Studio Code thế nào?",
    "GitHub là gì vậy?",
    "Tôi muốn học trí tuệ nhân tạo thì nên bắt đầu từ đâu?",
    "Học Machine Learning có khó không?",
    "Bạn có thể giải thích ChatGPT hoạt động ra sao không?",
    "Ngôn ngữ lập trình nào phổ biến nhất hiện nay?",
    "Cách tạo website bằng HTML là gì?",
    "Cách sử dụng Docker trên Windows?",
    "Kubernetes dùng để làm gì?",

    "Hôm nay có phim gì hay không?",
    "Gợi ý cho tôi vài phim Hàn Quốc nổi tiếng đi.",
    "Marvel sắp ra phim mới nào vậy?",
    "Bạn biết diễn viên Song Joong Ki không?",
    "Top 10 bộ phim hay nhất Netflix là gì?",
    "Tôi nên xem anime nào đầu tiên?",
    "Phim Titanic công chiếu năm nào?",
    "Ai đóng vai chính trong phim Avatar?",
    "Phim kinh dị nào đáng sợ nhất?",
    "Cách tải phim về điện thoại là sao?",

    "Tôi muốn nghe nhạc Lo-fi, gợi ý giúp với.",
    "Bạn thích ca sĩ nào nhất?",
    "Sơn Tùng M-TP ra bài mới chưa?",
    "Nhạc K-pop hiện nay có nhóm nào nổi bật?",
    "BLACKPINK có mấy thành viên vậy?",
    "Cách tạo playlist trên Spotify là sao?",
    "Nhạc Trịnh hay ở điểm nào?",
    "Tôi muốn nghe nhạc không lời khi học, gợi ý nhé.",
    "Có bài hát nào đang trend trên TikTok không?",
    "Bạn biết nhạc sĩ Đen Vâu không?",

    "Messi đang đá cho đội nào?",
    "World Cup tổ chức ở đâu năm nay?",
    "Việt Nam có vào được vòng loại không?",
    "Cách tính điểm trong bóng rổ là sao?",
    "Ronaldo và Messi ai giỏi hơn?",
    "Bạn có thể kể top 5 đội bóng mạnh nhất thế giới?",
    "NBA là giải gì vậy?",
    "Tôi muốn học bơi, nên bắt đầu từ đâu?",
    "Bạn biết cầu thủ Quang Hải không?",
    "Ai vô địch AFF Cup 2022?",

    "Cách nấu phở bò ngon là gì?",
    "Cách trồng cây xương rồng sao cho không chết?",
    "Tôi muốn học tiếng Nhật thì nên bắt đầu từ đâu?",
    "Bạn biết cách làm bánh flan không?",
    "Làm sao để học tốt tiếng Anh giao tiếp?",
    "Tôi nên mua xe máy hay xe đạp điện?",
    "Bạn có thể chỉ tôi cách quản lý thời gian hiệu quả?",
    "Cách tiết kiệm tiền mỗi tháng là gì?",
    "Tôi nên chọn ngành học nào trong tương lai?",
    "Có cách nào học nhanh lập trình không?",

    "Elon Musk là ai vậy?",
    "Tỷ giá đô la hôm nay bao nhiêu?",
    "Tin tức mới nhất về AI là gì?",
    "Thời tiết ở Sao Hỏa ra sao?",
    "Việt Nam đang có bao nhiêu tỉnh thành?",
    "Dân số thế giới hiện tại là bao nhiêu?",
    "Bạn nghĩ tương lai xe điện có phổ biến không?",
    "Metaverse là gì vậy?",
    "Blockchain hoạt động ra sao?",
    "Có nên đầu tư tiền ảo không?",

    "Laptop nào tốt để chơi game?",
    "Điện thoại nào chụp ảnh đẹp nhất 2025?",
    "Mua iPhone ở đâu uy tín?",
    "Tôi muốn giảm cân, nên ăn gì?",
    "Cách chăm sóc mèo con mới đẻ?",
    "Bạn có biết lập trình Arduino không?",
    "Cách sửa lỗi máy tính không vào mạng?",
    "Bạn có thể kể truyện cười được không?",
    "Cách tắt chế độ Dark Mode trên Windows?",
    "Tôi nên mua bàn phím cơ loại nào tốt?"
]


rows = []
for _ in range(3500):
    place = random.choice(places)
    rows.append([random.choice(info_templates).format(place=place), "info"])
for _ in range(3500):
    rows.append([random.choice(none_templates), "none"])

random.shuffle(rows)

with open("../backend/data/intents.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "label"])
    writer.writerows(rows)

print("File intents.csv đã được tạo.")