self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('pandora-cloud-cache').then(function (cache) {
            return cache.addAll([
                '/auth/login',
                '/ulp/react-components/1.66.5/css/main.cdn.min.css',
                '/fonts/colfax/ColfaxAIRegular.woff2',
                '/fonts/colfax/ColfaxAIRegular.woff',
                '/fonts/colfax/ColfaxAIRegularItalic.woff2',
                '/fonts/colfax/ColfaxAIRegularItalic.woff',
                '/fonts/colfax/ColfaxAIBold.woff2',
                '/fonts/colfax/ColfaxAIBold.woff',
                '/fonts/colfax/ColfaxAIBoldItalic.woff2',
                '/fonts/colfax/ColfaxAIBoldItalic.woff',
                '/fonts/soehne/soehne-buch.woff2',
                '/fonts/soehne/soehne-halbfett.woff2',
                '/fonts/soehne/soehne-mono-buch.woff2',
                '/fonts/soehne/soehne-mono-halbfett.woff2',
                '/_next/static/css/b389cdeaa663d62e.css',
                '/_next/static/chunks/polyfills-c67a75d1b6f99dc8.js',
                '/_next/static/chunks/webpack-febc072ffb3fcfd3.js',
                '/_next/static/chunks/framework-e23f030857e925d4.js',
                '/_next/static/chunks/main-2f10fecca4c74462.js',
                '/_next/static/chunks/pages/_app-ab949dad0ea9d6e3.js',
                '/_next/static/chunks/2802bd5f-8ff236fd4fe2a08c.js',
                '/_next/static/chunks/bd26816a-981e1ddc27b37cc6.js',
                '/_next/static/chunks/1f110208-cda4026aba1898fb.js',
                '/_next/static/chunks/012ff928-bcfa62e3ac82441c.js',
                '/_next/static/chunks/68a27ff6-a453fd719d5bf767.js',
                '/_next/static/chunks/791-87c69e21acb5fd01.js',
                '/_next/static/chunks/58-f9da11f48bf979b2.js',
                '/_next/static/chunks/734-d34f3efd388e555d.js',
                '/_next/static/chunks/pages/index-a51bd7ac61420e8d.js',
                '/_next/static/chunks/pages/_error-433a1bbdb23dd341.js',
                '/_next/static/35uzIQibpwv56FyPcgmGz/_buildManifest.js',
                '/_next/static/35uzIQibpwv56FyPcgmGz/_ssgManifest.js',
                '/_next/static/chunks/pages/c/[chatId]-2337d8baa604475c.js',
            ]);
        })
    );
});

self.addEventListener('fetch', function (event) {
    event.respondWith(
        caches.match(event.request)
            .then(function (response) {
                    if (response) {
                        return response;
                    }
                    return fetch(event.request);
                }
            )
    );
});
