# Generated by Django 2.0.1 on 2020-09-20 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0007_venda_nfe_emitida'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItensDoPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.FloatField()),
                ('desconto', models.DecimalField(decimal_places=2, max_digits=5)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Produto')),
            ],
        ),
        migrations.RemoveField(
            model_name='venda',
            name='produtos',
        ),
        migrations.AddField(
            model_name='itensdopedido',
            name='venda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Venda'),
        ),
    ]
