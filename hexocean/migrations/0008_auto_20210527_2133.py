# Generated by Django 3.2.3 on 2021-05-27 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hexocean', '0007_img_height'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='img',
            name='height',
        ),
        migrations.RemoveField(
            model_name='img',
            name='parent',
        ),
        migrations.CreateModel(
            name='Thumb',
            fields=[
                ('img_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hexocean.img')),
                ('height', models.IntegerField(blank=True, null=True)),
                ('parentt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='hexocean.img')),
            ],
            bases=('hexocean.img',),
        ),
    ]