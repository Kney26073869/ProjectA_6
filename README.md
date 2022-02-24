# ProjectA_6
OC PROJET6 Participez à la communauté

# Lab test
* Virtualbox
* GNS3

# Topologie
![topologie](https://user-images.githubusercontent.com/99196130/152831223-a28cc9ab-d326-4dc1-aecf-ab64dee3733e.png)

# Description
* Ce projet a pour but de sauvegarder/restaurer un site wordpress et sa base de données
* Possibilité de stocker les sauvegardes journalières sur 2 supports différents
    - Serveur FTP
    - Filezilla (client FTP)
* La sauvegarde et la restauration s'effectue à l’aide de deux scripts sous python 3.8
    - Backup.py
    - Restore.py

# Pré-requis/configuration : Super-user do
## Serveur wordpress/mysql
- Debian 10 : Graphical install
    - environnement de bureau Debian
    - serveur SSH
    - utilitaires usuels du système
        - apt-get update && apt-get upgrade
        - apt install apache2 php libapache2-mod-php mariadb-server php-mysql
        - apt install php-curl php-gd php-intl php-json php-mbstring php-xml php-zip
        - cd /var/www/
        - wget https://wordpress.org/latest.tar.gz
        - tar -zxvf latest.tar.gz
        - rm latest.tar.gz
        - cp -r wordpress/* /var/www/html
        - rm -r wordpress
        - chmod -R 777 /var/www/html
        - cp index.html index.html.bak
        - rm index.html 
        - mysql_secure_installation
            - Enter current password for root : Enter for none
            - Set root password? y
            - New password 
            - Remove anonymous user? y
            - Disallow root login remotely? y
            - Remove test database and access to it? y
            - Reload privileges tables now? y
        - mysql -u root -proot
            - MariaDB [()]> CREATE DATABASE xxxxxx;
            - MariaDB [()]> CREATE USER 'xxxxxx'@'localhost' IDENTIFIED BY 'xxxxxx';
            - MariaDB [()]> GRANT ALL PRIVILEGES ON xxxxxx.* TO 'xxxxxx'@'localhost';
            - MariaDB [()]> FLUSH PRIVILEGES;
            - MariaDB [()]> QUIT;
        - nano /etc/hosts
            - 127.0.0.1 localhost
            - 127.0.0.1 **nom du serveur** **wordpress.lan**
    - Postes clients
        - nano /etc/hosts
            - 192.168.1.2   **wordpress.lan**  
             
* Configurations de base du serveur en raison du fait qu’il n’y a pas d’autorité DNS serveur sur le réseau. Mappage de l’adresse IP du serveur au (faux) nom de domaine virtuel pour pouvoir y accéder comme un vrai nom de domaine depuis n’importe quel navigateur
              
    - Navigateur Firefox
        - xxx.xxx.xxx.xxx/wp-admin/setup-config.php ou wordpress.lan/wp-admin/setup-config.php
            - **Let's go!**
        - xxx.xxx.xxx.xxx/wp-admin/setup-config.php,step=1
            - Database = xxxxxx
            - Username = xxxxxx
            - Password = xxxxxx
            - Database HOST = localhost
            - Table Prefix = wp_
            - **Submit**  
        - xxx.xxx.xxx.xxx/wp-admin/setup-config.php,step=2 
            - **Run the installation** 
        - xxx.xxx.xxx.xxx/wp-admin/install.php?language=en_US
            - Site Title = xxxxxx
            - Username = xxxxxx
            - Password = xxxxxx
            - Confirm Password
            - Your Email = xxxxxx@xxxxxx.x
            - Search engine visibility
            - **Install Wordpress**  
        - xxx.xxx.xxx.xxx/wp-admin/install.php?step=2
            - Success!
            - **Log In**  
        - xxx.xxx.xxx.xxx/wp-login.php
            - Username or Email Address
            - Password
            - **Log In**      
        - xxx.xxx.xxx.xxx/wp-admin/
            - **Welcome to Wordpress!** 

## Serveur FTP
* Possibilité de créer un utilisateur commun et non celui de l'installateur entre le serveur FTP et le client FTP
- Debian 10 : Graphical install
    - environnement de bureau Debian
    - serveur SSH
    - utilitaires usuels du système
        - apt-get update && apt-get upgrade
        - apt install vsftpd
        - cd /etc
        - cp vsftpd.conf vsftpd.conf.bak
        - nano vsftpd.conf (modification du fichier)
            - utilisateur commun ou utillisateur d'installation            
        - cat vsftpd.conf | grep -v "^#"
            - listen=YES
            - anonymous_enable=NO
            - local_enable=YES
            - write_enable=YES
            - dirmessage_enable=YES
            - use_localtime=YES
            - xferlog_enable=YES
            - listen_port=21
            - chroot_local_user=YES
            - chroot_list_enable=YES
            - chroot_list_file=/etc/vsftpd.chroot_list
            - secure_chroot_dir=/var/run/vsftpd/empty
            - pam_service_name=vsftpd
            - rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
            - ras_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
            - ssl_enable=NO  
        - nano vsftpd.chroot_list (Création du fichier & modification du fichier)
            - /utilisateur d'installation/utilisateur commun
        - systemctl restart vsftpd.service

## Client FTP
- Debian 10 : Graphical install
    - environnement de bureau Debian
    - serveur SSH
    - utilitaires usuels du système
        - apt-get update && apt-get upgrade
        - apt -y install filezilla
            - Ajouter aux favoris
            - Executer FilZilla
                - Hôte = xxx/xxx/xxx/xxx
                - Identifiant = utilisateur commun ou utillisateur d'installation serveur FTP 
                - Mot de passe = xxxxxx
                - Port = 21 ou laisser le champ vide
                - Connexion rapide
                - **Valider**
                    - Transfert des sauvegardes entre le serveur FTP et le client

# Mise en place des scripts
## Serveur wordpress/mysql : Backup.py
- Les étapes pour pouvoir exécuter le script
    - apt install python3-pip
    - apt-get install libffi-dev
    - python3 -m pip install paramiko
- Télécharger le script ou effectuer un copier/coller du contenu dans un éditeur de texte
- Copier le script à la racine du disque
- Mettre les droits d'exécution si nécessaire
    - chmod +x Backup.py
- Éditer le script pour enregistrer les différents paramètres dans les parties concernées
    - python3 Backup.py

## Automatisation du script du script avec Crontab pour une sauvegarde journalière
- Ex : Tous les jours à 23h59
    - Terminal 
        - crontab -e : Choix de l'éditeur de texte
            - L'éditeur de texte apparaît 
                - #m h  dom mon dow   command
                - #Tous les jours a 11h59
                - 59 11 * * * python3 /root/Backup.py >> /home/adminstal/Documents/log.file 2>&1
                    - systemctl restart cron 

## Serveur FTP : Restore.py
- Les étapes pour pouvoir exécuter le script
    - apt install python3-pip
    - apt-get install libffi-dev
    - python3 -m pip install paramiko
- Télécharger le script ou effectuer un copier/coller du contenu dans un éditeur de texte
- Copier le script à la racine du disque
- Mettre les droits d'exécution si nécessaire
    - chmod +x Restore.py
- Éditer le script pour enregistrer les différents paramètres dans les parties concernées
- Sur le serveur wordpress/mysql
    - nano /etc/sudoers
        - adminstal     ALL=(ALL:ALL) NOPASSWD:ALL
    - mysql -u root -proot
        - MariaDB [()]> CREATE USER 'xxxxxx'@'localhost' IDENTIFIED BY 'xxxxxx';
        - MariaDB [()]> QUIT;
- Sur le serveur FTP
    - python3 Restore.py
