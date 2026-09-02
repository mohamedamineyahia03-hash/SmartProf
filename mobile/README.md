# SmartProf — application mobile Android (chemin 100% gratuit)

Ce dossier enveloppe l'application web SmartProf déjà en ligne dans une vraie
application Android installable, via [Capacitor](https://capacitorjs.com).
L'app ne recharge pas une copie du site : `capacitor.config.json` pointe
`server.url` vers le vrai serveur SmartProf, donc elle affiche toujours la
version à jour, avec les mêmes comptes/sessions que sur le web.

## Déjà préparé ici

- `capacitor.config.json` — config Capacitor (id `com.smartprof.app`)
- `android/` — projet Android natif généré (Gradle, manifest...)
- `resources/` — icône source (1024×1024), icône adaptative (premier plan +
  fond séparés, exigés par Android 8+), écran de démarrage
- Icônes/splash générés dans `android/` pour toutes les densités d'écran

## Ce qu'il reste à faire sur votre machine

Rien ici ne peut compiler un vrai `.apk` sans deux outils qui ne sont pas
installés sur cette machine :

1. **Java (JDK 17)** — nécessaire pour Gradle, le système de build Android.
2. **Android SDK** — soit via [Android Studio](https://developer.android.com/studio)
   (le plus simple : l'IDE installe le SDK automatiquement), soit juste les
   [command-line tools](https://developer.android.com/studio#command-tools)
   si vous préférez tout faire en ligne de commande (plus léger, ~1 Go au
   lieu de ~5-8 Go pour Android Studio complet).

Je n'ai pas lancé cette installation moi-même : c'est plusieurs Go de
téléchargement et une modification durable de votre machine — mieux vaut que
vous choisissiez vous-même l'emplacement et la méthode (Android Studio ou
CLI seule).

### Une fois Java + le SDK installés

```bash
cd mobile
npx cap sync android
```

Puis soit :
- **Ouvrir dans Android Studio** (`npx cap open android`) et cliquer sur
  Build → Build Bundle(s)/APK(s) → Build APK(s) — le plus simple.
- **Ou en ligne de commande**, depuis `mobile/android/` :
  ```bash
  ./gradlew assembleDebug     # test rapide, non signé
  ./gradlew bundleRelease     # version publiable, à signer ensuite
  ```

### Avant de publier pour de vrai

1. **Mettre à jour `capacitor.config.json`** — `server.url` pointe
   actuellement vers `https://app.smartprof.tn` (placeholder). À remplacer
   par la vraie adresse dès que l'app est en ligne, puis relancer
   `npx cap sync android`.
2. **Signer l'APK** — générer une clé une seule fois :
   ```bash
   keytool -genkeypair -v -keystore smartprof-release.keystore -alias smartprof -keyalg RSA -keysize 2048 -validity 10000
   ```
   Gardez ce fichier `.keystore` et son mot de passe en lieu sûr — le
   reperdre empêche de mettre à jour l'app plus tard, il faudrait tout
   republier sous une nouvelle identité.
3. **Politique de confidentialité** — une URL publique est exigée par tous
   les stores, même gratuits. Base : la mention légale déjà présente en bas
   de la page vitrine — à étoffer en page dédiée (`/confidentialite` par
   exemple) avant soumission.

## Distribution gratuite (le chemin retenu)

| Où | Coût | Étapes |
|---|---|---|
| **Téléchargement direct** | 0 € | Héberger le `.apk` signé sur le site (ou GitHub Releases) avec un bouton "Télécharger" sur la vitrine. Android affichera un avertissement "source inconnue" au premier lancement — normal, pas bloquant. |
| **Samsung Galaxy Store** | 0 € | Compte sur [Samsung Developers](https://developer.samsung.com/), soumission via Samsung Galaxy Store Seller Portal. |
| **Huawei AppGallery** | 0 € | Compte sur [AppGallery Connect](https://developer.huawei.com/consumer/en/appgallery/), soumission du même APK/AAB. |

Les trois utilisent le **même fichier** — pas de travail à refaire par
plateforme, seulement une fiche (description, captures d'écran) par store.

## iOS

Pas de chemin gratuit équivalent (voir échange précédent) — le PWA déjà en
place (`/app`, "Ajouter à l'écran d'accueil" depuis Safari) reste la seule
option gratuite sur iPhone.
