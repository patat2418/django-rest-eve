# Generated by Django 4.1.7 on 2023-04-14 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies_rest_app', '0003_alter_oscar_actor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oscar',
            name='actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies_rest_app.actor'),
        ),
    ]
