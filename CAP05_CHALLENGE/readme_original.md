## Descripción del Proyecto

InternetWhisper es un chatbot conversacional de inteligencia artificial generativa con acceso a Internet. Utiliza una base de datos vectorial Redis para cachear información previamente recuperada, reduciendo la necesidad de repetir búsquedas. El sistema consulta la API de búsqueda de Google y utiliza modelos de lenguaje de OpenAI para generar respuestas contextuales y precisas.

---

## Arquitectura y Tecnologías

### Componentes principales

- **Frontend**: Interfaz de usuario basada en Streamlit (src/frontend/main.py), que permite la interacción en tiempo real con el chatbot.
- **Orchestrator**: API principal construida con FastAPI (src/orchestrator/main.py), que coordina la búsqueda, recuperación, procesamiento y generación de respuestas.
- **Scraper**: Servicio de scraping web (src/scraper/main.py), capaz de obtener contenido HTML de páginas web, incluso aquellas que requieren renderizado JavaScript.
- **Cache**: Redis Stack como base de datos vectorial para almacenamiento y recuperación eficiente de contexto relevante.

### Tecnologías utilizadas

- **FastAPI**: Framework para la API principal.
- **Streamlit**: Interfaz web interactiva.
- **OpenAI API**: Generación de respuestas y embeddings.
- **Google Custom Search API**: Búsqueda de información en la web.
- **Redis Stack**: Almacenamiento de vectores y caché.
- **LangChain**: División y manejo de textos largos.
- **Playwright & aiohttp**: Scraping web avanzado.
- **Docker & Docker Compose**: Contenerización y orquestación de servicios.

---

## Variables de Entorno

Copia el archivo .env.example a `.env` y completa los valores necesarios:

```env
HEADER_ACCEPT_ENCODING="gzip"
HEADER_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."
GOOGLE_API_HOST="https://www.googleapis.com/customsearch/v1?"
GOOGLE_FIELDS="items(title, displayLink, link, snippet,pagemap/cse_thumbnail)"
GOOGLE_API_KEY=TU_API_KEY_DE_GOOGLE
GOOGLE_CX=TU_CX_DE_GOOGLE
OPENAI_API_KEY=TU_API_KEY_DE_OPENAI
```

- **GOOGLE_API_KEY**: Obténla en [Google Custom Search](https://developers.google.com/custom-search/v1/overview).
- **GOOGLE_CX**: ID de tu motor de búsqueda personalizado.
- **OPENAI_API_KEY**: Consíguela en [OpenAI](https://openai.com/blog/openai-api).

---

## Instalación y Ejecución Local

1. **Clona el repositorio y navega al directorio del proyecto:**

   ```sh
   git clone <repo-url>
   cd project
   ```

2. **Configura las variables de entorno:**

   ```sh
   cp .env.example .env
   # Edita .env y agrega tus claves
   ```

3. **Construye y ejecuta los servicios con Docker Compose:**

   ```sh
   docker-compose build
   docker-compose up
   ```

4. **Accede a la aplicación:**

   - Interfaz web: [http://localhost:8501/](http://localhost:8501/)
   - API principal: [http://localhost:8000/](http://localhost:8000/)

---

## Cambiar el Scraper o Embeddings

- Por defecto, se usa `ScraperLocal` (scraping con aiohttp).
- Para scraping avanzado (JavaScript), usa `ScraperRemote` y habilita el servicio correspondiente en docker-compose.yml.
- Para embeddings, puedes alternar entre `OpenAIEmbeddings` y `RemoteEmbeddings` en `main.py`.

---

## Endpoints y OpenAPI

La API principal expone el endpoint `/streamingSearch`:

- **GET /streamingSearch?query=...**
  - Devuelve eventos SSE con los resultados de búsqueda, contexto y tokens generados.

Puedes ver la documentación OpenAPI accediendo a [http://localhost:8000/docs](http://localhost:8000/docs) cuando el servicio esté corriendo.

**Ejemplo de definición OpenAPI:**
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/streamingSearch": {
      "get": {
        "summary": "Main",
        "operationId": "main_streamingSearch_get",
        "parameters": [
          {
            "name": "query",
            "in": "query",
            "required": true,
            "schema": {
              "title": "Query",
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "text/event-stream": {
                "schema": {
                  "title": "Response",
                  "type": "string"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta LICENSE para más detalles.

---

## Créditos

Desarrollado por Santiago Morillo Segovia y colaboradores.  
Inspirado en tecnologías de vanguardia para IA conversacional y búsqueda web.

---

¿Dudas o sugerencias? ¡Explora, experimenta y contribuye!