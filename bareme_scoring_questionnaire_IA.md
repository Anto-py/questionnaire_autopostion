# Barème de scoring
## Questionnaire d'autopositionnement « Quel utilisateur d'IA es-tu ? »
*Version 2.0 — 2025*

---

## Principes généraux

| Score | Signification | Description |
|---|---|---|
| 0 | Non scoré | Question de contexte ou question ouverte |
| 1 | Angle mort | L'enjeu est ignoré, non perçu ou activement écarté |
| 2 | Conscience émergente | L'enjeu est perçu mais sans outillage ni pratique |
| 3 | Maîtrise partielle | Des pratiques existent mais restent intuitives ou instables |
| 4 | Maîtrise active | L'enjeu est intégré à la pratique professionnelle de façon réfléchie |

**Questions Likert (échelle 1→5)** : le score brut est conservé tel quel (1→5). Pour le calcul du score d'enjeu, la moyenne est calculée sur l'ensemble des questions scorées, qu'elles soient sur 4 ou sur 5 — le radar normalise ensuite les valeurs sur une échelle commune 0→100%.

**Questions de posture sans hiérarchie** : toutes les réponses valent 2 (conscience de l'enjeu présente), sauf indifférence explicite = 1 et réflexion approfondie et outillée = 4. La *nature* de la position est traitée qualitativement par l'IA dans le rapport.

**Questions ouvertes** : score = 0. Transmises telles quelles à l'API pour traitement qualitatif. Ne pas inclure dans le calcul du score d'enjeu.

---

## 🧭 MISE EN ROUTE — Questions de contexte

> Ces deux questions ne sont pas scorées. Elles déterminent le **ton et le niveau de personnalisation** du rapport individuel.

| Question | A | B | C | D | Usage |
|---|---|---|---|---|---|
| M1 — Rapport à l'IA | — | — | — | — | Profil débutant / intermédiaire / avancé |
| M2 — IA dans l'école | — | — | — | — | Contexte institutionnel |

**Mapping pour le rapport :**

| M1 | Profil assigné |
|---|---|
| A | `debutant` |
| B | `observateur` |
| C | `experimentateur` |
| D | `integrateur` |

---

## 🔵 ENJEU 1 — ÉTHIQUE

**Score d'enjeu = moyenne de E1 + E2 + E3 + E4 + E5 + E6**
*(E7 = question ouverte, non scorée)*

| Question | A | B | C | D | Note |
|---|---|---|---|---|---|
| **E1** — Transparence du collègue | 1 | 2 | 3 | 4 | Continuum de conscience déontologique |
| **E2** — Personnalisation algorithmique | 1 | 2 | 3 | 3 | Question de posture : A = indifférence, B/C/D = positions toutes valides mais D = réflexion la plus approfondie → 3 pour B et C, 3 pour D (pas de hiérarchie entre elles) |
| **E3** — Déclaration d'usage IA | 1 | 1 | 3 | 4 | A et B sont deux formes d'absence de pratique |
| **E4** — Préoccupation principale | 2 | 2 | 2 | 2 | Question de posture : toutes les réponses témoignent d'une conscience des enjeux |
| **E5** — Likert capacité à aborder l'éthique | 1 | 2 | 3 | 4 | 5 → 4 (regrouper 4 et 5 = maîtrise active) |
| **E6** — Responsabilité en cas de contenu biaisé | 1 | 2 | 3 | 4 | D = compréhension de la complexité de la responsabilité partagée |
| **E7** — Question ouverte | 0 | 0 | 0 | 0 | Traitement qualitatif uniquement |

**Correction E5 (Likert 1→5 → score 1→4) :**

| Likert | Score |
|---|---|
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |
| 5 | 4 |

---

## 🟢 ENJEU 2 — JURIDIQUE

**Score d'enjeu = moyenne de J1 + J2 + J3 + J4 + J5 + J6**
*(J7 = question ouverte, non scorée)*

| Question | A | B | C | D | Note |
|---|---|---|---|---|---|
| **J1** — Données élèves dans les prompts | 1 | 1 | 3 | 4 | A et B = absence de conscience RGPD |
| **J2** — Connaissance AI Act | 1 | 2 | 3 | 4 | Continuum de connaissance |
| **J3** — Cadre établissement sur l'IA | 4 | 2 | 2 | 1 | A = cadre existant et connu ; D = angle mort institutionnel |
| **J4** — Droit d'auteur image IA | 1 | 2 | 3 | 4 | Continuum de connaissance juridique |
| **J5** — Likert cadre juridique | 1→5 | | | | Score direct |
| **J6** — Compte élève mineur | 1 | 2 | 3 | 1 | A = absence de conscience ; D = même absence sous forme d'ignorance ; B = conscience partielle ; C = connaissance correcte |
| **J7** — Question ouverte | 0 | 0 | 0 | 0 | Traitement qualitatif uniquement |

**Correction J5 (Likert 1→5) :** score direct sans conversion.

---

## 🟡 ENJEU 3 — ÉCOLOGIQUE

**Score d'enjeu = moyenne de Éco1 + Éco2 + Éco3 + Éco4 + Éco5 + Éco6**
*(Éco7 = question ouverte, non scorée)*

| Question | A | B | C | D | Note |
|---|---|---|---|---|---|
| **Éco1** — Consommation énergétique IA | 1 | 2 | 3 | 4 | Continuum de connaissance + intégration dans les usages |
| **Éco2** — Usage pédagogique de l'argument écologique | 1 | 3 | 4 | 2 | A = rejet ; D = posture disciplinaire restrictive (non-implication) ; B et C = usages pédagogiques légitimes, C plus constructif |
| **Éco3** — Likert sobriété numérique personnelle | 1→5 | | | | Score direct |
| **Éco4** — Connaissance Compar:IA | 1 | 2 | 3 | 4 | Continuum connaissance → usage → transfert pédagogique |
| **Éco5** — Choisir un modèle frugal | 1 | 2 | 3 | 4 | Continuum de conscience → réflexe → intégration |
| **Éco6** — Aborder l'impact environnemental en classe | 1 | 2 | 3 | 4 | Continuum de pratique pédagogique |
| **Éco7** — Question ouverte | 0 | 0 | 0 | 0 | Traitement qualitatif uniquement |

---

## 🔴 ENJEU 4 — ESPRIT CRITIQUE

**Score d'enjeu = moyenne de EC1 + EC2 + EC3 + EC4 + EC5 + EC6**
*(EC7 = question ouverte, non scorée)*

| Question | A | B | C | D | Note |
|---|---|---|---|---|---|
| **EC1** — Réflexe face à un texte IA fluide | 1 | 2 | 4 | 3 | C = vérification ciblée et efficace (maîtrise active) ; D = scepticisme systématique utile mais potentiellement contre-productif |
| **EC2** — Détection des hallucinations | 1 | 2 | 3 | 4 | Continuum d'expérience et d'intégration |
| **EC3** — Conscience des idéologies des modèles | 1 | 2 | 3 | 4 | Continuum de conscience → observation → transfert dans les choix |
| **EC4** — Likert capacité à enseigner l'esprit critique IA | 1→5 | | | | Score direct |
| **EC5** — Réaction au devoir IA impeccable | 2 | 3 | 2 | 4 | A = acceptation sans questionnement ; C = refus sans levier pédagogique ; B = réflexe de vérification ; D = levier pédagogique explicite |
| **EC6** — Pratiques pour identifier un contenu IA | 1 | 2 | 3 | 4 | Continuum de pratique pédagogique |
| **EC7** — Question ouverte | 0 | 0 | 0 | 0 | Traitement qualitatif uniquement |

---

## 🟠 ENJEU 5 — CYBERSÉCURITÉ

**Score d'enjeu = moyenne de CS1 + CS2 + CS3 + CS4 + CS5 + CS6**
*(CS7 = question ouverte, non scorée)*

| Question | A | B | C | D | Note |
|---|---|---|---|---|---|
| **CS1** — Menace la plus sous-estimée | 2 | 2 | 2 | 2 | Question de posture : avoir une opinion sur la menace principale témoigne d'une conscience de l'enjeu |
| **CS2** — Vérification données collectées | 1 | 2 | 3 | 4 | Continuum de vigilance |
| **CS3** — Likert cybersécurité en classe | 1→5 | | | | Score direct |
| **CS4** — Réaction email phishing direction | 1 | 2 | 4 | 4 | A = vulnérabilité totale ; B = vulnérabilité avec doute non actionné ; C et D = bonne pratique (vérification multicanal) |
| **CS5** — Expliquer deepfake/clonage aux élèves | 1 | 2 | 3 | 4 | Continuum de compétence → transfert pédagogique |
| **CS6** — Connaissance jailbreak / prompt injection | 1 | 2 | 3 | 4 | Continuum de connaissance → implication professionnelle |
| **CS7** — Question ouverte | 0 | 0 | 0 | 0 | Traitement qualitatif uniquement |

---

## 🟣 ENJEU 6 — DÉMOCRATIQUE

**Score d'enjeu = moyenne de D1 + D2 + D3 + D4 + D5 + D6**
*(D7 = question ouverte, non scorée)*

| Question | A | B | C | D | Note |
|---|---|---|---|---|---|
| **D1** — Connaissance du dividende du menteur | 1 | 2 | 3 | 4 | Continuum connaissance → usage pédagogique |
| **D2** — Likert inquiétude désinformation IA | 1→5 | | | | Score direct — l'inquiétude est ici un indicateur de conscience (non d'anxiété) |
| **D3** — Observation bulle informationnelle | 1 | 2 | 3 | 4 | Continuum d'observation → pratique pédagogique outillée |
| **D4** — Préparer les élèves à la manipulation démocratique | 1 | 2 | 3 | 4 | Continuum de pratique pédagogique |
| **D5** — Concentration développement IA | 1 | 2 | 3 | 4 | Continuum de conscience politique de l'enjeu |
| **D6** — Rôle de l'école en citoyenneté numérique | 1 | 2 | 3 | 4 | Continuum d'adhésion à la mission civique de l'école |
| **D7** — Question ouverte | 0 | 0 | 0 | 0 | Traitement qualitatif uniquement |

