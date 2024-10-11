
![Logo](https://i.ibb.co/3vFT42G/image.png)


# File Share App

Utilisez ce programme pour partager des fichiers avec vos amis.




## Fonctionnalités

- Partage de fichiers volumineux
- Ajouter un mot de passe
- Personnaliser le site de téléchargement
- Interface simple


## Comment utiliser ?
Clonez et installez le script

```bash
  git clone https://github.com/SkillFXX/file-share-app.git
  cd file-share-app
  pip install -r requirements.txt
```

Lancez le fichier `main.py` et commencez à l'utiliser.


## FAQ

#### Comment accéder aux fichiers depuis un réseau différent ?
Vous devez ouvrir le port 5000 sur votre réseau afin que d'autres personnes sur des réseaux différents puissent accéder à vos fichiers. Une fois cela fait, ils devront simplement rechercher votre IP publique suivie du port 5000 (par exemple : 108.177.16.0:5000) dans un navigateur. Cependant, si vous êtes déjà connecté au même réseau que l'hôte, vous n'aurez besoin que d'entrer son IP locale et le port 5000 (par exemple : 128.0.0.0:5000).

