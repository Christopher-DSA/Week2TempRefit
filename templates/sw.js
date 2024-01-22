self.addEventListener('install', e => { //This event is fired when the service worker is first installed.
  console.log('Install Chris Refit!');
  e.waitUntil( //This promise doesn't allow the service worker to be considerd installed until the promise is resolved.
    caches.open('static').then(cache => {
        return cache.addAll(["https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css","https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js","/OfflineRepairForm"])
    })
  );
}); //service workers only get installed once in their lifecycle.

self.addEventListener("fetch", e => { //This event is fired whenever the browser requests a resource.}
    console.log('Intercepting fetch request for: ' + e.request.url);
    e.respondWith(
        caches.match(e.request).then(response => {
            return response  || fetch(e.request); //If the resource is in the cache, return it, otherwise fetch it from the network.
        })
        .catch(err => {
            console.log(err);
            if (e.request.mode == "navigate") {
                return caches.match("OfflineRepairForm.html");
            }
        })          
    );  
});