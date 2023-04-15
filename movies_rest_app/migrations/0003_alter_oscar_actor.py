# Generated by Django 4.1.7 on 2023-04-02 18:53

from django.db import migrations, models
import django.db.models.deletion
import movies_rest_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_rest_app', '0002_oscar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oscar',
            name='actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies_rest_app.actor', validators=[movies_rest_app.models.actor_oscar]),
        ),
    ]
