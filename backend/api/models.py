from django.db import models

# We are using raw SQL queries with pgvector directly in our services 
# to keep memory usage low and bypass the need for external vector ORMs.
# See supabase_schema.sql for the table definitions.
