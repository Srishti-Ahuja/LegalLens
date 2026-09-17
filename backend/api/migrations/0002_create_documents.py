from django.db import migrations
import django.contrib.postgres.operations

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        django.contrib.postgres.operations.CreateExtension('vector'),
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                chunk_text TEXT NOT NULL,
                embedding VECTOR(1536),
                chunk_index INTEGER NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS document_chunks; DROP TABLE IF EXISTS documents;",
        ),
    ]
