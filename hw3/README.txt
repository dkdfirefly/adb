SAT Results:(2010 and 2012)
============

SchoolID, School_name, readScore, MathScore, writeScore

schoolID - initial 2 digits removed
school name - as it is
readscore - value mod 50, append "-r"
mathScore - value mod 50, append "-m"
writeScore - value mod 50, append "-w"

for values not present in read, math, write score - replaced with 0-r, 0-m, 0-w resp.

no. of test takers - not used

added year as last column, and appended the two years together.

Demographic
============

all num counts removed, ell removed, fl removed.
all count of students in grade removed.
name removed.
schoolID - initial 2 digits removed
filtered only year - 09-10, 11-12


total_enrollment - value mod 500, append "-t"
all other races - value mod 10, append "-a"(asian), "-b"(black), "-h"(hispanic), "-wh"(white), "-male", "-f"(female)

Progress Report
================
taking only years: 2010-11, 2008-09
broken down to 2 records - corresponding to each year.
