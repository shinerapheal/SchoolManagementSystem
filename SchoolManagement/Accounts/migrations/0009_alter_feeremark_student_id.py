# Generated by Django 5.0 on 2024-12-14 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0008_alter_libraryhystory_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeremark',
            name='student_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]