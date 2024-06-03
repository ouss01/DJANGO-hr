# Generated by Django 5.0.2 on 2024-06-03 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the contract type', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='leave',
            name='departure_reason',
            field=models.CharField(default=None, help_text='Name of the departure reason', max_length=100),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('duration_regulation', models.IntegerField(help_text='Regulatory duration for the contract type (in months)')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='EmployeeApp.employee')),
                ('contract_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='EmployeeApp.contracttype')),
            ],
        ),
    ]