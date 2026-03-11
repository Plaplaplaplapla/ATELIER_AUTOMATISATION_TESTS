# API Choice

Étudiant : Eliott Deprade
API choisie : PokéAPI
URL base : https://pokeapi.co/api/v2/
Documentation officielle / README : https://pokeapi.co/docs/v2/
Auth : aucune (API publique, pas de clé requise)
Endpoints testés :
GET /pokemon/
GET /pokemon/bulbasaur
Hypothèses de contrat (champs attendus, types, codes) :
Code HTTP attendu : 200 pour ressource valide, 404 pour ressource inexistante, 5xx erreur serveur
Réponse au format JSON
Champs attendus : id (integer), name (string), height (integer), weight (integer), abilities (array)
Limites / rate limiting connu :
aucune limite officielle documentée, mais recommandation d’éviter un volume élevé de requêtes
Risques (instabilité, downtime, CORS, etc.) :
indisponibilité temporaire de l’API
erreurs réseau
changement du schéma JSON
ralentissement ou blocage en cas de trop nombreuses requêtes simultanées
