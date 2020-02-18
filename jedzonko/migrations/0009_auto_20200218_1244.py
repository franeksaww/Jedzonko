# Generated by Django 2.2.6 on 2020-02-18 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0008_remove_recipeplan_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayname',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='day_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Dayname', unique=True),
        ),
    ]
