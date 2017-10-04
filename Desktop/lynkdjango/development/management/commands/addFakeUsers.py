from django.core.management import BaseCommand
from django.db import models
from account.models import *
from datetime import date
from django.conf import settings

from django.db import models
from django.conf import settings
from account.models import *

from course.models import Course
import csv


#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	# Show this when the user types help
	help = "Takes fake names and creates users in bulk."
	# A command must define handle()

	def handle(self, *args, **options):
		with open('data/mock_students.csv', 'r') as csvFile:
			data = csv.reader(csvFile, delimiter=',')
			userNamesUsed = []
			grade = 6
			for row in data:
				finalUserName = ""
				possibleUserName = row[0][0].lower() + (row[1][0].lower() if row[1] != "" else "") + row[2].lower()
				if not possibleUserName in userNamesUsed:
					finalUserName = possibleUserName
				else:
					i = 1
					while possibleUserName + str(i) in userNamesUsed:
						i = i + 1
					finalUserName = possibleUserName + str(i)
				print(", ".join([row[0], row[1], row[2], "hlhughes@uci.edu", finalUserName]))
				User.objects.filter(username = finalUserName).delete()
				print(finalUserName)
				User.objects.create_counselor_user(first_name=row[0],middle_name=row[1],last_name=row[2],email="hlhughes@uci.edu",username=finalUserName,password="tango123")
				grade = grade + 1
				if grade > 8:
					grade = 6