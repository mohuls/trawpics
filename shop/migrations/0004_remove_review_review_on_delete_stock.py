# Generated by Django 4.0.3 on 2022-03-12 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_delete_about_remove_order_plan_delete_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='review_on',
        ),
        migrations.DeleteModel(
            name='Stock',
        ),
    ]
