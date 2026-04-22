import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import * as historyApiFallbackImport from 'connect-history-api-fallback'

const historyApiFallback =
  (historyApiFallbackImport as any).default ?? (historyApiFallbackImport as any)

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    svelte(),
    {
      name: 'spa-fallback',
      configureServer(server) {
        server.middlewares.use(
          historyApiFallback({
            // réécrit uniquement les routes "propres" vers /index.html
            htmlAcceptHeaders: ['text/html', 'application/xhtml+xml'],
          })
        )
      },
    },
  ],
})
