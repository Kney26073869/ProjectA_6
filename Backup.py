##########################################################
#Titre		: Backup.py
#
# DESCRIPTION :
# Sauvegarde wordpress/sql vers un serveur distant (FTP)
#
# AUTEUR	: COIGNOUX Morgan
#
# Date 		: 31/01/2022
#
# REPO		:
##########################################################

#!/usr/bin/python3
#  -*- coding: utf-8 -*-

# Mise en forme de la bibliothèque : https://docs.python.org ###
# 								Documentation		: https://docs.python.org
#											: http://docs.paramiko.org
print("Importation de la biblioteque")
import os
import sys
import shutil
import paramiko
import time
import datetime
import subprocess

# Mise en forme des variables
#
#
# '******' Entrer les parametres suivant les besoins
print("Mise en forme des variables")

# Jour de la semaine
date = datetime.datetime.today().strftime("%A") 

# Informations concernant le traitement
backup_folder = 'backup_to_ftp'
wphtml= 'wp_html'
html = '/var/www/html'
targz = '.tar.gz'
tarhtml = wphtml+targz
backup_to_ftp_targz = backup_folder+targz

# Informations mysql
usermysql = '******'
pwdmysql = '******'
databasemysql = '******'
bddbackupname = '******'

# Informations FTP 				
host = '******' 				 				
username = '******' 							
password = '******' 				
destination= '/home/******/Documents/' 			

print("Traitement de la sauvegarde")

# Création du répertoitre de sauvegarde
print("Creation du repertoire de sauvegarde")
os.makedirs(backup_folder, exist_ok=True)

time.sleep(1)

# Exportation de la base de donnee wordpress
print("DUMP de la BDD")
os.system("mysqldump -u "+usermysql+" -p"+pwdmysql+" "+databasename+" > "+backup_folder+"/"+bddbackupname+".sql")

time.sleep(1)

print("Compression du repertoire html")
subprocess.call(['tar', '-czvf', tarhtml, html])

time.sleep(1)

print("Deplacement du repertoire html compresse")
shutil.move(tarhtml, backup_folder)

time.sleep(1)

print("Compression du repertoire de sauvegarde")
subprocess.call(['tar', '-czvf', backup_to_ftp_targz, backup_folder])

time.sleep(1)

print("Suppression du repertoire html compresse")
shutil.rmtree(backup_folder)

time.sleep(1)

print("Suppression des sauvegardes de + de 6 jours sur le serv FTP")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host,
            username=username,
            password=password)
commands = ['find /home/******/Documents/ -name "*.tar.gz" -ctime +6 -exec rm -rf {} \;']
for command in commands:
    stdin, stdout, stderr = ssh.exec_command(command)
    time.sleep(3)
    print(stdout.read().decode())
ssh.close()

time.sleep(1)

print("Deplacement de la sauvegarde du jour vers le serveur FTP")
from ftplib import FTP
ftp = FTP(host)
ftp.login(user=username, passwd=password)
ftp.cwd(destination)
def placeFile():
    filename = backup_to_ftp_targz
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.rename(filename, date+'.tar.gz')
    ftp.quit()
placeFile()

time.sleep(1)

print("Suppression du repetoire compresse contenant la sauvegarde journaliere")
os.remove(backup_to_ftp_targz)

print("Fin du traitement de la sauvegarde avec succes")







