/* KEMET CODEX — service worker
   Precache the app shell; runtime-cache CDN assets (Three.js, Tailwind,
   fonts) after first use so the installed app works offline. Wikimedia
   images stay network-first (they are decorative and large). */
'use strict';

const VERSION = 'kemet-v4';
const SHELL = [
  './',
  './index.html',
  './packs/giza.js',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(VERSION)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  // Don't cache Wikimedia photos — network only, fail silently.
  if (url.hostname.endsWith('wikimedia.org')) return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        // Cache successful same-origin responses and opaque CDN responses.
        if (res && (res.ok || res.type === 'opaque')){
          const clone = res.clone();
          caches.open(VERSION).then(c => c.put(e.request, clone)).catch(() => {});
        }
        return res;
      }).catch(() => {
        // Offline fallback for navigations.
        if (e.request.mode === 'navigate') return caches.match('./index.html');
        return Response.error();
      });
    })
  );
});
