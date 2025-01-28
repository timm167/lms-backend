from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_lesson_content'),  
    ]

    operations = [
        migrations.RunSQL("""
            CREATE VIEW teacher_user_view AS
            SELECT 
                teacher.id AS teacher_id,
                user.username AS username,
                user.first_name AS first_name,
                user.last_name AS last_name,
                user.email AS email,
                teacher.subject AS subject
            FROM teacher
            JOIN user ON teacher.user_id = user.id;
        """)
    ]