-- SQLite
INSERT INTO auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name)
VALUES (1,'pbkdf2_sha256$720000$8wZKZEe31qp8ksJmRbbiK5$DDGXvU84gs27n7L94NdJGjGC+zO/ZKEj3C/yn0FDII8=','2024-05-21 01:51:04.381058',1,'admin','','vuvananh010203@gmail.com',1,1,'2024-05-21 01:11:12.761545','');
INSERT INTO auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name)
VALUES (2,'pbkdf2_sha256$720000$8wZKZEe31qp8ksJmRbbiK5$DDGXvU84gs27n7L94NdJGjGC+zO/ZKEj3C/yn0FDII8=','2024-05-21 01:51:04.381058',0,'customer1','','example123@gmail.com',0,1,'2024-05-21 01:11:12.761545','');


INSERT INTO WebApp_parentcategories (id, ParentCategoryName)
VALUES (1,'IPhone');
INSERT INTO WebApp_parentcategories (id, ParentCategoryName)
VALUES (2,'SamSung');
INSERT INTO WebApp_parentcategories (id, ParentCategoryName)
VALUES (3,'Xiaomi');
INSERT INTO WebApp_parentcategories (id, ParentCategoryName)
VALUES (4,'Sạc dự phòng');
INSERT INTO WebApp_parentcategories (id, ParentCategoryName)
VALUES (5,'Củ, cáp sạc');

INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id)
VALUES (1, 'Iphone 15 Pro Max',1);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id)
VALUES (2, 'Iphone 15 Pro',1);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id)
VALUES (3, 'Iphone 15 Plus',1);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id)
VALUES (4, 'Iphone 15',1);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (5, 'Samsung Galaxy S24 Ultra', 2);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (6, 'Samsung Galaxy S23 Ultra', 2);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (7, 'Samsung Galaxy S22 Ultra', 2);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (8, 'Xiaomi Poco X6 Pro', 3);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (9, 'Xiaomi Poco M6 Pro', 3);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (10, 'Sạc dự phòng 10000 mAh', 4);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (11, 'Sạc dự phòng 20000 mAh', 4);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (12, 'Cáp sạc Apple', 5);
INSERT INTO WebApp_categories (id, CategoryName, ParentCategoryID_id) 
VALUES (13, 'Cáp sạc Samsung', 5);


INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (1,'Ốp lưng da iPhone 15 Pro Max HDD Produce (đa năng, có ngăn đựng thẻ, kệ chống lưng)',330000,25,'static/images/product/1715946324938.jpg','Ốp lưng da iPhone 15 Pro Max HDD Produce là sản phẩm mới nhất của thương hiệu HDD Produce, được thiết kế dành riêng cho iPhone 15 Pro Max. Ốp lưng có thiết kế sang trọng, thời trang, với nhiều tính năng hữu ích giúp bảo vệ iPhone của bạn khỏi trầy xước, va đập và bụi bẩn.',1);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (2,'Kính cường lực Nillkin H+ Pro cho iPhone 15 Pro Max cao cấp (trong suốt, mỏng 0.2mm, mài cạnh 2.5D)',250000,28,'static/images/product/1715946324939.jpg','Kính cường lực Nillkin H+ Pro cho iPhone 15 Pro Max cao cấp (trong suốt, mỏng 0.2mm, mài cạnh 2.5D) là một sản phẩm chất lượng cao, được thiết kế dành riêng cho chiếc điện thoại iPhone 15 Pro Max mới nhất của Apple. Kính được làm từ chất liệu kính cường lực AGC nhập khẩu từ Nhật Bản, có độ cứng lên đến 9H, giúp bảo vệ màn hình khỏi bị trầy xước, va đập. Kính được thiết kế trong suốt, giúp hiển thị hình ảnh rõ nét, không bị biến dạng. Kính có độ mỏng chỉ 0,2mm, tạo cảm giác cầm nắm thoải mái, không bị cộm. Kính được mài cạnh 2.5D, giúp ôm sát màn hình, hạn chế tình trạng cấn tay khi sử dụng. Kính được phủ lớp oleophobic chống bám vân tay và dầu mỡ, giúp màn hình luôn sạch sẽ, dễ dàng vệ sinh. Kính được dán dễ dàng, không gây bọt khí',1);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (3,'Ốp lưng iPhone 15 Pro chính hãng Nillkin CarboProp Magnetic Case (hỗ trợ sạc từ không dây magsafe)',660000,30,'static/images/product/1715946324940.jpg','Ốp lưng iPhone 15 Pro chính hãng Nillkin CarboProp Magnetic Case (hỗ trợ sạc từ không dây MagSafe). Ốp lưng iPhone 15 Pro chính hãng Nillkin CarboProp Magnetic Case là sản phẩm mới nhất của thương hiệu Nillkin, được thiết kế dành riêng cho dòng iPhone 15 Pro. Ốp lưng được làm từ chất liệu cao cấp, mang đến khả năng bảo vệ tối ưu cho điện thoại, đồng thời hỗ trợ sạc từ không dây MagSafe tiện lợi.',2);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (4,'Ốp lưng kính chính hãng HODA Crystal Pro cho iPhone 15 Pro. Hàng cao cấp.',800000,6,'static/images/product/1715946324941.jpg','Vật liệu: TPU, Kính. Độ dày: 2.44mm. Đạt tiêu chuẩn của quân đội. Độ bền gấp 2 lần. Hạn chế bám vân tay. Bao phủ cạnh. Chất liệu TPU cao cấp từ Bayer Đức.',2);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (5,'Ốp lưng iPhone 15 Plus chính hãng Mentor VII Pocard cao cấp.',870000,20,'static/images/product/1715946324942.jpg',' Đây là sản phẩm thuộc dòng cao cấp với thiết kế khe đựng card, thẻ, tiền.. rất tiện lợi. Ốp da Mentor VII phần ốp lưng với thiết kế khung nhựa TPU mềm ôm toàn diện góc cạnh máy.',3);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (6,'Ốp lưng iPhone 15 Plus hãng X-LEVEL trong màu hỗ trợ sạc không dây Magsafe. Chống sốc, bảo vệ Camera.',250000,28,'static/images/product/1715946324943.jpg','Ốp mỏng 0.88mm chất liệu PC hỗ trợ sạc không dây.. Gờ cao giúp bảo vệ Camera khi tiếp xúc với mặt bàn.. Ốp mỏng, gọn, đẹp, đem lại cảm giác cầm vừa vặn, gọn tay.. Bảo vệ máy tránh bị xước, va đạp mạnh.',3);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (7,'Kính cường lực chống nhìn trộm Nillkin Guardian iPhone 15. Hàng cao cấp, chính hãng.',300000,17,'static/images/product/1715946324944.jpg','Sử dụng công ty AGC Glass liệu nhập khẩu từ Nhật Bản với phòng thủ tuyệt vời.. Lớp phủ riêng tư hoàn toàn mới, bảo vệ sự riêng tư của bạn.. Che phủ với lớp phủ chống chói có hiệu quả có thể ngăn chặn sự ánh sáng chói mắt xảy ra.',4);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (8,'Kính cường lực chống vân tay có bảo vệ màng loa WIWU iVista cho iPhone 15. Hàng cao cấp chính hãng.',230000,30,'static/images/product/1715946324945.jpg','Kính cường lực chống vân tay có bảo vệ màng loa WIWU iVista. Giúp cho màn hình luôn trong trạng thái sạch sẽ, không bị đục màu. Miếng dán này có độ chống lóa rất rốt. Khi ở ngoài trời thì loại này hạn chế tối đa dấu vân tay và giảm được lượng nhiệt ánh sáng mặt trời. Điều này giúp điện thoại không bị phản ngược và ánh sáng, không bị chói mắt. Được thiết kế rất mỏng nhẹ, tinh tế được bo xung quanh đường viền, thân máy. Điều đó hạn chế cho việc cạnh viền bị hở, bụi bặm lọt vào trong.',4);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (9,'Miếng dán mặt lưng Samsung S24 Ultra PPF (Dán đàn hồi, siêu mỏng)',130000,46,'static/images/product/1715946324946.jpg','Chống trầy xước, va đập hiệu quả. Giữ nguyên vẻ đẹp nguyên bản của điện thoại. Mỏng nhẹ, không ảnh hưởng đến kích thước hay trọng lượng của điện thoại. Dễ dàng dán và thay thế.',5);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (10,'Dán Lens Camera Samsung S24 Ultra chính hãng Kuzoom ( bảo vệ camera chống vỡ, xước)',230000,43,'static/images/product/1715946324947.jpg','Chất liệu cao cấp, bền bỉ. Thiết kế full màn, trong suốt. Chống vỡ, chống xước. Dễ dán.',5);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (11,'Ốp lưng Samsung S23 Ultra chính hãng Memumi (Mica trong suốt, siêu mỏng)',200000,25,'static/images/product/1715946324948.jpg','Ốp lưng Samsung S23 Ultra chính hãng Memumi là sản phẩm ốp lưng cao cấp dành cho dòng điện thoại Samsung Galaxy S23 Ultra. Sản phẩm được thiết kế với chất liệu mica trong suốt, giúp khoe trọn vẻ đẹp của chiếc điện thoại. Ngoài ra, ốp lưng còn có độ dày chỉ 0,3mm, siêu mỏng, không gây cản trở khi sử dụng điện thoại.',6);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (12,'Kính cường lực full màn hình Samsung Galaxy S23 Ultra 3D CP+MAX chính hãng NILLKIN',350000,20,'static/images/product/1715946324949.jpg','Được lựa chọn và sử dụng vật liệu thủy tinh AGC nhập khẩu từ Nhật Bản và công nghệ nano HARVES với hiệu suất bảo vệ tuyệt vời.. Nó sở hữu độ truyền qua siêu cao và khả năng khôi phục màu gốc của màn hình cao.. Nó hỗ trợ lớp phủ chống chói để ngăn chặn ánh sáng chói.',6);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (13,'Bao da Samsung S22 Ultra cao cấp chính hãng Nillkin Qin có nắp trượt bảo vệ camera',300000,17,'static/images/product/1715946324950.jpg','Thiết kế mới Trở nên hoàn hảo. Bao da Qin sử dụng chất liệu da có kết cấu tự nhiên cao cấp mang lại cảm giác cao cấp cho chiếc vỏ. Thiết kế nắp trượt ống kính đã được cấp bằng sáng chế, bảo vệ ống kính máy ảnh, chống trầy xước và bảo vệ sự riêng tư của bạn.',7);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (14,'Miếng dán màn hình PPF dẻo cho Samsung Galaxy S22, S22 Plus, S22 Ultra',130000,38,'static/images/product/1715946324951.jpg','Thiết kế của dán PPF full mặt sau Samsung Galaxy S22, S22 Plus, S22 Ultra chính xác đến từng chi tiết, giúp miếng dán vừa vặn với chiếc điện thoại của bạn, bảo vệ mọi chi tiết mặt sau của chiếc điện thoại. Ngoài ra, nó còn được khoét lỗ tỉ mỉ ở vị trí camera và đèn flash đảm bảo chức năng của bộ phận này hoạt động được bình thường.',7);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (15,'Sạc dự phòng Wiwu 10000mAh Magnetic Charging Power Bank with Stand JC-20 (sạc magsafe 15W, sạc nhanh 20W)',750000,23,'static/images/product/1715946324952.jpg','Sạc dự phòng Wiwu 10000mAh Magnetic Charging Power Bank with Stand JC-20 (sạc magsafe 15Ư, sạc nhanh 20W) là một sản phẩm sạc dự phòng cao cấp đến từ thương hiệu Wiwu. Sản phẩm có thiết kế nhỏ gọn, sang trọng với dung lượng 10000mAh, hỗ trợ sạc nhanh Magsafe 15W và sạc nhanh PD 20W.',10);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (16,'Sạc dự phòng Wiwu Magnetic Wi-P016 Power Bank 10000mAh (Công nghệ sạc nhanh Magsafe, 22.5W)',900000,20,'static/images/product/1715946324953.jpg','Sạc dự phòng Wiwu Magnetic Wi-P016 Power Bank 10000mAh (22.5W,công nghệ sạc nhanh Magsafe) là sản phẩm sạc dự phòng cao cấp dành cho các thiết bị điện tử như iPhone, iPad, Apple Watch. Sạc dự phòng được thiết kế nhỏ gọn, hỗ trợ sạc nhanh không dây lên đến 22.5W, mang đến trải nghiệm sử dụng tiện lợi và an toàn cho người dùng.',10);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (17,'Pin sạc dự phòng MagSafe chính hãng Wiwu Snap Cube 10.000 mAh (sử dụng từ iPhone 12 đến 13, 14, 15 Pro Max)',750000,21,'static/images/product/1715946324954.jpg','WIWU Snap Cube Pin sạc dự phòng dung lượng 10.000 mAh là loại siêu nhỏ gọn thích hợp sạc Magsafe hút từ tính chắc chắn kiêm luôn giá đỡ rất nhiều tính năng trong cục sạc dự phòng này',10);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (18,'Sạc dự phòng Wiwu 20000mAh New Tank Wi-P012 (sạc nhanh 67W, đèn led hiển thị pin)',1200000,17,'static/images/product/1715946324955.jpg','Sạc dự phòng Wiwu 20000mAh New Tank Wi-P012 (sạc nhanh 67W, đèn led hiển thị pin) là một trong những sản phẩm sạc dự phòng tốt nhất trên thị trường hiện nay. Sản phẩm có dung lượng pin lớn, hỗ trợ sạc nhanh và được thiết kế nhỏ gọn, sang trọng.',11);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (19,'Củ Sạc Nhanh 20W dành cho iPhone 14, 13 Pro Max, 12Pro, 12Pro Max, iPad, Macbook hàng Zin',650000,42,'static/images/product/1715946324956.jpg','Củ Sạc Nhanh 20W dành cho iPhone 14, 13 Pro Max, 12Pro, 12Pro Max, iPad, Macbook hàng Zin',12);
INSERT INTO WebApp_accessories (id, Name, Price, Discount, Image, Description, CategoryID_id)
VALUES (20,'Củ sạc nhanh 20W dành cho iPhone 15, 14, 13 Pro Max, 12Pro, 12Pro Max, iPad, Macbook chính hãng',550000,29,'static/images/product/1715946324957.jpg','Củ Sạc Nhanh 20W dành cho iPhone 14, 13 Pro Max, 12Pro, 12Pro Max, iPad, Macbook chính hãng. Hỗ trợ sạc nhanh PD Type-C 3.0 công suất sử dụng lên đến 20W, cổng sạc type-c thời thượng.. Công suất đầu ra 5V-3A/ 9V-2.22A',12);

