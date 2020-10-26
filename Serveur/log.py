""" Create log file for AWS bucket """
import datetime

def create_log_txt(liste, result):
    # Entrees :
    # les notes en format "1/3/5/7/9"
    # la sortie process_marks_raw() du calcul des notes
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    fichier_log = open("fichier_log.txt", "w")
    fichier_log.write(now + "\n")
    liste = liste.replace("/", " ")
    fichier_log.write(liste + "\n")
    fichier_log.write(result + "\n")
    fichier_log.close()


# Test

create_log_txt("1/2/3", "1 3 2 2")
