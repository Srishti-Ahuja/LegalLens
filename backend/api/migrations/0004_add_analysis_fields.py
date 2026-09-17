from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_update_document_chunks'),  # runs after our previous migration
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE documents
                ADD COLUMN summary TEXT,
                ADD COLUMN risk_assessment JSONB,
                ADD COLUMN is_processed BOOLEAN NOT NULL DEFAULT FALSE;
            """,
            reverse_sql="""
                ALTER TABLE documents
                DROP COLUMN summary,
                DROP COLUMN risk_assessment,
                DROP COLUMN is_processed;
            """,
        ),
    ]