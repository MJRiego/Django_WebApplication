from django.db import models
from django.utils import timezone

default_value = timezone.now()

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Members(BaseModel):
    memberID = models.AutoField(primary_key=True)
    YEAR_LEVEL_CHOICES = (('1st Year','1st Year'), ('2nd Year','2nd Year'), ('3rd Year','3rd Year'), ('4th Year', '4th Year'))
    SEX_CHOICES = (('Male','Male'), ('Female','Female'))
    CIVIL_STATUS_CHOICES = (('Single','Single'), ('Married','Married'), ('Widowed','Widowed'), ('Divorced','Divorced'))
    batchnum = models.IntegerField()
    firstname = models.CharField(max_length=250)
    midinitial = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    school = models.CharField(max_length=250)
    college = models.CharField(max_length=250)
    yearlevel = models.CharField(max_length=20, choices=YEAR_LEVEL_CHOICES)
    program = models.CharField(max_length=300)
    major = models.CharField(max_length=250)
    acceptdate = models.DateField()
    age = models.IntegerField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    birthdate = models.DateField()
    civilstatus = models.CharField(max_length=20, choices=CIVIL_STATUS_CHOICES)
    religion = models.CharField(max_length=250)
    mobile = models.BigIntegerField()
    email = models.CharField(max_length=250)
    address = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Members"

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"
    
    

    
class Grades(BaseModel):
    YEAR_LEVEL_CHOICES = (('1st Year','1st Year'), ('2nd Year','2nd Year'), ('3rd Year','3rd Year'), ('4th Year', '4th Year'))
    SEM_CHOICES = (('1st Sem','1st Sem'), ('2nd Sem','2nd Sem'))
    gradeID = models.AutoField(primary_key=True)
    memberID = models.ForeignKey(Members, on_delete=models.CASCADE, db_column='memberID')
    yearlevel = models.CharField(max_length=20, choices=YEAR_LEVEL_CHOICES)
    semester = models.CharField(max_length=20, choices=SEM_CHOICES)
    course = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    unit = models.IntegerField()
    grades = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name_plural = "Grades"

    def __str__(self):
        return f"{self.grades}"
    

class Allowances(BaseModel):
    YEAR_LEVEL_CHOICES = (('1st Year','1st Year'), ('2nd Year','2nd Year'), ('3rd Year','3rd Year'), ('4th Year', '4th Year'))
    SEM_CHOICES = (('1st Sem','1st Sem'), ('2nd Sem','2nd Sem'))
    MONTH_CHOICES = (('1st Month','1st Month'), ('2nd Month','2nd Month'), ('3rd Month','3rd Month'), ('4th Month', '4th Month'),('5th Month', '5th Month'))
    allowanceID = models.AutoField(primary_key=True)
    memberID = models.ForeignKey(Members, on_delete=models.CASCADE, db_column='memberID')
    yearlevel = models.CharField(max_length=20, choices=YEAR_LEVEL_CHOICES)
    semester = models.CharField(max_length=20, choices=SEM_CHOICES)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    date_received = models.DateField()

    class Meta:
        verbose_name_plural = "Allowances"

    def __str__(self):
        return f"{self.date_received}"
    

class Requirements_list(BaseModel):
    reqs_listID = models.AutoField(primary_key=True)
    reqs_requirements = models.CharField(max_length=250)
    notes = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Requirements_list"

    def __str__(self):
        return f"{self.reqs_requirements}"


class Requirements(BaseModel):
    reqsID = models.AutoField(primary_key=True)
    memberID = models.ForeignKey(Members, on_delete=models.CASCADE, db_column='memberID')
    reqs_listID = models.ForeignKey(Requirements_list, on_delete=models.CASCADE, related_name='requirements', db_column='reqs_listID')
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Requirements"

    def __str__(self):
        return f"{self.date}"

    




    
