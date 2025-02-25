INSERT INTO Communities (name) VALUES
('Arrakis'),
('Comedy');

INSERT INTO Channels (name, community_id) VALUES
('Worms', 1),
('Random', 1),
('ArgumentClinic', 2),
('Dialogs', 2),
('Comedy', 2);

INSERT INTO Users (username, contact_info, created_at, password_hash) VALUES
('Abbott', 'abbott@gmail.com', '1922-01-01','123456789123456798765432198765431fbe5ea842a3ec8acafbb45c1be87a14c691e8052b164b48f76a10d48e98ce6ab218c24f06a588990f69d458418a2ff8ef6e915b2f273c62625eec710838fe45'),
('Costello', 'costello@gmail.com', '1922-01-01', ''),
('Moe', 'moe@gmail.com', '1922-01-01', ''),
('Larry', 'larry@gmail.com', '1922-01-01', ''),
('Curly', 'curly@gmail.com', '1922-01-01', ''),
('DrMarvin', 'drmarvin@gmail.com', '1991-05-16', '');

INSERT INTO Messages (sender_id, receiver_id, message, timestamp, is_unread, community_id, channel_id) VALUES
(1, 2, 'Hey Costello', '1925-01-01', TRUE, 1, 2),
(2, 1, 'Hey Abbott', '1925-01-02', FALSE, 1, 2),
(3, 4, 'Hey Larry', '1995-06-01', TRUE, 1, 2),
(4, 3, 'Hey Moe', '1995-06-05', FALSE, 1, 2),
(5, 1, 'Hey Abbott', '1970-02-15', TRUE, 1, 2);

INSERT INTO Suspensions (user_id, suspended_until) VALUES
(4, '2060-01-01'),
(5, '1999-12-31');