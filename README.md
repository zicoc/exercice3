# exercice3
Développer une application temps réel qui interroge périodiquement le flux GTFS Realtime et affiche pour chaque ligne disponible dans le flux:    
- le nom du prochain arrêt
- L'heure de passage ajustée en fonction du délai
- La distance en ligne droite en le véhicule et l'arrêt


# installation des dependances
pip install requests gtfs-realtime-bindings time peewee protobuf aiohttp geopy
