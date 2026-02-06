# Comment lancer des primitives à Poppy à partir de la connexion au Hotspot (pour Windows):

- Installer [Postman](https://www.postman.com/). Le télécharger sur sa propre machine (laptop)
- Ne pas se connecter à Postman avec un compte. Si nécessaire, se connecter puis se déconnecter.
- Lancer le robot (alimentation *on*)
- Se connecter à partir de sa machine sur le hotspot de poppy.
    - Mot de passe : poppyproject
- Aller sur un *browser* web. Rentrer l'ip suivant : 
    - 10.99.99.1
- Cliquer sur le bouton *what is happening ?*
- Reboot Robot API
- Revenir au menu principal
- Aller dans Monitor and Control
- On peut alors voir la température en *live* des moteurs.
- Aller sur Postman sans être connecté.
- Toutes les requêtes commencent par l'ip de poppy et son port : 
    - 10.99.99.1:8080/.......suite
- Lancer la requête GET suivante pour obtenir la liste des primitives: 
    - primitives/list.json
- Liste de toutes les requêtes : 

```txt
/robot.json
/ip.json
/motors/list.json
/motors/aliases/list.json
/motors/<alias>/list.json
/motors/<motor_name>/registers/list.json
/motors/<motor_name>/registers/<register_name>/value.json
/motors/registers/<register_name>/list.json
/sensors/list.json<br>/sensors/<sensor_name>/registers/list.json
/sensors/<sensor_name>/registers/<register_name>/value.json
/sensors/camera/frame.png
/sensors/code/<code_name>.json
/records/list.json
/records/<move_name>/value.json
/primitives/list.json
/primitives/running/list.json
/primitives/<primitive_name>/start.json
/primitives/<primitive_name>/stop.json
/primitives/<primitive_name>/pause.json
/primitives/<primitive_name>/resume.json
/primitives/<primitive_name>/properties/list.json
/primitives/<primitive_name>/properties/<prop>/value.json
/primitives/<primitive_name>/methods/list.json
/ik/<chain_name>/value.json
/ik/<chain_name>/rpy.json

Post method url:
/motors/<motor_name>/registers/<register_name>/value.json
/motors/<motor_name>/goto.json
/motors/goto.json
/sensors/<sensor_name>/registers/<register_name>/value.json
/records/<move_name>/record.json
/records/<move_name>/save.json
/records/<move_name>/play.json
/records/<move_name>/stop.json
/records/<move_name>/delete.json
/primitives/<primitive_name>/properties/<prop>/value.json
/primitives/<primitive_name>/methods/<method_name>/args.json
/ik/<chain_name>/goto.json
```


- Par la suite, on peut lancer des requêtes GET pour les primitives de Poppy, dont notamment stand_position, avec la syntaxe suviante : 
    - 10.99.99.1:8080/primitives/stand_position/start.json
- ATTENTION ! Les primitives qui ne sont pas stoppées avec stop.json reviendront éventuellement dans le comportement de Poppy. Autrement dit, elles ne sont pas arrêtées.