# Surveillance de la Batterie

Cet extrait de code est un script Python qui surveille l'état de la batterie d'un appareil. Il utilise la bibliothèque `psutil` pour obtenir des informations sur la batterie et la bibliothèque `plyer` pour envoyer des notifications.

> ⚠️ Ce projet a été créé dans le but de surveiller la batterie de mon ordinateur portable et d'intégrer l'utilisation de l'IA dans mes projets de développement.

## Fonctionnalités

- **check_battery_status()**: Cette fonction permet de connaître l'état de la batterie, notamment de savoir si elle est branchée et quel est son pourcentage.
  
- **send_notification()**: Envoie une notification avec le titre et le message spécifiés en utilisant la bibliothèque `plyer`.

- **battery_monitor()**: Surveille l'état de la batterie et envoie des notifications lorsque la batterie est faible ou complètement chargée. La fonction tourne dans une boucle infinie et attend 60 secondes entre chaque vérification.
- 
## Intégration d'assistants de langage
Ce projet a été développé avec l'aide d'assistants de langage tels que ChatGPT de OpenAI et CodiumAi pour la rédaction de la documentation et l'assistance au développement.

## Utilisation

Pour utiliser ce code, les bibliothèques `psutil` et `plyer` doivent être installées. Le thread `battery_thread` est démarré et joint au thread principal pour garantir que le script continue à s'exécuter jusqu'à ce qu'il soit arrêté manuellement.

## Configuration

- **Seuils de batterie**: Les variables `LOW_BATTERY_THRESHOLD` et `FULL_BATTERY_THRESHOLD` définissent les seuils de pourcentage de batterie pour les niveaux de batterie faibles et pleins, respectivement.

- **Arrêt de la surveillance**: Pour arrêter la surveillance de la batterie, la variable `event` peut être définie pour déclencher un événement.

## Exécution

```bash
python script.py
```

## Auteur

Crée par VIRY Brandon.

