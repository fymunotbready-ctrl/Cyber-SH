import type { CapacitorConfig } from "@capacitor/cli"

// Points Capacitor at the static export Next.js already produces
// (next.config.mjs has output: 'export' → frontend/out).
// The native app shell loads these files locally; all /api and /auth
// calls still go out over the network to NEXT_PUBLIC_CYBERSH_API,
// same as the web version.
const config: CapacitorConfig = {
  appId: "com.cybersh.app",
  appName: "Cyber SH",
  webDir: "out",
  server: {
    // Only used if you want LIVE-RELOAD against a dev server while
    // building — leave commented out for production app store builds,
    // since then Capacitor serves the bundled `out/` files locally.
    // url: "http://192.168.1.50:3000",
    // cleartext: true,
    androidScheme: "https",
  },
}

export default config
