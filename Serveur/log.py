""" Create log file for AWS bucket """
import os, datetime

def create_log_txt(liste, result):
    # Entrees :
    # liste = les notes en format "1/3/5/7/9"
    # result = la sortie raw_result de process_marks()
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    liste = liste.replace("/", " ")
    
    fichier_log = open("fichier_log.txt", "w")
    fichier_log.write(now + "\n")
    fichier_log.write(liste + "\n")
    fichier_log.write(result + "\n")
    fichier_log.close()


def delete_log_txt():
    os.remove("fichier_log.txt")

