from django.db import migrations, models
import django.contrib.postgres.operations

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        django.contrib.postgres.operations.CreateExtension('vector'),
        migrations.RunSQL(
            sql="""
            CREATE TABLE documents (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE document_chunks (
            id SERIAL PRIMARY KEY,
            document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            chunk_text TEXT NOT NULL,
            embedding VECTOR(1536),
            chunk_index INTEGER NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """,
            reverse_sql="DROP TABLE document_chunks; DROP TABLE documents;"
        ),
    ]