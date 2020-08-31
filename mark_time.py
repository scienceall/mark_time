import sqlite3, time, datetime

con = sqlite3.connect('work_since_12.05.2020')
c = con.cursor()

def table_creation():
	c.execute('create table if not exists working( start_time real, end_time real)')

def table_delete():
	c.execute('drop table if exists working')

def check_table_exists_or_1st_rec_not_finished():
	c.execute('select max(end_time) from working')
	find_max_val = c.fetchone()[0]
	wont_be_used_var = 1 / find_max_val

def attempt_to_initiate_of_start():
	c.execute('select min(end_time) from working')
	checkzero = c.fetchone()[0]
	if checkzero != 0:
		start_time = time.time()
		end_time = 0
		c.execute("insert into working (start_time, end_time) values (?, ?)", (start_time, end_time))
		con.commit()
		print ('Your work day has been successfully started.')
	else:
		print ("Wow, you are already started, finish first.")

def attempt_to_initiate_of_end():
	c.execute('select min(end_time) from working')
	checkzero = c.fetchone()[0]
	if checkzero == 0:
		endday = time.time()
		zva = 0
		c.execute('update working set end_time = (?) where end_time = (?)', (endday, zva))
		con.commit()
		print ('Your work day has been successfully finished.')
	else:
		print ("Wow, you are already finished, start first.")

def delete_table_choice():
	print ('Are you sure? If yes print "yes", if no print "no" to cancel and out to main menu.')
	choice_delete = input()
	if choice_delete == 'yes':
		table_delete()
		print ('Ready.')
	elif choice_delete == 'no':
		print ('Ok, you will be redirected to main menu.')
	else:
		print ('Command not understood. You will be redirected to main menu.')

def checking_datetime():
	normal_input = input()
	checking_input = (datetime.datetime.strptime(normal_input, '%d%m%Y %H%M').timestamp())
	condition_x = 0
	c.execute('select * from working')
	for row in c.fetchall():
		if checking_input > row[0] and checking_input < row[1]:
			condition_x = condition_x + 1
	if condition_x > 0:
		print ('Yes, you did work that moment.')
	else:
		print ('No, you did not work that moment.')

while True:
	print ('_____________________________')
	print ('THIS IS MAIN MENU')
	print ('To begin work day enter "start"')
	print ('To finish work day enter "end"')
	print ('To check date enter "check"')
	print ('To out the program enter "out"')
	print ('To clear data enter "clear"')
	print ('To show info enter "info"')
	entry_action = input()
	if entry_action == "start":
		table_creation()
		attempt_to_initiate_of_start()
	elif entry_action == "end":
		try:
			attempt_to_initiate_of_end()
		except:
			#table_creation()
			print ('Database is empty yet, start work day to make first record.')
	elif entry_action == "check":
		try:
			check_table_exists_or_1st_rec_not_finished()
		except sqlite3.OperationalError:
			print ('Can not check.(No data.)')
		except ZeroDivisionError:
			print ('Table of database has only one record that not finished. First finish work day then you can make check.')
		else:
			print ('Enter a date and time using format DDMMYYYYspaceHHMM(Example: 31052020 2359), date should not exceed 19 janruary 2038.')
			xx = 1
			while xx == 1:
				try:
					checking_datetime()
					xx = 0
				except (OverflowError, ValueError):
					print ('Input error. Try again? For yes enter "y", for no enter "n."')
					xxx = 1
					while xxx == 1:
						again_check = input()
						if again_check == 'y':
							print ('Enter date and time.')
							xxx = 0
						elif again_check == 'n':
							xxx = 0
							xx = 0
						else:
							print ('Command not recognized. Would you try again? y-yes, n-no.')
				except sqlite3.OperationalError:
					print ('Wow, table disappeared.')
					xx = 0
	elif entry_action == "out":
		c.close()
		con.close()
		break
	elif entry_action == "clear":
		try:
			check_table_exists_or_1st_rec_not_finished()
		except sqlite3.OperationalError:
			print ('Is already clean.')
		except ZeroDivisionError:
			delete_table_choice()
		else:
			delete_table_choice()
	elif entry_action == "info":
		print ('''This program can be used for example by employee who want to mark their precise work time. When worker starting his work day,
		he should input start command, when he finish its work day, input the end command, at the next working time should to do the same.
		By this way worker mark his working time in database. If worker oneday going to check if he had worked at some specific date and time,
		he just can input the check command, and by this way he can find out does he had been working at that moment or not.''')
	else:
		print ('Command not recognized.')
