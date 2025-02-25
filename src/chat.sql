DROP TABLE IF EXISTS Memberships CASCADE;
DROP TABLE IF EXISTS Channels CASCADE;
DROP TABLE IF EXISTS Messages CASCADE;
DROP TABLE IF EXISTS Suspensions CASCADE;
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Communities CASCADE;

CREATE TABLE IF NOT EXISTS Communities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash  VARCHAR(255),
    contact_info TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_username_change TIMESTAMP,
    session_key VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Channels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    community_id INT REFERENCES Communities(id) NOT NULL
);

CREATE TABLE IF NOT EXISTS Messages (
    id SERIAL PRIMARY KEY,
    sender_id INT REFERENCES Users(id) NOT NULL,
    receiver_id INT REFERENCES Users(id) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_unread BOOLEAN DEFAULT TRUE NOT NULL,
    community_id INT REFERENCES Communities(id),
    channel_id INT REFERENCES Channels(id),
    search_vector tsvector
);

CREATE TABLE IF NOT EXISTS Suspensions (
    user_id INT REFERENCES Users(id) NOT NULL,
    suspended_until TIMESTAMP,
    PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS Memberships (
    user_id INT REFERENCES Users(id) NOT NULL,
    community_id INT REFERENCES Communities(id) NOT NULL,
    channel_id INT REFERENCES Channels(id) NOT NULL,
    suspended BOOLEAN DEFAULT FALSE NOT NULL,
    PRIMARY KEY (user_id, community_id)
);