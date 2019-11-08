# Map Matching

Le Map Matching est la technologie et les algorithmes permettant de faire coincider un tracé géographique avec une carte.
Ce Map Matching en correlation avec l'itinéraire relatif tracé aupars avant pourrait permettre de déduire l'emplacement de la personne à partir d'une carte préenregistrée.

Dans l'article *Map Matching Algorithm and Its Application*, Lianxia Xi et ses collègues étudient les différents agorithmes permettant de faire coincider un tracé géographique avec une carte et les problèmes que l'on peut rencontrer dans le processus.
L'algorithme "Position Matching" permet de projeter un point d'un tracé GPS sur une route aux alentours par l'évaluation de la distance qui sépare la position de la route le plus proche et la différencee d'angle entre la direction mesurée et la direction de la route.
Apres avoir éliminé les cas dépassant un seuil, on séléctionne la route qui minimise les deux valeurs.
Dans notre cas, l'évaluation de ces deux variables permettrais de trouver la position de l'utilisateur sur la route la plus proche.
Mais cela implique de connaitre la position actuel de l'utilisateur, ce que l'on essaie de trouver dans notre cas.

## Algorithme

L'algorithme du système de localisation se base sur deux étapes.
Une première étape de pré-traitement permettant de générer un fichier de données organisant les données de la carte d'une certaine mainière permettant un traitement rapide des données sur le terrain.

Les données pré-traitées sont alors utilisées en live dans le boitier.

### Algorithme de pré-traitement

L'algorithme de pré-traitement s'opère suivant les étapes suivantes :

1. Subdiviser la carte OSM en tronçons de taille fixe à définir
2. Construction d'un graph des tronçons composé de point liant les tronçons dans l'espace (latitude, longitude) entre eux. Chaque relation représantant un itinéraire possible entre deux points et reliés par un tronçon
3. Classifier et regrouper les tronçons suivant un algorithme de comparaison de courbe avec une tolérance faible
4. Synthetisation des classes de tronçon en tronçons "moyens"
5. Construction de l'arbre de localisation

### Format de données

Les données pré-traitées sont contenues dans un fichier (probablement Protocol Buffer) sont les suivantes :

* Le graph des points et de tronçons en relation
* Les classes de tronçons
* L'arbre de localisation

#### Graph de points

Le graph contiens en point les liaisons entre les tronçons de taille fixée et leur latitude-longitude.
Les relations entre ces points est le tronçon de route permettant le passage du point à l'autre

#### Arbre de localisation

L'arbre de décision permet de déduire les localisation possible en fonction de l'itinéraire pris.
Il est composé des différentes classes de tronçons regroupés en arbre.

## Ressources

* [https://en.wikipedia.org/wiki/Map_matching](https://en.wikipedia.org/wiki/Map_matching)
* [https://www.atlantis-press.com/proceedings/iske2007/1316](https://www.atlantis-press.com/proceedings/iske2007/1316)
* [https://blog.mapbox.com/matching-gps-traces-to-a-map-73730197d0e2](https://blog.mapbox.com/matching-gps-traces-to-a-map-73730197d0e2)