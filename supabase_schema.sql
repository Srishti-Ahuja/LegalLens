-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Table to store uploaded documents metadata
create table if not exists documents (
    id uuid primary key default gen_random_uuid(),
    filename text not null,
    upload_date timestamp with time zone default timezone('utc'::text, now()),
    file_hash text not null,
    summary text,
    risk_assessment jsonb,
    is_processed boolean default false
);

-- Table to store document chunks and their vector embeddings
create table if not exists document_chunks (
    id uuid primary key default gen_random_uuid(),
    document_id uuid references documents(id) on delete cascade,
    page_number integer not null,
    chunk_index integer not null,
    content text not null,
    embedding vector(768) -- Gemini text-embedding-004 uses 768 dimensions
);

-- Create an HNSW index for fast similarity search
create index if not exists document_chunks_embedding_idx 
on document_chunks using hnsw (embedding vector_cosine_ops);
