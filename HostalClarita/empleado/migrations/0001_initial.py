# Generated by Django 3.2.2 on 2021-06-30 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_codp', models.DateField()),
                ('estado_odp', models.IntegerField()),
                ('precio_total_odp', models.IntegerField()),
                ('fecha_rodp', models.DateField()),
                ('empleado_rut_emp', models.CharField(max_length=20)),
                ('proveedor_rut_prov', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Detallepedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidadp', models.IntegerField()),
                ('precio_pedido', models.IntegerField()),
                ('producto_codigo_producto', models.IntegerField()),
                ('orden_pedido_id', models.ForeignKey(db_column='orden_pedido_id', on_delete=django.db.models.deletion.DO_NOTHING, to='empleado.ordenpedido')),
            ],
        ),
    ]