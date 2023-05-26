# Rapport

## Membres de l'équipe

L'équipe est composée de Jonathan Robinson-Roberge, Nathaelle Fournier, Quoc Huan Tran et Andrzej Wisniowski.

## Librairie FiniteStateMachine

Notre travail est estimé à environ 90% proche de la conception donnée. Tous les éléments demandés ont été réalisés. Cependant, nous avons rencontré quelques problèmes mineurs dans la gestion des lumières pour la deuxième tâche du robot qui sont encore à résoudre.

## Infrastructure

### C64Project

La classe C64Project a été conçue pour réaliser plusieurs fonctions :

- Validation de l'intégrité du robot : Ce processus confirme que tous les composants du robot fonctionnent correctement avant son déploiement.
- Gestion de démarrage du robot : Cette fonctionnalité permet au robot de démarrer correctement.
- Gestion des tâches du robot : Cette partie permet au robot d'exécuter les tâches demandées.
- Gestion de fin d'application : Cette fonctionnalité permet à l'application de se terminer correctement.

### Robot

La classe Robot a été conçue pour réaliser plusieurs fonctions :

- Gestion de la télécommande : Cette fonctionnalité permet de contrôler le robot à distance.
- Gestion du télémètre : Cette partie assure la capacité du robot à mesurer les distances.
- Gestion de la couleur pour les yeux (la classe EyeBlinkers) : Cela donne au robot la capacité de changer la couleur de ses yeux, de les ouvrir et del es fermer.
- Gestion des phares : Cette fonctionnalité permet au robot d'allumer et d'éteindre ses phares.

### Infrastructure du logiciel

Notre logiciel est divisé en trois niveaux d'abstraction. Le premier offre une machine d'état générique avec un plan, des états et des transitions. Le deuxième propose des sous-classes ajoutant des fonctionnalités plus rapprochées du besoin réel, et le troisième permet de contrôler un robot gopigo. Cette structure modulaire facilite l'ajout de nouvelles tâches au robot simplement en ajoutant une nouvelle machine d'état à sa liste de machines d'états.

## Autres éléments d'abstraction

Une abstraction particulièrement notable dans notre travail concerne la structure hiérarchique imbriquée que nous avons mise en place avec nos classes d'états et de machines d'état. Cette configuration ressemble en effet à celle d'un mini système d'exploitation.

Chaque instance de notre classe d'état est capable de posséder une machine d'état. Cela signifie que, dans notre architecture, non seulement une machine d'état peut posséder plusieurs états, mais aussi qu'un état peut lui-même posséder une autre machine d'état. Cette hiérarchie imbriquée crée une structure complexe qui peut être ajustée de manière flexible pour répondre aux diverses exigences de notre système.

Cela est semblable à la manière dont un système d'exploitation gère les processus et les threads. De même que dans notre architecture, un processus dans un système d'exploitation peut avoir plusieurs threads, et ces threads peuvent eux-mêmes générer d'autres processus ou threads. Cette comparaison met en lumière la puissance de notre approche en termes de modularité et d'extensibilité.

## Conclusion

Nous sommes fiers de ce que nous avons accompli avec cette librairie FiniteStateMachine et la façon dont nous avons abordé les défis du projet. Nous sommes confiants que les problèmes mineurs de gestion des lumières pourraient être résolus facilement avec un peu plus de temps.
