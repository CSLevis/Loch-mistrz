// Basic Service Worker to enable PWA installability
const CACHE_NAME = 'rpg-lochmistrz-v1';
const urlsToCache = [
    '/',
    '/static/style.css',
    '/static/style2.css',
    '/static/character_cards.css',
    '/static/tmanager.css',
    '/static/main.js',
    '/static/d20a.png'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Cache hit - return response
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});
