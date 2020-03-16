# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CoepHostel(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    c_id = models.CharField(db_column='C_ID', unique=True, max_length=7)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=25)  # Field name made lowercase.
    gender = models.CharField(db_column='GENDER', max_length=10)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=15)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50)  # Field name made lowercase.
    phone_no = models.BigIntegerField(db_column='PHONE_NO')  # Field name made lowercase.
    branch = models.CharField(db_column='BRANCH', max_length=20)  # Field name made lowercase.
    district = models.CharField(db_column='DISTRICT', max_length=25)  # Field name made lowercase.
    year = models.CharField(db_column='YEAR', max_length=15)  # Field name made lowercase.
    cet = models.IntegerField(db_column='CET')  # Field name made lowercase.
    preference = models.ManyToManyField('self',db_column='preference',)
    cgpa = models.FloatField(db_column='CGPA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COEP_HOSTEL'


class User(AbstractUser):
    username = models.IntegerField(null=False,unique=True)
    year = models.CharField(max_length=2 ,null=True,default='')
    gender = models.CharField(db_column='GENDER', max_length=10 ,null=True,default='')  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=15 ,null=True,default='')  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=25)  # Field name made lowercase.
    cet = models.IntegerField(db_column='CET' ,null=True,default=0)  # Field name made lowercase.
    cgpa = models.FloatField(db_column='CGPA',null=True,default=0)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True,default=0)  # Field name made lowercase.
    branch = models.CharField(db_column='BRANCH', max_length=50, null=True,default='')
    name = models.CharField(db_column='NAME', max_length=25,default='')
    astatus = models.IntegerField(db_column='ASTATUS',default=0)
    roomno = models.IntegerField(db_column='ROOMNO',default=0)
    pref1=models.IntegerField(db_column='PREF1',null=True,default=0)
    pref2=models.IntegerField(db_column='PREF2',null=True,default=0)
    pref3=models.IntegerField(db_column='PREF3',null=True,default=0)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.username)

    class Meta:
        managed = False
        db_table = 'app1_user'



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class StudentsUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    username = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'students_user'


class StudentsUserGroups(models.Model):
    user = models.ForeignKey(StudentsUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'students_user_groups'
        unique_together = (('user', 'group'),)


class StudentsUserUserPermissions(models.Model):
    user = models.ForeignKey(StudentsUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'students_user_user_permissions'
        unique_together = (('user', 'permission'),)
