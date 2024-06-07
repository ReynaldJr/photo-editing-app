# Generated by Django 5.0.4 on 2024-06-07 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_photo_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='action',
            field=models.CharField(choices=[('SHARPEN', 'sharpen'), ('GRAYSCALE', 'grayscale'), ('BLURRED', 'blurred'), ('COLD', 'cold'), ('COLORIZED', 'colorized'), ('WARM', 'warm'), ('SKETCH', 'sketch'), ('INVERT', 'invert'), ('BINARY', 'binary'), ('SEPIA', 'sepia')], max_length=50, null=True),
        ),
    ]