---

## ⚫ ENJEU 7 — GÉOPOLITIQUE

**Score d'enjeu = moyenne de G1 + G2 + G3 + G4 + G5 + G6**
*(G7 = question ouverte, non scorée)*

| Question | A | B | C | D | Note |
|---|---|---|---|---|---|
| **G1** — Localisation des modèles dominants | 1 | 2 | 3 | 4 | Continuum de conscience → implication professionnelle |
| **G2** — Nature du choix des outils IA | 1 | 1 | 2 | 4 | A et B = absence de conscience politique ; C = conscience partielle ; D = compréhension de la dimension de pouvoir |
| **G3** — Likert influence culturelle des modèles | 1→5 | | | | Score direct |
| **G4** — Données utilisateurs et entraînement des modèles | 1 | 2 | 3 | 4 | Continuum d'indifférence → vigilance → engagement institutionnel |
| **G5** — Approche réglementaire européenne | 1 | 2 | 3 | 4 | Continuum de conscience des enjeux souverains |
| **G6** — Connaissance initiatives souveraines | 1 | 2 | 3 | 4 | Continuum de connaissance → participation |
| **G7** — Question ouverte | 0 | 0 | 0 | 0 | Traitement qualitatif uniquement |

---

## 📊 BOUSSOLE PERSONNELLE

