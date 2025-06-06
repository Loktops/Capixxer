# Generated by Django 5.2 on 2025-04-06 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DadosLoja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('vendas', models.DecimalField(decimal_places=2, max_digits=10)),
                ('clientes', models.IntegerField()),
                ('ticket_medio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('meta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produtos', models.IntegerField(default=0)),
                ('observacoes', models.TextField(blank=True)),
                ('loja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Capixxer.loja')),
            ],
        ),
    ]
