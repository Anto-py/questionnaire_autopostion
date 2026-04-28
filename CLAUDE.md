# CLAUDE.md
## Questionnaire d'autopositionnement IA — Spécifications techniques complètes
**Projet** : « Quel utilisateur d'IA es-tu ? »
**Formation** : L'intelligence artificielle en éducation : cultiver un regard critique, éthique et sécurisé
**FWB — Enseignement secondaire**

---

## 1. VUE D'ENSEMBLE

### Ce que tu dois produire
Un fichier HTML unique, autonome, sans dépendance externe, qui :
1. Affiche le questionnaire d'autopositionnement (49 questions + mise en route + boussole)
2. Calcule les scores par enjeu selon le barème défini
3. Génère un rapport individuel via l'API Anthropic
4. Envoie les scores anonymisés à un webhook n8n pour agrégation de groupe
5. Affiche le rapport individuel en markdown rendu dans l'interface

### Fichiers de référence obligatoires
Lire ces trois documents avant de coder :
- `questionnaire_autopositionnement_IA_v2.md` — contenu exact des questions et options
- `bareme_scoring_questionnaire_IA.md` — logique de scoring question par question
- `prompt_systeme_rapport_IA.md` — prompts système pour l'API Anthropic

---

## 2. ARCHITECTURE TECHNIQUE

### Fichier unique
- **Un seul fichier** `.html` — HTML + CSS + JS inline
- Aucune dépendance externe (pas de CDN, pas de framework, pas de bibliothèque)
- Exception unique autorisée : Google Fonts via `<link>` si disponible, sinon system fonts
- Taille cible : < 200 Ko

### Structure du fichier
```
index.html
├── <head>         — meta, CSS complet inline
└── <body>
    ├── ÉCRAN 0    — Consentement RGPD
    ├── ÉCRAN 1    — Mise en route (M1, M2)
    ├── ÉCRANS 2–8 — Un écran par enjeu (7 enjeux × 7 questions)
    ├── ÉCRAN 9    — Boussole personnelle (B1–B4)
    ├── ÉCRAN 10   — Génération du rapport (loader + appel API)
    └── ÉCRAN 11   — Affichage du rapport individuel
```

### Navigation
- Questionnaire paginé : **un enjeu = un écran**
- Barre de progression visible en permanence (8 étapes hors consentement)
- Bouton « Suivant » activé uniquement quand toutes les questions scorées de l'écran ont une réponse
- Les questions ouvertes sont optionnelles (jamais bloquantes)
- Pas de bouton « Précédent » — le questionnaire est à sens unique (cohérence des réponses spontanées)

### Stockage des données
- **Uniquement dans la mémoire JavaScript** (objet `state` en mémoire)
- Aucun `localStorage`, `sessionStorage` ou `cookie`
- Les données disparaissent à la fermeture du navigateur — c'est voulu

---

## 3. LOGIQUE DE SCORING

### Objet `state` principal
```javascript
const state = {
  // Contexte
  profil_entree: null,      // 'debutant' | 'observateur' | 'experimentateur' | 'integrateur'
  contexte_ecole: null,     // 'absent' | 'evite' | 'emergent' | 'present'

  // Réponses brutes (clé = id question, valeur = lettre choisie A/B/C/D ou chiffre Likert)
  reponses: {},

  // Scores calculés par enjeu (0–100 normalisés)
  scores: {
    ethique: null,
    juridique: null,
    ecologique: null,
    esprit_critique: null,
    cybersecurite: null,
    democratique: null,
    geopolitique: null
  },

  // Profils calculés
  profils_dominants: [],    // 2 enjeux avec score le plus élevé
  angles_morts: [],         // 2 enjeux avec score le plus faible

  // Réponses ouvertes (texte brut)
  reponses_ouvertes: {
    E7: '', J7: '', Eco7: '', EC7: '', CS7: '', D7: '', G7: ''
  },

  // Boussole
  boussole: {
    B1_dominants: '', B2_angles_morts: '', B3_attente: '', B4_question: ''
  }
};
```

### Barème — Référence impérative
Appliquer **exactement** le barème défini dans `bareme_scoring_questionnaire_IA.md`.

