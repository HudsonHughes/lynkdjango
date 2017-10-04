from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from django.conf import settings

from datetime import date, datetime


class TermManager(models.Manager):
    def create_term(self, title, slug, start_date, end_date,):
        report = self.get_or_create(title=title, slug=slug, start_date=start_date, end_date=end_date)
        return report

    def delete_term(self, title, slug, start_date, end_date,):
        report = self.delete(title=title, slug=slug, start_date=start_date, end_date=end_date)
        return report

    def current_term(self):
        term = None
        try:
            term = self.get(start_date__gte=date.today(),
                    end_date__lte=date.today())
        except Term.DoesNotExist:
            term = None
        return term


class Term(models.Model):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=32, unique=True)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End date')
    objects = TermManager()

    def __str__(self):
        return self.title

    def clean(self):
        super().clean(self)
        if self.start_date < self.end_date:
            raise ValidationError('End date is before start date.')


class SubjectManager(models.Manager):
    pass


class Subject(models.Model):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=32, unique=True)
    objects = SubjectManager()


class PeriodManager(models.Manager):
    pass


class Period(models.Model):
    title = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(max_length=16)
    start_time = models.TimeField()
    end_time = models.TimeField()
    objects = PeriodManager()


class CourseManager(models.Manager):
    pass


class Course(models.Model):
    title = models.CharField(max_length = 64)
    slug = models.SlugField(max_length = 64)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True)
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='instructors', blank=True,
                                      through='Teaching')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students', blank=True, through='Enrollment')
    edition = models.IntegerField(default=0)
    intro_info = models.TextField(blank=True)
    calendar_link = models.CharField(max_length = 256, default="")

    passing_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0.70)

    grade_threshold_A_plus = models.DecimalField(max_digits=5, decimal_places=2, default=0.97)
    grade_threshold_A = models.DecimalField(max_digits=5, decimal_places=2, default=0.93)
    grade_threshold_A_minus = models.DecimalField(max_digits=5, decimal_places=2, default=0.90)

    grade_threshold_B_plus = models.DecimalField(max_digits=5, decimal_places=2, default=0.87)
    grade_threshold_B = models.DecimalField(max_digits=5, decimal_places=2, default=0.83)
    grade_threshold_B_minus = models.DecimalField(max_digits=5, decimal_places=2, default=0.80)

    grade_threshold_C_plus = models.DecimalField(max_digits=5, decimal_places=2, default=0.77)
    grade_threshold_C = models.DecimalField(max_digits=5, decimal_places=2, default=0.73)
    grade_threshold_C_minus = models.DecimalField(max_digits=5, decimal_places=2, default=0.70)

    grade_threshold_D_plus = models.DecimalField(max_digits=5, decimal_places=2, default=0.67)
    grade_threshold_D = models.DecimalField(max_digits=5, decimal_places=2, default=0.63)
    grade_threshold_D_minus = models.DecimalField(max_digits=5, decimal_places=2, default=0.60)

    grade_threshold_F_plus = models.DecimalField(max_digits=5, decimal_places=2, default=0.57)
    grade_threshold_F = models.DecimalField(max_digits=5, decimal_places=2, default=0.53)
    grade_threshold_F_minus = models.DecimalField(max_digits=5, decimal_places=2, default=0.50, )

    # prerequisites = models.ManyToManyField('course.Course', blank=True, related_name='prerequisites', null=True,)

    # Useful for past records
    last_set_period = models.CharField(max_length=16, blank=True)
    last_set_term = models.CharField(max_length=64, blank=True)
    last_set_subject = models.CharField(max_length=64, blank=True)

    objects = CourseManager()

    def clean(self):
        super().clean(self)
        actual_order = sorted([self.grade_threshold_F_minus, self.grade_threshold_F, self.grade_threshold_F_plus,
                self.grade_threshold_D_minus, self.grade_threshold_D, self.grade_threshold_D_plus,
                self.grade_threshold_C_minus, self.grade_threshold_C, self.grade_threshold_C_plus,
                self.grade_threshold_B_minus, self.grade_threshold_B, self.grade_threshold_B_plus,
                self.grade_threshold_A_minus, self.grade_threshold_A, self.grade_threshold_A_plus,])
        expected_order = [self.grade_threshold_F_minus, self.grade_threshold_F, self.grade_threshold_F_plus,
                self.grade_threshold_D_minus, self.grade_threshold_D, self.grade_threshold_D_plus,
                self.grade_threshold_C_minus, self.grade_threshold_C, self.grade_threshold_C_plus,
                self.grade_threshold_B_minus, self.grade_threshold_B, self.grade_threshold_B_plus,
                self.grade_threshold_A_minus, self.grade_threshold_A, self.grade_threshold_A_plus,]
        convert_nones = lambda s: '' if s is None else str(s)
        self.full_name = self.first_name + " " + (convert_nones(self.middle_name) + " ") if convert_nones(
            self.middle_name) != "" else "" + self.last_name
        self.full_name_initial = self.first_name + " " + (
            convert_nones(self.middle_name)[0] + ". ") if convert_nones(
            self.middle_name) != "" else "" + self.last_name
        if actual_order == expected_order:
            raise ValidationError('Grade letter thresholds overlap.')

    @permalink
    def get_absolute_url(self):
        return reverse('course', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.last_set_period = "%s"% self.period.title
        self.last_set_term = "%s" % self.term.title
        self.last_set_subject = "%s" % self.period.subject
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('title', 'edition',)


class EnrollmentManager(models.Manager):
    def assign_student(self, user, course):
        report = self.get_or_create(user=user,course=course)
        return report

    def remove_student(self, user, course):
        report = self.delete(user=user, course=course)
        return report


class Enrollment(models.Model):
    course = models.ForeignKey('Course')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    objects = EnrollmentManager()

    class Meta:
        unique_together = ('course', 'user',)


class TeachingManager(models.Manager):
    def assign_teacher(self, user, course):
        report = self.create(user=user,course=course)
        return report

    def revoke_teacher(self, user, course):
        report = self.get_or_create(user=user,course=course)
        return report


class Teaching(models.Model):
    course = models.ForeignKey('Course')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    objects = TeachingManager()

    class Meta:
        unique_together = ('course', 'user',)