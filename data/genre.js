/* Le Lexique — couche de genre (gender layer)
   ─────────────────────────────────────────────────────────────────────
   Le corpus ne garde qu'une forme : « un employé ». Sans cette couche,
   l'élève qui écrit « une employée » est compté faux alors que sa
   réponse est juste.

   Cette couche ne modifie PAS les listes. app.js fabrique l'autre forme
   au moment de la correction, à partir des règles ci-dessous, et
   l'accepte. Ajouter un couple irrégulier ici l'active d'un coup dans
   tout le corpus.
   ───────────────────────────────────────────────────────────────────── */
window.GENERO = {
  arts: [["le","la"],["un","une"],["les","les"],["des","des"]],

  suffixes: [
    ["eur","euse"],   // un chanteur    → une chanteuse
    ["teur","trice"], // un acteur      → une actrice
    ["ier","ière"],   // un ouvrier     → une ouvrière
    ["er","ère"],     // un boulanger   → une boulangère
    ["ien","ienne"],  // un pharmacien  → une pharmacienne
    ["on","onne"],    // un patron      → une patronne
    ["at","atte"],
    ["el","elle"],    // professionnel  → professionnelle
    ["f","ve"],       // sportif        → sportive
    ["x","se"],       // heureux        → heureuse
    ["", "e"]         // un employé     → une employée
  ],

  /* Terminaisons réellement épicènes. Surtout pas "e" tout seul :
     « la chanteuse » deviendrait « le chanteuse ». */
  invariable: ["iste","aire","logue","graphe","able","ible"],

  pairs: [
    ["homme","femme"],      ["mari","femme"],       ["père","mère"],
    ["parrain","marraine"], ["roi","reine"],        ["prince","princesse"],
    ["duc","duchesse"],     ["comte","comtesse"],   ["héros","héroïne"],
    ["neveu","nièce"],      ["gendre","belle-fille"],["copain","copine"],
    ["vieux","vieille"],    ["beau","belle"],       ["nouveau","nouvelle"],
    ["fou","folle"],        ["frais","fraîche"],    ["favori","favorite"],
    ["serviteur","servante"],["dieu","déesse"],     ["taureau","vache"],
    ["élève","élève"],["enfant","enfant"],["camarade","camarade"],
    ["collègue","collègue"],["adulte","adulte"],["architecte","architecte"],
    ["photographe","photographe"],["interprète","interprète"],
    ["bénévole","bénévole"],["gosse","gosse"],["cadre","cadre"],
    ["juge","juge"],["membre","membre"],["ministre","ministre"],
    ["guide","guide"],["élu","élue"]
  ],

  /* Mots que la règle transformerait à tort — « le livre » / « la livre »,
     « le tour » / « la tour ». Les deux membres sont bloqués. */
  excepciones: [
    ["livre","livre"],["tour","tour"],["poste","poste"],["mode","mode"],
    ["manche","manche"],["voile","voile"],["somme","somme"],["page","page"],
    ["vase","vase"],["moule","moule"],["critique","critique"],
    ["physique","physique"],["mémoire","mémoire"],["aide","aide"],
    ["garde","garde"],["solde","solde"],["œuvre","œuvre"],
    ["espace","espace"],["greffe","greffe"],["pendule","pendule"],
    ["poêle","poêle"],["mousse","mousse"],["crêpe","crêpe"],
    ["finale","finale"],["cours","course"],["part","part"],["pot","pote"],
    ["chat","chatte"],["son","sonne"],["don","donne"],["ton","tonne"],
    ["bon","bonne"],["salon","salonne"],["camion","camionne"],
    ["avion","avionne"],["ballon","ballonne"],["béton","bétonne"],
    ["coton","cotonne"],["citron","citronne"],["wagon","wagonne"],
    ["talon","talonne"],["préjugé","préjugée"],["projecteur","projecteuse"],
    ["moteur","moteuse"],["secteur","secteuse"],["facteur","facteuse"],
    ["ordinateur","ordinateuse"],["bonheur","bonheuse"],
    ["malheur","malheuse"],["honneur","honneuse"]
  ],

  /* Noms de personne. Un nom précédé d'un article ne change de genre que
     s'il figure ici (ou dans "pairs") : « un employé » oui, « le travail »
     non. Les adjectifs seuls — sans article — n'en ont pas besoin.
     Quand tu ajoutes un métier au corpus, ajoute le mot ici. */
  personas: [
    "acteur", "adepte", "adhérent", "adolescent", "adulte", "africain",
    "agriculteur", "algérien", "allemand", "alsacien", "ami", "américain",
    "anglais", "annonceur", "antillais", "apprenti", "argentin", "artisan",
    "artiste", "asiatique", "assassin", "auditeur", "auteur", "avocat",
    "bachelier", "belge", "berger", "bordelais", "boulanger", "boxeur",
    "breton", "brésilien", "bénévole", "camerounais", "canadien",
    "candidat", "chanteur", "cheminot", "chercheur", "chilien", "chinois",
    "chirurgien", "chômeur", "citoyen", "coiffeur", "collaborateur",
    "collégien", "colombien", "commerçant", "communiste", "comédien",
    "congolais", "conseiller", "consommateur", "corse", "coréen", "cousin",
    "croyant", "créateur", "cubain", "célibataire", "danois", "danseur",
    "descendant", "dessinateur", "directeur", "dirigeant", "débutant",
    "défenseur", "dénonciateur", "déporté", "député", "détenteur",
    "détenu", "employeur", "employé", "enfant", "enseignant", "espagnol",
    "européen", "finlandais", "fonctionnaire", "frontiste", "gagnant",
    "gallois", "gardien", "gendarme", "grec", "gréviste", "habitant",
    "historien", "hollandais", "immigrant", "immigré", "indien",
    "infirmier", "instituteur", "internaute", "interprète", "iranien",
    "irlandais", "israélien", "italien", "ivoirien", "japonais",
    "jardinier", "joueur", "journaliste", "jumeau", "juré", "latino",
    "lecteur", "libanais", "locataire", "lycéen", "lyonnais", "maire",
    "marié", "marocain", "marseillais", "meurtrier", "mexicain",
    "milicien", "militaire", "militant", "musicien", "mécanicien",
    "nigérian", "normand", "norvégien", "occupant", "ouvrier",
    "pakistanais", "parent", "parisien", "partenaire", "partisan",
    "patron", "paysan", "perdant", "pharmacien", "policier", "politicien",
    "polonais", "pompier", "portugais", "professeur", "propriétaire",
    "provençal", "proviseur", "président", "péruvien", "refugié",
    "retraité", "revendeur", "riverain", "russe", "réalisateur",
    "réfractaire", "réfugié", "résistant", "salarié", "scientifique",
    "scénariste", "serveur", "socialiste", "sociologue", "spectateur",
    "sportif", "stagiaire", "suisse", "supporteur", "survivant", "suédois",
    "syndicaliste", "syrien", "sénégalais", "technicien", "touriste",
    "travailleur", "traître", "tunisien", "turc", "téléspectateur",
    "utilisateur", "vainqueur", "vendeur", "veuf", "villageois", "voisin",
    "écolier", "écologiste", "écossais", "écrivain", "éditeur", "égyptien",
    "électeur", "électricien", "élève", "époux", "étranger", "étudiant"
  ],

  stops: ["de","du","des","à","au","aux","en","avec","sans","par","pour","que","qui","et","ou","comme"]
};
