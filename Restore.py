#########################################################################
#Titre		: Restore.py
#
# DESCRIPTION :
# Restauration d'un serveur wordpress/sql depuis un serveur distant (FTP)
#
# AUTEUR	: COIGNOUX Morgan
#
# Date 		: 02/02/2022
#
# REPO		: https://github.com/Kney26073869/ProjectA_6.git
#########################################################################

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Mise en forme de la bibliothèque : https://docs.python.org ###
# 								Documentation		: https://docs.python.org
#											: http://docs.paramiko.org
print("Importation de la biblioteque")
import os
import shutil
import time
import sys
import paramiko

# Mise en forme des variables
#
#
# '******' Entrer les parametres suivant les besoins
print("Mise en forme des variables")

# Informations concernant le traitement
path_restore = '/home/******/Restore'
target_day = '/home/******/Documents'
restore_folder = 'Restore'
targz = '.tar.gz'
dest_restore = path_restore+'/'+restore_folder+targz
localpath = dest_restore 
path_wordpress = target_day+'/'+restore_folder+targz	#wordpress
path = path_wordpress

# Choix du jour de la semaine
days_list = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
sunday = target_day+'/'+days_list[0]+targz
monday = target_day+'/'+days_list[1]+targz
tuesday = target_day+'/'+days_list[2]+targz
wednesday = target_day+'/'+days_list[3]+targz
thursday = target_day+'/'+days_list[4]+targz
friday = target_day+'/'+days_list[5]+targz
saturday = target_day+'/'+days_list[6]+targz

# Informations serveur wordpress
username = '******'
password = '******'
host = '******'
port = 22

print("Traitement de la sauvegarde")

# Création du répertoitre de restauration
print("Creation du repertoire de restauration")
os.makedirs(restore_folder, exist_ok=True)

time.sleep(1)

print("Selectionner la sauvegarde <=> 0:Sunday 1:Monday 2:Tuesday 3:wednesday 4:Thursday 5:Friday 6:Saturday")
while True:
    try:
        Day = int(input("Entrer le jour : "))
        if (Day == 0 or Day == 1 or Day == 2 or Day == 3 or Day == 4 or Day == 5 or Day == 6):
            break
        else:
            print("Date No Exist")
            exit();
    except ValueError:
        print("Date No Exist")
        exit();
if Day == 0 : shutil.copyfile(sunday, dest_restore)
elif Day == 1 : shutil.copyfile(monday, dest_restore)
elif Day == 2 : shutil.copyfile(tuesday, dest_restore)
elif Day == 3 : shutil.copyfile(wednesday, dest_restore)
elif Day == 4 : shutil.copyfile(thursday, dest_restore)
elif Day == 5 : shutil.copyfile(friday, dest_restore)
elif Day == 6 : shutil.copyfile(saturday, dest_restore)

time.sleep(1)

print("Deplacement de la sauvegarde selectionnee vers le serveur Wordpress")
transport = paramiko.Transport((host, port))
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put(localpath, path)
sftp.close()
transport.close()

time.sleep(1)

print("Suppression du repetoire compresse contenant la sauvegarde selectionnee")
os.remove(dest_restore)

time.sleep(1)

print("Execution des commandes pour le rétablissement du serveur Wordpress")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host,
            username=username,
            password=password)
commands =['cd /home/******/Documents/ && tar -xzvf /home/******/Documents/Restore.tar.gz',
           'rm /home/******/Documents/Restore.tar.gz',
           'cd /home/******/Documents/backup_to_ftp/ && tar -xzvf /home/******/Documents/backup_to_ftp/wp_html.tar.gz',
           'sudo cp -R /home/******/Documents/backup_to_ftp/var/www/html /var/www/',
           'mysql -u wpuser -pwpuserpw -e "CREATE DATABASE wordpressdb;"',
           'mysql -u wpuser -pwpuserpw wordpressdb < /home/******/Documents/backup_to_ftp/dumpbddwp.sql',
           'rm -r /home/******/Documents/backup_to_ftp']
for command in commands:
    stdin, stdout, stderr = ssh.exec_command(command)
    time.sleep(1)
    print(stdout.read().decode())
ssh.close()

print("Fin du traitement de la sauvegarde avec succes")
