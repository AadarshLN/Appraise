# Generated by Django 2.2.12 on 2020-10-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EvalData', '0041_directassessmentdocumentresult_directassessmentdocumenttask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textsegment',
            name='segmentText',
            field=models.TextField(help_text='(max. 2000 characters)', max_length=2000, verbose_name='Segment text'),
        ),
    ]