> Les 4 questions de boussole (B1 à B4) sont des réponses ouvertes libres.
> Elles ne sont pas scorées. Elles sont transmises à l'API pour personnaliser la conclusion du rapport.

---

## Calcul du score final par enjeu

```
Score_enjeu = moyenne arithmétique des scores des questions scorées (score ≠ 0)

Enjeu Éthique      = (E1 + E2 + E3 + E4 + E5 + E6) / 6
Enjeu Juridique    = (J1 + J2 + J3 + J4 + J5 + J6) / 6
Enjeu Écologique   = (Éco1 + Éco2 + Éco3 + Éco4 + Éco5 + Éco6) / 6
Enjeu Esprit crit. = (EC1 + EC2 + EC3 + EC4 + EC5 + EC6) / 6
Enjeu Cybersécurité= (CS1 + CS2 + CS3 + CS4 + CS5 + CS6) / 6
Enjeu Démocratique = (D1 + D2 + D3 + D4 + D5 + D6) / 6
Enjeu Géopolitique = (G1 + G2 + G3 + G4 + G5 + G6) / 6
```

### Normalisation pour le radar (0 → 100%)

Les questions Likert ont une échelle 1→5, les autres 1→4.
Pour homogénéiser avant de tracer le radar :

```
Score_normalisé = ((Score_brut - Score_min) / (Score_max - Score_min)) × 100

Pour questions 1→4 : Score_max = 4, Score_min = 1
Pour questions 1→5 : Score_max = 5, Score_min = 1
Score_enjeu_normalisé = moyenne des scores_normalisés des questions de l'enjeu
```

### Seuils d'interprétation (score normalisé)

| Score normalisé | Interprétation | Label dans le rapport |
|---|---|---|
| 0 – 30% | Angle mort | `angle_mort` |
| 31 – 55% | Conscience émergente | `emergent` |
| 56 – 75% | Maîtrise partielle | `partiel` |
| 76 – 100% | Maîtrise active | `actif` |

---

## Identification des profils dominants et angles morts

```
Profils dominants  = les 2 enjeux avec le score normalisé le plus élevé
Angles morts       = les 2 enjeux avec le score normalisé le plus faible
Enjeu central      = Esprit critique (toujours mis en avant — fil conducteur de la formation)
```

> **Note importante** : si l'Esprit critique figure parmi les angles morts,
> le rapport doit le signaler explicitement comme priorité de la formation.

---

## Données transmises à l'API pour la génération du rapport

### Données scorées (anonymisées)
```json
{
  "profil_entree": "experimentateur",
  "contexte_ecole": "emergent",
  "scores": {
    "ethique": 68,
    "juridique": 42,
    "ecologique": 55,
    "esprit_critique": 71,
    "cybersecurite": 38,
    "democratique": 60,
    "geopolitique": 25
  },
  "profils_dominants": ["esprit_critique", "ethique"],
  "angles_morts": ["geopolitique", "cybersecurite"]
}
```

### Données qualitatives (réponses ouvertes — à anonymiser avant envoi)
```json
{
  "reponses_ouvertes": {
    "E7": "...",
    "J7": "...",
    "Eco7": "...",
    "EC7": "...",
    "CS7": "...",
    "D7": "...",
    "G7": "..."
  },
  "boussole": {
    "B1_dominants": "...",
    "B2_angles_morts": "...",
    "B3_attente": "...",
    "B4_question": "..."
  }
}
```

> **Règle RGPD** : aucun nom, prénom, établissement, email ou identifiant
> ne doit figurer dans les données transmises à l'API.
> Les réponses ouvertes doivent être transmises telles quelles,
> sans ajout de métadonnées identifiantes.
```
