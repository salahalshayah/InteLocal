-- init.sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Chat table
CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Message table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);

-- Response table
CREATE TABLE responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id UUID NOT NULL,
    content TEXT NOT NULL,
    sources UUID[], -- Array of UUIDs for source references
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
);

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    file_type TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Chat vectors table
CREATE TABLE chat_vectors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID NOT NULL,
    is_message BOOLEAN NOT NULL,
    content TEXT NOT NULL,
    vector VECTOR(768),
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);

-- Document vectors table
CREATE TABLE doc_vectors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doc_id UUID NOT NULL,
    doc_index INT NOT NULL,
    user_id UUID NOT NULL,
    content TEXT NOT NULL,
    vector VECTOR(768),
    FOREIGN KEY (doc_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for faster queries
CREATE INDEX idx_chats_user_id ON chats(user_id);
CREATE INDEX idx_messages_chat_id ON messages(chat_id);
CREATE INDEX idx_responses_message_id ON responses(message_id);
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_chat_vectors_chat_id ON chat_vectors(chat_id);
CREATE INDEX idx_doc_vectors_user_id ON doc_vectors(user_id);

-- pgvector indexes for similarity search
CREATE INDEX chat_vectors_vector_idx ON chat_vectors USING hnsw (vector vector_l2_ops);
CREATE INDEX doc_vectors_vector_idx ON doc_vectors USING hnsw (vector vector_l2_ops);


--What the admin user will look like
-- {
--   "first_name": "admin",
--   "last_name": "admin",
--   "email": "admin@admin.admin",
--   "password": "admin"
-- }

INSERT INTO users (id, first_name, last_name, email, password_hash)
VALUES (
    '00000000-0000-0000-0000-000000000000', -- Placeholder UUID for a system/admin user
    'admin',
    'admin',
    'admin@admin.admin',
    'cc597772af8f8d0c0771c5457974b600$0beb9c3fde6fd227de9dc529f587fd65b0b7f38bdb74d4a05d90da220233be24'
);

INSERT INTO documents (id, user_id, file_type, file_name, file_path, added_at)
VALUES (
    '00000000-0000-0000-0000-000000000000', -- Placeholder UUID for the deleted document
    '00000000-0000-0000-0000-000000000000', -- Placeholder UUID for a system/admin user or real user
    'deleted',                             -- file_type indicating it's a deleted document
    'Deleted Document',                    -- A clear name indicating deletion
    '/path/to/deleted/file',               -- Placeholder file path since the file is removed
    CURRENT_TIMESTAMP                      -- Time of creation
);
