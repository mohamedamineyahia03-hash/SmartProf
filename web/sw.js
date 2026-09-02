// Service worker minimal pour SmartProf : rend l'appli installable et
// utilisable hors-ligne pour l'essentiel de l'interface, SANS jamais mettre
// en cache les appels /api/* (une session, une réponse, un corrigé doivent
// toujours venir du serveur — les servir depuis un cache périmé casserait
// la logique de session côté serveur, qui est la source de vérité).
const CACHE_NAME = 'smartprof-shell-v1';
const SHELL_URLS = ['/app', '/manifest.json', '/icons/icon-192.png', '/icons/icon-512.png'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Jamais de cache pour l'API — toujours le serveur, quoi qu'il arrive.
  if (url.pathname.startsWith('/api/')) return;

  if (event.request.mode === 'navigate') {
    // Réseau d'abord (contenu toujours à jour quand la connexion marche),
    // repli sur la coquille en cache si hors-ligne.
    event.respondWith(
      fetch(event.request).catch(() => caches.match('/app'))
    );
    return;
  }

  // Fichiers statiques (icônes, manifest, police...) : cache d'abord.
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
