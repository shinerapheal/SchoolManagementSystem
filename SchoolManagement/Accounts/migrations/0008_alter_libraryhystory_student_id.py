# Generated by Django 5.0 on 2024-12-13 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0007_user_is_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryhystory',
            name='student_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
