"""
Técnicas anti-detección avanzadas para evadir Cloudflare
Basado en playwright-stealth y técnicas probadas
"""

def get_stealth_scripts():
    """Retorna todos los scripts anti-detección para inyectar"""

    return """
    // 1. Ocultar webdriver
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });

    // 2. Sobrescribir el objeto chrome
    window.chrome = {
        runtime: {},
        loadTimes: function() {},
        csi: function() {},
        app: {}
    };

    // 3. Permisos
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
    );

    // 4. Plugins
    Object.defineProperty(navigator, 'plugins', {
        get: () => [
            {
                0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
                description: "Portable Document Format",
                filename: "internal-pdf-viewer",
                length: 1,
                name: "Chrome PDF Plugin"
            },
            {
                0: {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: Plugin},
                description: "",
                filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                length: 1,
                name: "Chrome PDF Viewer"
            },
            {
                0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable", enabledPlugin: Plugin},
                1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable", enabledPlugin: Plugin},
                description: "",
                filename: "internal-nacl-plugin",
                length: 2,
                name: "Native Client"
            }
        ]
    });

    // 5. Mimetypes
    Object.defineProperty(navigator, 'mimeTypes', {
        get: () => [
            {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: Plugin},
            {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: Plugin},
            {type: "application/x-nacl", suffixes: "", description: "Native Client Executable", enabledPlugin: Plugin},
            {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable", enabledPlugin: Plugin}
        ]
    });

    // 6. Languages
    Object.defineProperty(navigator, 'languages', {
        get: () => ['es-ES', 'es', 'en-US', 'en']
    });

    // 7. Platform
    Object.defineProperty(navigator, 'platform', {
        get: () => 'Win32'
    });

    // 8. Vendor
    Object.defineProperty(navigator, 'vendor', {
        get: () => 'Google Inc.'
    });

    // 9. Hardware Concurrency
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 8
    });

    // 10. Device Memory
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => 8
    });

    // 11. User Agent Data
    Object.defineProperty(navigator, 'userAgentData', {
        get: () => ({
            brands: [
                { brand: "Not A(Brand", version: "8" },
                { brand: "Chromium", version: "131" },
                { brand: "Google Chrome", version: "131" }
            ],
            mobile: false,
            platform: "Windows"
        })
    });

    // 12. Battery (falso para parecer desktop)
    if ('getBattery' in navigator) {
        navigator.getBattery = () => Promise.resolve({
            charging: true,
            chargingTime: 0,
            dischargingTime: Infinity,
            level: 1,
            addEventListener: () => {},
            removeEventListener: () => {},
            dispatchEvent: () => true
        });
    }

    // 13. Connection
    Object.defineProperty(navigator, 'connection', {
        get: () => ({
            effectiveType: '4g',
            rtt: 50,
            downlink: 10,
            saveData: false
        })
    });

    // 14. Screen
    Object.defineProperty(screen, 'width', { get: () => 1920 });
    Object.defineProperty(screen, 'height', { get: () => 1080 });
    Object.defineProperty(screen, 'availWidth', { get: () => 1920 });
    Object.defineProperty(screen, 'availHeight', { get: () => 1040 });
    Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
    Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });

    // 15. Date para evitar headless detection
    const originalDate = Date;
    Date = class extends originalDate {
        constructor(...args) {
            if (args.length === 0) {
                super();
            } else {
                super(...args);
            }
        }
        getTimezoneOffset() {
            return -60; // Madrid timezone
        }
    };

    // 16. Canvas fingerprint randomization
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(type) {
        if (type === 'image/png' && this.width === 280 && this.height === 60) {
            return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUg==';
        }
        return originalToDataURL.apply(this, arguments);
    };

    // 17. WebGL Vendor
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) {
            return 'Intel Inc.';
        }
        if (parameter === 37446) {
            return 'Intel Iris OpenGL Engine';
        }
        return getParameter.apply(this, arguments);
    };

    // 18. Eliminar _Selenium_IDE_Recorder, _phantom, callPhantom, etc.
    delete window._Selenium_IDE_Recorder;
    delete window._phantom;
    delete window.callPhantom;
    delete window._selenium;
    delete window.__selenium_unwrapped;
    delete window.__selenium_evaluate;
    delete window.__selenium_script_fn;
    delete window.__driver_evaluate;
    delete window.__webdriver_evaluate;
    delete window.__driver_unwrapped;
    delete window.__webdriver_unwrapped;
    delete window.__fxdriver_evaluate;
    delete window.__fxdriver_unwrapped;
    delete window.__webdriver_script_fn;
    delete window.__webdriver_script_func;
    delete window.__webdriver_script_function;
    delete window.$cdc_asdjflasutopfhvcZLmcfl_;
    delete window.$chrome_asyncScriptInfo;

    // 19. Notification permissions
    const originalPermissions = navigator.permissions;
    if (originalPermissions) {
        navigator.permissions.query = (parameters) => {
            if (parameters.name === 'notifications') {
                return Promise.resolve({ state: 'default' });
            }
            return originalPermissions.query(parameters);
        };
    }

    // 20. Console.debug para parecer normal
    console.debug('Chrome initialized');

    // 21. Iframe detection evasion
    Object.defineProperty(window, 'length', {
        get: () => 0
    });
    """

def get_browser_args():
    """Retorna argumentos del navegador para evitar detección"""
    return [
        '--disable-blink-features=AutomationControlled',
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials',
        '--disable-features=BlockInsecurePrivateNetworkRequests',
        # Evitar detección de headless
        '--window-size=1920,1080',
        '--start-maximized',
        '--disable-blink-features=AutomationControlled',
        # Fingir plugins y extensiones
        '--load-extension=' if False else '',  # Placeholder
        '--disable-extensions-except=' if False else '',
        # User agent
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        # GPU
        '--use-gl=swiftshader',
        '--use-angle=swiftshader',
        # Audio
        '--mute-audio',
        # Timezone
        '--lang=es-ES',
    ]

def get_context_options():
    """Retorna opciones del contexto para parecer más real"""
    return {
        'viewport': {'width': 1920, 'height': 1080},
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'locale': 'es-ES',
        'timezone_id': 'Europe/Madrid',
        'permissions': ['geolocation', 'notifications'],
        'color_scheme': 'light',
        'device_scale_factor': 1,
        'is_mobile': False,
        'has_touch': False,
        'accept_downloads': True,
        'extra_http_headers': {
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
    }
