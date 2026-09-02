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

## Build de test — fait et vérifié

L'outillage a fini par être installé (voir plus bas les vrais pièges
rencontrés) et un premier `.apk` de debug a réellement été compilé :

```
mobile/android/app/build/outputs/apk/debug/app-debug.apk   (5,4 Mo)
```

Il n'est **pas encore utile tel quel** : `capacitor.config.json` pointe vers
`https://app.smartprof.tn`, un nom de domaine qui n'existe pas encore (rien
n'est déployé) — l'app s'ouvrirait sur une erreur réseau. Utile uniquement
pour prouver que la chaîne de compilation fonctionne de bout en bout.

Outillage installé localement (`C:\Users\NITRO\dev-tools\`), pas dans le
dépôt :
- **JDK 21** (Eclipse Temurin) — **pas JDK 17**. Le premier essai avec 17 a
  échoué (`error: invalid source release: 21`) : ce projet Capacitor exige
  Java 21 pour compiler, une contrainte qui n'est pas documentée nulle part
  dans les fichiers Capacitor eux-mêmes, seulement découverte à l'exécution.
- **Android SDK command-line tools**, `platform-tools`, `platforms;android-36`,
  `build-tools;36.0.0` (`build-tools;35.0.0` aussi installé automatiquement
  par Gradle en cours de route).
- **Piège rencontré et résolu** : `sdkmanager` échouait au tout début
  (`Failed to download any source lists!`) — un antivirus (Avast, "Web/Mail
  Shield") intercepte le HTTPS pour scanner le trafic avec son propre
  certificat, que Java ne connaît pas par défaut (contrairement à Windows).
  Corrigé en importons ce certificat dans le magasin de confiance de
  **chaque** JDK installé (`keytool -importcert ... -keystore
  <JAVA_HOME>\lib\security\cacerts`) — à refaire si un JDK est réinstallé.

### Pour recompiler après un changement (nouvelle machine ou après avoir mis à jour l'app)

```bash
cd mobile
npx cap sync android
```

Puis soit :
- **Ouvrir dans Android Studio** (`npx cap open android`) et cliquer sur
  Build → Build Bundle(s)/APK(s) → Build APK(s) — le plus simple.
- **Ou en ligne de commande**, depuis `mobile/android/` (avec `JAVA_HOME`
  pointant vers un JDK 21, et le SDK Android sur le `PATH`) :
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
