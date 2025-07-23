hotel-reservation-system/
│
├── README.md
├── docker-compose.yml
├── .gitignore
├── .env.example
│
├── frontend/                           # Aplicaciones Frontend
│   ├── web-app/                       # Aplicación Web
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/            # Componentes reutilizables
│   │   │   ├── pages/                 # Páginas principales
│   │   │   ├── services/              # Servicios API
│   │   │   ├── hooks/                 # Custom hooks
│   │   │   ├── utils/                 # Utilidades
│   │   │   ├── styles/                # Estilos globales
│   │   │   └── App.js
│   │   ├── package.json
│   │   └── Dockerfile
│   │
│   ├── mobile-app/                    # Aplicación Móvil
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── screens/
│   │   │   ├── navigation/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   ├── package.json
│   │   └── app.json
│   │
│   └── admin-panel/                   # Panel de Administración
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── services/
│       │   └── utils/
│       ├── package.json
│       └── Dockerfile
│
├── backend/                           # Microservicios Backend
│   ├── api-gateway/                   # API Gateway
│   │   ├── src/
│   │   │   ├── middleware/            # Middleware personalizado
│   │   │   ├── routes/                # Definición de rutas
│   │   │   ├── config/                # Configuraciones
│   │   │   └── app.js
│   │   ├── package.json
│   │   └── Dockerfile
│   │
│   ├── services/                      # Microservicios
│   │   ├── user-service/              # Gestión de Usuarios
│   │   │   ├── src/
│   │   │   │   ├── controllers/       # Controladores
│   │   │   │   ├── models/            # Modelos de datos
│   │   │   │   ├── services/          # Lógica de negocio
│   │   │   │   ├── repositories/      # Acceso a datos
│   │   │   │   ├── routes/            # Rutas del servicio
│   │   │   │   ├── middleware/        # Middleware específico
│   │   │   │   ├── config/            # Configuraciones
│   │   │   │   └── app.js
│   │   │   ├── tests/                 # Pruebas unitarias
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   ├── auth-service/              # Autenticación y Autorización
│   │   │   ├── src/
│   │   │   │   ├── controllers/
│   │   │   │   ├── services/
│   │   │   │   ├── middleware/
│   │   │   │   ├── utils/             # JWT, hashing, etc.
│   │   │   │   └── app.js
│   │   │   ├── tests/
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   ├── search-service/            # Motor de Búsqueda
│   │   │   ├── src/
│   │   │   │   ├── controllers/
│   │   │   │   ├── services/
│   │   │   │   ├── algorithms/        # Algoritmos de búsqueda
│   │   │   │   ├── cache/             # Gestión de cache
│   │   │   │   └── app.js
│   │   │   ├── tests/
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   ├── reservation-service/       # Gestión de Reservas
│   │   │   ├── src/
│   │   │   │   ├── controllers/
│   │   │   │   ├── models/
│   │   │   │   ├── services/
│   │   │   │   ├── state-machine/     # Máquina de estados
│   │   │   │   ├── events/            # Eventos de reserva
│   │   │   │   └── app.js
│   │   │   ├── tests/
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   ├── inventory-service/         # Gestión de Inventario
│   │   │   ├── src/
│   │   │   │   ├── controllers/
│   │   │   │   ├── models/
│   │   │   │   ├── services/
│   │   │   │   ├── availability/      # Lógica de disponibilidad
│   │   │   │   └── app.js
│   │   │   ├── tests/
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   ├── payment-service/           # Procesamiento de Pagos
│   │   │   ├── src/
│   │   │   │   ├── controllers/
│   │   │   │   ├── services/
│   │   │   │   ├── gateways/          # Integraciones de pago
│   │   │   │   ├── webhooks/          # Webhooks de pagos
│   │   │   │   └── app.js
│   │   │   ├── tests/
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   ├── notification-service/      # Servicio de Notificaciones
│   │   │   ├── src/
│   │   │   │   ├── controllers/
│   │   │   │   ├── services/
│   │   │   │   ├── templates/         # Plantillas de mensajes
│   │   │   │   ├── providers/         # Email, SMS providers
│   │   │   │   └── app.js
│   │   │   ├── tests/
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   ├── hotel-management-service/  # Gestión de Hoteles
│   │   │   ├── src/
│   │   │   │   ├── controllers/
│   │   │   │   ├── models/
│   │   │   │   ├── services/
│   │   │   │   └── app.js
│   │   │   ├── tests/
│   │   │   ├── package.json
│   │   │   └── Dockerfile
│   │   │
│   │   └── review-service/            # Reseñas y Calificaciones
│   │       ├── src/
│   │       │   ├── controllers/
│   │       │   ├── models/
│   │       │   ├── services/
│   │       │   └── app.js
│   │       ├── tests/
│   │       ├── package.json
│   │       └── Dockerfile
│   │
│   └── shared/                        # Código compartido
│       ├── middleware/                # Middleware común
│       ├── utils/                     # Utilidades compartidas
│       ├── constants/                 # Constantes globales
│       ├── validators/                # Validaciones comunes
│       └── errors/                    # Manejo de errores
│
├── infrastructure/                    # Infraestructura y DevOps
│   ├── kubernetes/                    # Manifiestos K8s
│   │   ├── namespaces/
│   │   ├── deployments/
│   │   ├── services/
│   │   ├── ingress/
│   │   └── configmaps/
│   │
│   ├── terraform/                     # Infraestructura como código
│   │   ├── modules/
│   │   ├── environments/
│   │   └── main.tf
│   │
│   ├── monitoring/                    # Monitoreo y observabilidad
│   │   ├── prometheus/
│   │   ├── grafana/
│   │   └── jaeger/
│   │
│   └── scripts/                       # Scripts de deployment
│       ├── build.sh
│       ├── deploy.sh
│       └── migrate.sh
│
├── database/                          # Scripts de base de datos
│   ├── migrations/                    # Migraciones
│   │   ├── user-service/
│   │   ├── reservation-service/
│   │   ├── inventory-service/
│   │   ├── payment-service/
│   │   ├── hotel-management-service/
│   │   └── review-service/
│   │
│   ├── seeds/                         # Datos iniciales
│   │   ├── hotels.sql
│   │   ├── rooms.sql
│   │   └── test-users.sql
│   │
│   └── schemas/                       # Esquemas de BD
│       ├── postgresql/
│       └── mongodb/
│
├── docs/                              # Documentación
│   ├── api/                           # Documentación de API
│   │   ├── openapi.yaml
│   │   └── postman-collections/
│   │
│   ├── architecture/                  # Documentación de arquitectura
│   │   ├── diagrams/
│   │   ├── decisions/                 # ADRs (Architecture Decision Records)
│   │   └── system-design.md
│   │
│   ├── deployment/                    # Guías de deployment
│   │   ├── local-setup.md
│   │   ├── staging-deployment.md
│   │   └── production-deployment.md
│   │
│   └── user-