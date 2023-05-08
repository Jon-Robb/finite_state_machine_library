# <center> Connexion au robot GoPiGo3 avec Visual Studio Code

## Étape 1
### Téléchargez l'extension Remote-SSH
---
1. Cliquer sur l'icône extension

2. Chercher et installer Remote-SSH

![Extension Remote-SSH](../Recherche/VNC_recherche/img/Remote-SSH.PNG)

## Étape 2
### Connexion et mise en place via le robot
---

1. Allumez votre robot 

    - Attendez que la lumière soit verte et connectez-vous à celui-ci de la manière habituelle.

1. Créez-vous un dossier de travail nommé c64

## Étape 3
### Connexion à Visual Studio Code
---
1. Retournez sur Visual Studio Code et appuyez sur F1

    - Sélectionnez l'option **Remote-SSH : Connect to Host...**

![Connexion ssh](../Recherche/VNC_recherche/img/Remote-SSH_connexion.PNG)
1. Cliquez sur ajouter un nouvel hôte SSH
    - Entrée **ssh jupyter@10.10.10.10**

    - **IMPORTANT n'oubliez pas le ssh**
    - Sélectionnez le fichier où sauvegarder l'hôte ".../ssh/config"
1. Appuyez sur se connecter dans la notification en bas à droite
![Notification](../Recherche/VNC_recherche/img/boite_connexion.PNG)
1. Entrez le mot de passe **jupyter**
1. Cliquez sur Open Folder
    - Sélectionnez votre dossier de travail "home/jupyter/c64"
    
    - Entrez à nouveau le mot de passe **jupyter**

Vous êtes prêt à travailler!