# Generated by Django 5.0.4 on 2024-06-05 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_photo_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='action',
            field=models.CharField(choices=[('HDR', 'hdr'), ('BINARY', 'binary'), ('COLORIZED', 'colorized'), ('STYLIZATION', 'stylization'), ('VIGNETTE', 'vignette'), ('GRAYSCALE', 'grayscale'), ('SKETCH', 'sketch'), ('SEPIA', 'sepia'), ('COLD', 'cold'), ('SHARPEN', 'sharpen'), ('INVERT', 'invert'), ('BLURRED', 'blurred')], max_length=50, null=True),
        ),
    ]