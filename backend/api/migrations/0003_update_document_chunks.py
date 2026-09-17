from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_create_documents'),
    ]
    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE document_chunks ADD COLUMN page_number INTEGER NOT NULL DEFAULT 0;
                ALTER TABLE document_chunks RENAME COLUMN chunk_text TO content;
            """,
            reverse_sql="""
                ALTER TABLE document_chunks DROP COLUMN page_number;
                ALTER TABLE document_chunks RENAME COLUMN content TO chunk_text;
            """,
        ),
    ]
