# Generated by Django 5.0.2 on 2024-03-03 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('societe_name', models.CharField(max_length=30, verbose_name='إسم المؤسسة')),
                ('ceo_fname', models.CharField(max_length=20, verbose_name='إسم الشخصي للمدير')),
                ('ceo_lname', models.CharField(max_length=20, verbose_name='إسم اعائلي للمدير')),
                ('ceo_cnie', models.CharField(max_length=10, verbose_name='رقم ب.ت.و')),
                ('ceo_mail', models.CharField(max_length=30, verbose_name='البريد الإلكتروني')),
                ('city', models.CharField(max_length=15, verbose_name='مقر المؤسسة')),
                ('address', models.CharField(max_length=40, verbose_name='عنوان المؤسسة')),
                ('fix', models.CharField(max_length=10, verbose_name='رقم الهاتف الثابت')),
                ('phone', models.CharField(max_length=10, verbose_name='رقم الهاتف')),
                ('license_number', models.SmallIntegerField(verbose_name='رقم الرخصة')),
                ('reg_num_in_cms', models.SmallIntegerField(verbose_name='رقم القيد في السجل التجاري')),
                ('reg_num_pro_tax', models.SmallIntegerField(verbose_name='رقم القيد في سجل الضريبة المهنية ')),
            ],
            options={
                'verbose_name_plural': 'قائمة خاصة بالمؤسسة',
            },
        ),
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicule_registration', models.CharField(max_length=20, null=True, unique=True, verbose_name='رقم التعريفي للعربة')),
                ('vehicule_name', models.CharField(max_length=20, verbose_name='إسم العربة')),
                ('expired_date', models.DateField(blank=True, null=True, verbose_name='تاريخ إنتهاء العمل')),
                ('vehicule_photo', models.ImageField(blank=True, null=True, upload_to='photos/vehicules/%Y/%m/%d/', verbose_name='الصورة العربة')),
            ],
            options={
                'verbose_name_plural': 'قائمة العربات',
            },
        ),
        migrations.CreateModel(
            name='MonitorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitor_authorization_number', models.CharField(max_length=8, unique=True, verbose_name='الرقم الوطني للمدرب')),
                ('fnameAR', models.CharField(max_length=15, verbose_name='الإسم الشخصي')),
                ('lnameAR', models.CharField(max_length=15, verbose_name='الإسم العائلي')),
                ('fnameLA', models.CharField(max_length=15, verbose_name='First name')),
                ('lnameLA', models.CharField(max_length=15, verbose_name='Last name')),
                ('phone', models.CharField(max_length=14, verbose_name='رقم الهاتف')),
                ('cnie', models.CharField(max_length=15, unique=True, verbose_name='رقم بطاقة التعريف الوطنية')),
                ('photo_mnt', models.ImageField(blank=True, null=True, upload_to='photos/monitors/%Y/%m/%d/', verbose_name='الصورة الشخصية')),
                ('gender', models.PositiveSmallIntegerField(choices=[(1, 'ذكر'), (2, 'أنثى')], default=1, verbose_name='الجنس')),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'A'), (2, 'A1'), (3, 'B')], default=3, verbose_name='الصنف')),
                ('nationality', models.CharField(default='MAROCAINE', max_length=15, verbose_name='الجنسية')),
                ('joined_date', models.DateField(auto_now_add=True, verbose_name='تاريخ التسجيل')),
                ('vehicule', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='monitors.vehicule', verbose_name='العربة')),
            ],
            options={
                'verbose_name_plural': 'قائمة المدربون',
            },
        ),
    ]