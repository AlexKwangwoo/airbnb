# Generated by Django 2.2.5 on 2020-09-27 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0007_conversation_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='reservation',
        ),
    ]