Points critiques à implémenter avec attention particulière (logique non linéaire) :
- **EC1** : C=4, D=3 (ordre inversé)
- **CS4** : C=4 ET D=4 (deux bonnes réponses)
- **J6** : A=1, B=2, C=3, D=1 (D n'est pas la meilleure réponse)
- **J3** : A=4, B=2, C=2, D=1 (ordre inversé)
- **E4, CS1** : toutes les réponses = 2 (questions de posture)
- **E2** : A=1, B=3, C=3, D=3

### Calcul du score d'enjeu
```javascript
function calculerScoreEnjeu(questions) {
  // 1. Récupérer le score brut de chaque question scorée (score ≠ 0)
  // 2. Pour les Likert (1→5) : conserver la valeur brute
  // 3. Pour les autres (1→4) : conserver la valeur brute
  // 4. Normaliser chaque score : ((brut - min) / (max - min)) × 100
  //    → min=1, max=4 pour questions à choix
  //    → min=1, max=5 pour Likert
  // 5. Calculer la moyenne des scores normalisés
  // 6. Retourner un entier arrondi (0–100)
}
```

### Identification des profils
```javascript
function calculerProfils(scores) {
  const enjeux = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  return {
    profils_dominants: [enjeux[0][0], enjeux[1][0]],
    angles_morts: [enjeux[enjeux.length-1][0], enjeux[enjeux.length-2][0]]
  };
}
```

### Mapping M1 → profil_entree
```javascript
const mappingM1 = { A: 'debutant', B: 'observateur', C: 'experimentateur', D: 'integrateur' };
const mappingM2 = { A: 'absent', B: 'evite', C: 'emergent', D: 'present' };
```

---

## 4. INTÉGRATION API ANTHROPIC

### Appel API — Rapport individuel
```javascript
async function genererRapportIndividuel() {
  const payload = {
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1200,
    system: PROMPT_SYSTEME_INDIVIDUEL,  // contenu exact du prompt système (voir fichier de référence)
    messages: [{
      role: 'user',
      content: JSON.stringify({
        profil_entree: state.profil_entree,
        contexte_ecole: state.contexte_ecole,
        scores: state.scores,
        profils_dominants: state.profils_dominants,
        angles_morts: state.angles_morts,
        reponses_ouvertes: state.reponses_ouvertes,
        boussole: state.boussole
      })
    }]
  };

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  return data.content[0].text;
}
```

### Rendu du rapport
- Le texte markdown retourné par l'API est rendu en HTML avec un **parseur markdown minimal** codé en JS pur (pas de bibliothèque)
- Éléments à supporter : `##`, `###`, `**bold**`, `*italic*`, listes `-`, paragraphes
- Le rapport s'affiche dans une carte scrollable sur l'écran 11

### Gestion des erreurs API
```javascript
// Afficher un message d'erreur clair à l'utilisateur
// Proposer un bouton "Réessayer"
// Ne jamais afficher le détail technique de l'erreur à l'utilisateur
```

---

## 5. INTÉGRATION WEBHOOK N8N

### Endpoint
```
POST https://n8n.pedagokit.be/webhook/questionnaire-ia-autopositionnement
```

### Payload envoyé (anonymisé — aucune donnée personnelle)
```javascript
async function envoyerScoresGroupe() {
  const payload = {
    timestamp: new Date().toISOString(),
    session_id: genererSessionId(),  // UUID aléatoire généré côté client, sans lien avec l'identité
    profil_entree: state.profil_entree,
    contexte_ecole: state.contexte_ecole,
    scores: state.scores,
    profils_dominants: state.profils_dominants,
    angles_morts: state.angles_morts
    // ⚠️ Les réponses ouvertes et la boussole NE sont PAS envoyées au webhook
  };

  await fetch('https://n8n.pedagokit.be/webhook/questionnaire-ia-autopositionnement', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
}
```

### Générateur de session_id
```javascript
function genererSessionId() {
  return 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
}
```

### Timing d'envoi
- L'envoi au webhook se fait **en parallèle** de l'appel API Anthropic (pas en séquence)
- Une erreur webhook n'interrompt pas la génération du rapport individuel
- L'envoi est silencieux — l'utilisateur n'en est pas informé dans l'interface (mais c'est mentionné dans le consentement RGPD)

---

## 6. ÉCRAN 0 — CONSENTEMENT RGPD

### Contenu obligatoire (texte exact à afficher)
```
INFORMATION SUR L'USAGE DE VOS DONNÉES

Ce questionnaire traite vos réponses de la façon suivante :

• Vos réponses restent dans votre navigateur. Elles ne sont jamais stockées sur un serveur.
• Vos scores anonymisés (sans nom, sans établissement) sont transmis à un serveur de formation 
  hébergé en Belgique (n8n.pedagokit.be) pour permettre la génération d'un rapport collectif.
• Votre rapport individuel est généré via l'API Anthropic (serveurs américains). 
  Vos réponses ouvertes y sont transmises sans aucun élément d'identification.
• Aucune donnée personnelle (nom, email, établissement) n'est collectée ou transmise.
• Les scores agrégés sont conservés le temps de la formation puis supprimés.

Responsable du traitement : [NOM FORMATEUR / ORGANISME]
Contact : [EMAIL CONTACT]

En cliquant sur "Je commence le questionnaire", vous acceptez ce traitement.
```

### Comportement
- Le bouton "Je commence" est inactif tant que la case à cocher n'est pas cochée
- Case à cocher : `☐ J'ai lu et j'accepte les conditions d'utilisation de mes données`
- Aucun accès au questionnaire sans consentement explicite

---

## 7. DESIGN RETROFUTURISTE

### Identité visuelle — Charte obligatoire

#### Palette CSS (variables à déclarer dans `:root`)
```css
:root {
  --retro-teal:   #127676;
  --retro-orange: #E4632E;
  --retro-jaune:  #E3A535;
  --retro-ink:    #0D1617;
  --retro-paper:  #F2EFE6;
}
```

#### Ratio 60-30-10
- **60% paper** (`#F2EFE6`) — fond général, zones de contenu
- **30% teal** (`#127676`) — titres, bordures, barre de progression, header
- **10% orange + jaune** (`#E4632E` + `#E3A535`) — boutons CTA, feedback, accents

#### Typographie
```css
/* Titres — géométrique majuscule */
.titre {
  font-family: Impact, 'Arial Black', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--retro-teal);
}

/* Corps — system sans-serif */
body {
  font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
  color: var(--retro-ink);
}
```

#### Page-frame Art Nouveau (règle obligatoire)
```css
body {
  background: var(--retro-ink);
  margin: 0;
  padding: 16px;
  min-height: 100vh;
}

.page-frame {
  background: var(--retro-paper);
  border: 4px solid var(--retro-orange);
  border-radius: 32px 8px 24px 12px; /* ASYMÉTRIQUE — jamais 4 coins identiques */
  position: relative;
  min-height: calc(100vh - 32px);
  padding: 40px;
  max-width: 860px;
  margin: 0 auto;
}
```

### Composants UI spécifiques

#### Bouton principal (pill)
```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  border: 3px solid var(--retro-teal);
  border-radius: 50px;
  overflow: hidden;
  cursor: pointer;
  font-family: Impact, 'Arial Black', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.btn-primary .btn-label {
  background: var(--retro-jaune);
  color: var(--retro-ink);
  padding: 12px 20px;
  font-size: 14px;
}
.btn-primary .btn-icon {
  background: var(--retro-orange);
  color: var(--retro-paper);
  padding: 12px 16px;
  font-size: 18px;
}
```

#### Cartes de question
```css
.carte-question {
  background: var(--retro-paper);
  border: 3px solid var(--retro-teal);
  border-radius: 24px 8px 24px 8px; /* Asymétrique */
  box-shadow: inset 0 0 0 1px rgba(228, 99, 46, 0.15);
  padding: 28px 32px;
  margin-bottom: 20px;
}
```

#### Options de réponse (radio/checkbox)
```css
.option {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 18px;
  border: 2px solid transparent;
  border-radius: 12px 4px 12px 4px; /* Asymétrique */
  cursor: pointer;
  transition: all 0.2s ease;
}
.option:hover {
  border-color: var(--retro-jaune);
  background: rgba(227, 165, 53, 0.08);
}
.option.selected {
  border-color: var(--retro-teal);
  background: rgba(18, 118, 118, 0.08);
}
.option-lettre {
  min-width: 28px;
  height: 28px;
  background: var(--retro-teal);
  color: var(--retro-paper);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Impact, sans-serif;
  font-size: 13px;
  flex-shrink: 0;
}
.option.selected .option-lettre {
  background: var(--retro-orange);
}
```

#### Barre de progression
```css
.progress-bar-container {
  height: 6px;
  background: rgba(18, 118, 118, 0.15);
  border-radius: 3px;
  margin-bottom: 32px;
}
.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--retro-teal), var(--retro-orange));
  border-radius: 3px;
  transition: width 0.4s ease;
}
```

#### Échelle Likert
```css
.likert-container {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding: 16px 0;
}
.likert-option {
  width: 48px;
  height: 48px;
  border: 3px solid var(--retro-teal);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: Impact, sans-serif;
  font-size: 18px;
  cursor: pointer;
  color: var(--retro-teal);
  transition: all 0.2s;
}
.likert-option:hover {
  background: var(--retro-jaune);
  border-color: var(--retro-jaune);
  color: var(--retro-ink);
}
.likert-option.selected {
  background: var(--retro-teal);
  color: var(--retro-paper);
}
```

#### Séparateurs Art Nouveau
```css
.separateur {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 24px 0;
  color: var(--retro-teal);
  font-size: 20px;
}
.separateur::before,
.separateur::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--retro-teal), transparent);
}
/* Ornements : ❧ ✿ ❀ ⚘ — à alterner selon les sections */
```

#### Header de section (par enjeu)
```css
.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--retro-teal);
}
.section-emoji {
  font-size: 32px;
  flex-shrink: 0;
}
.section-titre {
  font-family: Impact, 'Arial Black', sans-serif;
  font-size: 22px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--retro-teal);
  margin: 0;
}
.section-sous-titre {
  font-size: 13px;
  color: rgba(13, 22, 23, 0.6);
  margin: 4px 0 0;
  font-style: italic;
}
```

#### Loader (pendant génération du rapport)
```css
/* Animation orbes concentriques teal/orange */
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  padding: 60px 0;
}
.loader-orbe {
  width: 64px;
  height: 64px;
  border: 4px solid var(--retro-teal);
  border-top-color: var(--retro-orange);
  border-radius: 50%;
  animation: rotation 1s linear infinite;
}
@keyframes rotation {
  to { transform: rotate(360deg); }
}
.loader-texte {
  font-family: Impact, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--retro-teal);
  font-size: 14px;
}
```

#### Radar chart (résultats)
- Tracer le radar en **SVG pur** (pas de bibliothèque)
- 7 axes — un par enjeu
- Couleur de remplissage : `rgba(18, 118, 118, 0.25)` (teal transparent)
- Bordure du polygone : `var(--retro-teal)` 2px
- Points aux sommets : cercles `var(--retro-orange)` 6px de rayon
- Fond du radar : toile d'araignée en `rgba(18, 118, 118, 0.1)` (5 niveaux)
- Labels : font-family Impact, uppercase, teal

#### Rapport individuel (rendu markdown)
```css
.rapport-container {
  background: var(--retro-ink);
  color: var(--retro-paper);
  border-radius: 24px 8px 24px 8px;
  padding: 36px 40px;
  border: 2px solid var(--retro-orange);
}
.rapport-container h2 {
  font-family: Impact, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--retro-jaune);
  font-size: 18px;
  margin-top: 28px;
  border-bottom: 1px solid rgba(227, 165, 53, 0.3);
  padding-bottom: 8px;
}
.rapport-container h3 {
  color: var(--retro-teal);
  font-family: Impact, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 15px;
}
.rapport-container p {
  line-height: 1.7;
  color: rgba(242, 239, 230, 0.9);
}
.rapport-container strong {
  color: var(--retro-jaune);
}
```

### Animations globales
```css
/* Apparition des écrans */
.ecran {
  animation: fadeSlideIn 0.35s ease both;
}
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Hover général sur éléments interactifs */
* { transition: border-color 0.2s, background-color 0.2s, color 0.2s; }
```

---

## 8. STRUCTURE DES ÉCRANS — DÉTAIL

### Écran 0 — Consentement
- Logo / titre de la formation en grand (Impact, teal)
- Sous-titre retrofuturiste : « ANALYSEZ VOTRE RAPPORT À L'IA »
- Bloc d'information RGPD (texte exact défini en section 6)
- Case à cocher + bouton "Je commence le questionnaire"
- Ornements Art Nouveau aux coins (SVG inline teal)

### Écrans 1–8 — Questions
Structure identique pour chaque écran :
```
[Barre de progression]
[Header de section : emoji + titre enjeu + sous-titre]
[Séparateur Art Nouveau]
[Pour chaque question de l'enjeu :]
  [Numéro + texte de la question]
  [Options A/B/C/D OU Likert OU textarea]
[Séparateur Art Nouveau]
[Bouton "Suivant →"]
```

### Écran 9 — Boussole personnelle
- 4 textareas (B1 à B4) avec les questions exactes du questionnaire
- Tous optionnels — le bouton "Générer mon rapport" est toujours actif
- Message d'encouragement : « Ces réponses enrichissent votre rapport — prenez le temps d'y réfléchir. »

### Écran 10 — Génération
- Loader animation
- Message : « ANALYSE EN COURS... » puis messages rotatifs :
  - « Cartographie de vos profils dominants... »
  - « Identification de vos angles morts... »
  - « Rédaction de votre rapport personnalisé... »
- Lancer en parallèle : `genererRapportIndividuel()` + `envoyerScoresGroupe()`

### Écran 11 — Rapport individuel
Disposition en deux colonnes (desktop) / empilées (mobile) :

**Colonne gauche — Radar + scores**
- Radar SVG 7 axes
- Liste des scores par enjeu (barre de progression horizontale par enjeu)
- Badge "Profils dominants" (teal) + Badge "Angles morts" (orange)

**Colonne droite — Rapport texte**
- Rapport markdown rendu
- Bouton "Imprimer / Sauvegarder en PDF" (déclenche `window.print()`)
- Bouton "Recommencer" (recharge la page)

---

## 9. RESPONSIVE

```css
/* Desktop : max-width 860px centré */
/* Tablette (< 768px) : padding réduit, colonnes empilées */
/* Mobile (< 480px) : font-size réduits, options en pleine largeur */

@media (max-width: 768px) {
  .page-frame { padding: 20px 16px; }
  .rapport-columns { flex-direction: column; }
  .likert-option { width: 40px; height: 40px; font-size: 16px; }
}
```

---

## 10. CHECKLIST AVANT LIVRAISON

### Fonctionnel
- [ ] Toutes les 49 questions sont présentes avec le texte exact du questionnaire v2
- [ ] Le barème est appliqué correctement, y compris les 5 cas non linéaires (EC1, CS4, J6, J3, E4/CS1)
- [ ] Les questions Likert sont normalisées correctement (1→5 vers 0→100%)
- [ ] Le calcul des profils dominants et angles morts est correct
- [ ] L'appel API Anthropic fonctionne et le rapport s'affiche
- [ ] L'envoi au webhook n8n fonctionne en parallèle
- [ ] Une erreur API ou webhook n'empêche pas l'affichage du rapport
- [ ] Le consentement RGPD bloque l'accès au questionnaire si non coché
- [ ] Aucune donnée personnelle n'est envoyée à l'API ou au webhook

### Design
- [ ] Palette teal/orange/jaune/ink/paper respectée
- [ ] Ratio 60-30-10 respecté
- [ ] Page-frame avec border-radius asymétrique
- [ ] Page-frame ne touche pas les bords du viewport (padding body : 16px)
- [ ] Fond extérieur en `--retro-ink`
- [ ] Titres en Impact majuscules espacées
- [ ] Boutons pill avec section jaune + cercle orange
- [ ] Radar SVG 7 axes fonctionnel
- [ ] Animations fadeSlideIn sur chaque changement d'écran
- [ ] Séparateurs Art Nouveau entre les sections

### Accessibilité
- [ ] Contraste texte/fond ≥ 4.5:1 sur toutes les combinaisons
- [ ] Navigation au clavier possible (tabindex, focus visible)
- [ ] Labels explicites sur tous les inputs
- [ ] `lang="fr"` sur la balise `<html>`

---

## 11. VARIABLES DE CONFIGURATION

Regrouper en tête de script pour faciliter la maintenance :

```javascript
const CONFIG = {
  WEBHOOK_URL: 'https://n8n.pedagokit.be/webhook/questionnaire-ia-autopositionnement',
  API_MODEL: 'claude-sonnet-4-20250514',
  API_MAX_TOKENS: 1200,
  NOM_FORMATEUR: '[À COMPLÉTER]',
  EMAIL_CONTACT: '[À COMPLÉTER]',
  VERSION: '2.0',
  DATE: '2025'
};
```

---

## 12. PROMPT SYSTÈME — RÉFÉRENCE DIRECTE

Le prompt système complet est défini dans `prompt_systeme_rapport_IA.md`.
Le copier intégralement dans une constante JS :

```javascript
const PROMPT_SYSTEME_INDIVIDUEL = `[Coller ici le contenu exact du bloc système du fichier prompt_systeme_rapport_IA.md]`;
```

Ne pas le résumer, ne pas le reformuler — le copier mot pour mot.
```
