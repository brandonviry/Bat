"""
Cet extrait de code est un script Python qui surveille l'état de la batterie d'un appareil. Il utilise la bibliothèque psutil pour obtenir des informations sur la batterie et la bibliothèque plyer pour envoyer des notifications. 

Le code définit une fonction check_battery_status() qui récupère l'état de la batterie, y compris si elle est branchée et le pourcentage de la batterie. Une autre fonction, send_notification(), est définie pour envoyer des notifications à l'aide de la bibliothèque plyer.

La fonction principale battery_monitor() vérifie en permanence l'état de la batterie et envoie des notifications si la batterie est faible ou complètement chargée. Elle utilise deux seuils, LOW_BATTERY_THRESHOLD et FULL_BATTERY_THRESHOLD, pour déterminer quand envoyer des notifications. La fonction s'exécute dans un thread séparé à l'aide du module de threading.

Pour utiliser ce code, les bibliothèques psutil et plyer doivent être installées. Le thread battery_thread est démarré et joint au thread principal pour garantir que le script continue à s'exécuter jusqu'à ce qu'il soit arrêté manuellement.

Remarque : cet extrait de code est fourni à titre de contexte et n'inclut pas d'utilisation réelle ou d'intégration avec d'autres codes.
"""

import psutil
from plyer import notification
import threading


LOW_BATTERY_THRESHOLD = 20
FULL_BATTERY_THRESHOLD = 80


def check_battery_status():
    """
    Cette fonction permet de connaître l'état de la batterie, notamment de savoir si elle est branchée et quel est son pourcentage.

    Retourne :
        un tuple : Un tuple contenant deux valeurs :
            - plugged (bool) : True si la batterie est branchée, False sinon.
            - percent (int) : Le pourcentage de la batterie.

    Remarque :
        Cette fonction s'appuie sur la bibliothèque psutil pour récupérer les informations relatives à la batterie.
    """

    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent
    return plugged, percent


def send_notification(title, message):
    """Envoie une notification avec le titre et le message spécifiés en utilisant la bibliothèque plyer.

    Paramètres :
        titre (str) : Le titre de la notification.
        message (str) : Le message de la notification.

    Retourne :
        Aucun

    Note : Cette fonction s'appuie sur la bibliothèque plyer pour l'envoi des notifications :
        Cette fonction s'appuie sur la bibliothèque plyer pour envoyer des notifications.

    """
    notification.notify(title=title, message=message,
                        app_name="Battery Monitor")


def battery_monitor():
    """
    Surveille l'état de la batterie et envoie des notifications lorsque la batterie est faible ou complètement chargée.

    Retourne :
        Aucun

    Remarque :
        Cette fonction vérifie en permanence l'état de la batterie à l'aide de la fonction « check_battery_status » et envoie des notifications à l'aide de la fonction « send_notification » lorsque la batterie est faible ou complètement chargée. Elle utilise la bibliothèque « psutil » pour récupérer les informations relatives à la batterie et la bibliothèque « plyer » pour envoyer des notifications.

        La fonction tourne dans une boucle infinie et attend 60 secondes entre chaque vérification. Elle garde en mémoire le dernier état de la batterie afin d'éviter d'envoyer des notifications en double.

        Les variables 'LOW_BATTERY_THRESHOLD' et 'FULL_BATTERY_THRESHOLD' du module 'bat.py' définissent les seuils de pourcentage de batterie pour les niveaux de batterie faibles et pleins, respectivement.

        Pour arrêter la surveillance de la batterie, la variable 'event' du module 'bat.py' peut être définie pour déclencher un événement.

    """
    last_status = None
    while True:
        plugged, percent = check_battery_status()
        if (percent <= LOW_BATTERY_THRESHOLD and last_status != "low") or (
            percent >= FULL_BATTERY_THRESHOLD and plugged and last_status != "full"
        ):
            if percent <= LOW_BATTERY_THRESHOLD:
                message = (
                    f"La batterie est à {
                        percent}% - Veuillez brancher le chargeur!"
                )
                send_notification("Batterie Faible", message)
                last_status = "low"
            elif percent >= FULL_BATTERY_THRESHOLD and plugged:
                message = (
                    "La batterie est complètement chargée. Débranchez le chargeur!"
                )
                send_notification("Batterie Chargée", message)
                last_status = "full"
        event.wait(60)


"""Démarre un nouveau thread pour surveiller l'état de la batterie et attend qu'il se termine.

Retourne :
    Aucun

Remarques :
    Cet extrait de code crée un nouveau thread à l'aide du module de threading pour exécuter la fonction « battery_monitor » en arrière-plan. La fonction « battery_monitor » est chargée de surveiller l'état de la batterie et d'envoyer des notifications lorsque la batterie est faible ou complètement chargée.

    L'argument 'daemon=True' garantit que le thread se terminera lorsque le programme principal se terminera.

    L'appel « battery_thread.join() » est utilisé pour attendre que le thread se termine avant de poursuivre le programme principal. Cela permet de s'assurer que le programme principal ne se termine pas avant la fin de la surveillance de la batterie.

    La variable 'event' est utilisée pour contrôler l'exécution de la fonction 'battery_monitor'. Par défaut, la variable 'event' n'est pas définie, de sorte que la fonction 'battery_monitor' s'exécute indéfiniment. Pour arrêter la surveillance de la batterie, la variable 'event' peut être définie pour déclencher un événement.
"""


event = threading.Event()
battery_thread = threading.Thread(target=battery_monitor, daemon=True)
battery_thread.start()

battery_thread.join()
