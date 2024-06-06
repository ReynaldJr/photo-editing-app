# Generated by Django 5.0.4 on 2024-06-05 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_photo_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='action',
            field=models.CharField(choices=[('COLD', 'cold'), ('BINARY', 'binary'), ('COLORIZED', 'colorized'), ('SEPIA', 'sepia'), ('SHARPEN', 'sharpen'), ('VIGNETTE', 'vignette'), ('SKETCH', 'sketch'), ('HDR', 'hdr'), ('INVERT', 'invert'), ('STYLIZATION', 'stylization'), ('GRAYSCALE', 'grayscale'), ('BLURRED', 'blurred')], max_length=50, null=True),
        ),
    ]
