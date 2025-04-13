self.addEventListener("install", event => {
    console.log("Service Worker Installed");
});

self.addEventListener("activate", event => {
    console.log("Service Worker Activated");
});

self.addEventListener("message", event => {
    if (event.data === "startScreenshot") {
        setInterval(() => {
            self.clients.matchAll().then(clients => {
                clients.forEach(client => client.postMessage("takeScreenshot"));
            });
        }, 5000);
    }
});
