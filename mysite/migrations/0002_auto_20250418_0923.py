# Add this import at the top
from django.db import models
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('mysite', '0001_initial'),  # Make sure this matches your previous migration
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]