INSERT INTO WebApp_orders (id, TotalAmount, OrderDate, UserID_id, IsCancelled, IsPaid,Address, PhoneNumber)
VALUES (1,855000,'2024-05-21 01:11:12.761545',1,0,1,'','');
INSERT INTO WebApp_orders (id, TotalAmount, OrderDate, UserID_id, IsCancelled, IsPaid,Address, PhoneNumber)
VALUES (2,960500,'2024-05-21 02:11:12.761545',1,0,0,'','');
INSERT INTO WebApp_orders (id, TotalAmount, OrderDate, UserID_id, IsCancelled, IsPaid,Address, PhoneNumber)
VALUES (3,1237500,'2024-05-20 02:11:12.761545',1,0,0,'','');
INSERT INTO WebApp_orders (id, TotalAmount, OrderDate, UserID_id, IsCancelled, IsPaid,Address, PhoneNumber)
VALUES (4,1237500,'2024-05-19 02:11:12.761545',1,0,0,'','');
INSERT INTO WebApp_orders (id, TotalAmount, OrderDate, UserID_id, IsCancelled, IsPaid,Address, PhoneNumber)
VALUES (5,855000,'2024-05-19 02:11:12.761545',1,0,0,'','');
INSERT INTO WebApp_orders (id, TotalAmount, OrderDate, UserID_id, IsCancelled, IsPaid,Address, PhoneNumber)
VALUES (6,855000,'2024-05-18 02:11:12.761545',1,0,0,'','');
INSERT INTO WebApp_orders (id, TotalAmount, OrderDate, UserID_id, IsCancelled, IsPaid,Address, PhoneNumber)
VALUES (7,960500,'2024-05-17 02:11:12.761545',1,0,0,'','');

INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (1,2,247500,1,1);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (2,2,180000,2,1);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (3,1,462500,3,2);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (4,2,249000,7,2);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (5,5,330000,1,3);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (6,5,330000,1,4);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (7,2,247500,1,5);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (8,2,180000,2,5);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (9,2,247500,1,6);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (10,2,180000,2,6);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (11,1,462500,3,7);
INSERT INTO WebApp_orderdetails (id, Quantity, UnitPrice, AccessoryID_id, OrderID_id)
VALUES (12,2,249000,7,7);

INSERT INTO auth_user (id, password, last_login, is_superuser, username,last_name, email, is_staff, is_active, date_joined,first_name)
VALUES (3,'pbkdf2_sha256$720000$8wZKZEe31qp8ksJmRbbiK5$DDGXvU84gs27n7L94NdJGjGC+zO/ZKEj3C/yn0FDII8=	','2024-05-21 01:21:35.307383',0,'customer2','Trần','vantaiduongviet@gmail.com',0,1,'2024-05-21 01:11:12.761545','Huyền');
INSERT INTO auth_user (id, password, last_login, is_superuser, username,last_name, email, is_staff, is_active, date_joined,first_name)
VALUES (4,'pbkdf2_sha256$720000$8wZKZEe31qp8ksJmRbbiK5$DDGXvU84gs27n7L94NdJGjGC+zO/ZKEj3C/yn0FDII8=	','2024-05-21 01:21:35.307383',0,'customer3','Lê','taynambacsg@gmail.com',0,1,'2024-05-21 01:11:12.761545','Trang');
INSERT INTO auth_user (id, password, last_login, is_superuser, username,last_name, email, is_staff, is_active, date_joined,first_name)
VALUES (5,'pbkdf2_sha256$720000$8wZKZEe31qp8ksJmRbbiK5$DDGXvU84gs27n7L94NdJGjGC+zO/ZKEj3C/yn0FDII8=	','2024-05-21 01:21:35.307383',0,'customer4','Nguyễn','vantaivohongphat@gmail.com',0,1,'2024-05-21 01:11:12.761545','Thu');
INSERT INTO auth_user (id, password, last_login, is_superuser, username,last_name, email, is_staff, is_active, date_joined,first_name)
VALUES (6,'pbkdf2_sha256$720000$8wZKZEe31qp8ksJmRbbiK5$DDGXvU84gs27n7L94NdJGjGC+zO/ZKEj3C/yn0FDII8=	','2024-05-21 01:21:35.307383',0,'customer5','Lê','thienhuonglogistics@gmail.com',0,1,'2024-05-21 01:11:12.761545','Thuỷ');