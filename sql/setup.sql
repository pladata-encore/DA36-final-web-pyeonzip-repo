
CREATE DATABASE pyeonzip;

INSERT INTO pyeonzip.product_productcategory(productCategoryId, productCategoryName) VALUES (0,'식품');
INSERT INTO pyeonzip.product_product VALUES (1,'불닭볶음면',0,'10000','http:///0','2025-01-03 22:24:47.377130',1);
INSERT INTO pyeonzip.auth_user VALUES (4, '신상품 만들어주세여', '2025-01-03 22:24:47.377130', '1', 'we',2,1,1,1,1,'2025-01-14 05:52:58.737818');
INSERT INTO pyeonzip.community_category VALUES (1,'신상품아이디어');
INSERT INTO pyeonzip.community_community (communityId,communityTitle, communityContent, created_at, deadline, authorId_id, categoryId_id) VALUES (2, '신상품 만들어주세여', 'The python web framework for perfectionists with deadlines. 이게 무슨 말인가요?', '2025-01-03 22:24:47.377130', '2025-01-07 04:56:33.037743',1,1);
INSERT INTO pyeonzip.community_community (communityId,communityTitle, communityContent, created_at, deadline, authorId_id, categoryId_id) VALUES (3, '신상품 만들어주세여', 'The python web framework for perfectionists with deadlines. 이게 무슨 말인가요?', '2025-01-03 22:24:47.377130', '2025-01-07 04:56:33.037743',1,1);
INSERT INTO pyeonzip.community_community (communityId,communityTitle, communityContent, created_at, deadline, authorId_id, categoryId_id) VALUES (1, '신상품 만들어주세여', 'The python web framework for perfectionists with deadlines. 이게 무슨 말인가요?', '2025-01-03 22:24:47.377130', '2025-01-07 04:56:33.037743',1,1);
INSERT INTO pyeonzip.community_community (communityId,communityTitle, communityContent, created_at, deadline, authorId_id, categoryId_id) VALUES (4, '신상품 만들어주세여', 'The python web framework for perfectionists with deadlines. 이게 무슨 말인가요?', '2025-01-03 22:24:47.377130', '2025-01-07 04:56:33.037743',1,1);

DELETE FROM pyeonzip.product_product where productId=1;

INSERT INTO pyeonzip.product_product(product_name, product_category_name, convenient_store_name, product_price, product_image_url, updated_at)
VALUES ('바나프레소 커피', '음료', 0, 1000, 'http:/', NOW());

INSERT INTO pyeonzip.product_product(product_name, product_category_name, convenient_store_name, product_price, product_image_url, updated_at)
VALUES ('바나나 과자', '과자', 0, 2000, 'http:/', NOW());
