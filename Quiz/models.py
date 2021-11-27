from django.db import models

# Create your models here.

class StudentDetails(models.Model):
    Sid =models.CharField(max_length=200, null=True)
    user_name = models.CharField(max_length=200, null=True)
    pas= models.CharField(max_length=200, null=True)


class QuesModel(models.Model):
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question



class Student(models.Model):
    Sid =models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    result1 = models.CharField(max_length=200, null=True)
    result2 = models.CharField(max_length=200, null=True)
    result3 = models.CharField(max_length=200, null=True)
    count1 = models.CharField(max_length=200, null=True)
    count2 = models.CharField(max_length=200, null=True)
    count3 = models.CharField(max_length=200, null=True)

class Performance(models.Model):
    Sid =models.CharField(max_length=200, null=True)
    # Resulttest = models.CharField(max_length=200, null=True)
    result = models.CharField(max_length=200, null=True)





