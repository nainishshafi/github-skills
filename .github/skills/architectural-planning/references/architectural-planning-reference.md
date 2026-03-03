# Architectural Planning Reference

Technology compatibility matrices, Mermaid diagram templates, output document template, and project structure templates for the architectural-planning skill.

_Last updated: 2026-03-03_

---

## Section 1 — Backend Stack Matrix

| Stack | Language | Framework | Package Manager | Testing | Strengths | Best For |
|-------|----------|-----------|-----------------|---------|-----------|----------|
| Java / Spring Boot | Java 21+ | Spring Boot 3.x | Maven or Gradle | JUnit 5 + Mockito | Enterprise-grade, strong typing, massive ecosystem, mature tooling | Large teams, microservices, enterprise integrations, banking/finance |
| Node.js / Express | Node 20+ (TS recommended) | Express 4.x / 5.x | npm or pnpm | Jest or Vitest | Fast iteration, JS everywhere, huge npm ecosystem, async I/O | Startups, real-time apps, full-stack JS teams, BFF layers |
| Python / Django | Python 3.11+ | Django 5.x | pip + requirements.txt or Poetry | pytest + Django test client | Batteries included, rapid prototyping, excellent admin panel | MVPs, admin-heavy apps, content platforms, ML/data projects |
| Python / FastAPI | Python 3.11+ | FastAPI 0.110+ | pip + requirements.txt or Poetry | pytest + httpx | Modern async, auto-generated OpenAPI docs, high performance | APIs, microservices, ML model serving, data pipelines |
| Go | Go 1.22+ | stdlib net/http or Gin/Echo | go modules | testing + testify | High performance, built-in concurrency, small binaries, fast compile | Microservices, infrastructure tools, high-throughput APIs, CLI tools |
| .NET / ASP.NET Core | C# 12 / .NET 8+ | ASP.NET Core | NuGet + dotnet CLI | xUnit or NUnit + Moq | Enterprise framework, excellent tooling, cross-platform, strong typing | Enterprise apps, Windows ecosystem, large teams, Azure-native |
| Rust / Actix-web | Rust 1.75+ | Actix-web 4.x | Cargo | built-in #[test] + tokio::test | Maximum performance, memory safety, zero-cost abstractions | Performance-critical services, systems programming, embedded APIs |

### When NOT to Use

| Stack | Avoid When |
|-------|-----------|
| Java / Spring Boot | Small prototypes, solo developer projects needing fast iteration |
| Node.js / Express | CPU-intensive computation, strict type safety requirements without TS |
| Python / Django | High-concurrency real-time apps, performance-critical microservices |
| Python / FastAPI | Need server-rendered HTML, need Django-style admin panel |
| Go | Rapid prototyping, heavy ORM usage, complex business logic with deep inheritance |
| .NET / ASP.NET Core | Linux-only teams unfamiliar with C#, small scripts or utilities |
| Rust / Actix-web | Rapid prototyping, teams unfamiliar with Rust, short-lived projects |

---

## Section 2 — Database Compatibility Matrix

Recommended ORM / data-access library for each backend + database combination.

### Relational Databases

| Backend | PostgreSQL | MySQL / MariaDB | SQL Server | SQLite |
|---------|-----------|-----------------|-----------|--------|
| Spring Boot | Spring Data JPA + Hibernate + HikariCP | Spring Data JPA + Hibernate + HikariCP | Spring Data JPA + Hibernate + HikariCP | Spring Data JPA (dev/test only) |
| Node.js / Express | Prisma or TypeORM + pg | Prisma or TypeORM + mysql2 | Prisma + mssql or tedious | Prisma + better-sqlite3 |
| Python / Django | Django ORM + psycopg2-binary | Django ORM + mysqlclient | Django ORM + django-mssql-backend | Django ORM (built-in sqlite3) |
| Python / FastAPI | SQLAlchemy 2.0 + asyncpg (async) or psycopg2 | SQLAlchemy 2.0 + aiomysql | SQLAlchemy 2.0 + aioodbc | SQLAlchemy 2.0 + aiosqlite |
| Go | pgx (recommended) or GORM + pgx driver | go-sql-driver/mysql or GORM | go-mssqldb or GORM | go-sqlite3 or GORM |
| .NET / ASP.NET Core | EF Core + Npgsql | EF Core + Pomelo.EntityFrameworkCore.MySql | EF Core + Microsoft.Data.SqlClient | EF Core + Microsoft.EntityFrameworkCore.Sqlite |
| Rust / Actix-web | sqlx (compile-time checked) or Diesel | sqlx or Diesel | sqlx (with mssql feature) | sqlx or Diesel |

### NoSQL Databases

| Backend | MongoDB | DynamoDB | Redis (as primary) |
|---------|---------|----------|-------------------|
| Spring Boot | Spring Data MongoDB | AWS SDK for Java v2 | Spring Data Redis + Lettuce |
| Node.js / Express | Mongoose or mongodb (native) | @aws-sdk/client-dynamodb | ioredis |
| Python / Django | djongo or MongoEngine (limited Django integration) | boto3 + dynamodb | django-redis |
| Python / FastAPI | Motor (async) + Beanie (ODM) | boto3 + aiobotocore | redis-py (async) |
| Go | mongo-driver (official) | aws-sdk-go-v2/service/dynamodb | go-redis/redis |
| .NET / ASP.NET Core | MongoDB.Driver (official) | AWSSDK.DynamoDBv2 | StackExchange.Redis |
| Rust / Actix-web | mongodb (official) | aws-sdk-dynamodb | redis-rs |

### Migration Tools

| Backend | Recommended Migration Tool |
|---------|--------------------------|
| Spring Boot | Flyway or Liquibase |
| Node.js / Express | Prisma Migrate or Knex migrations |
| Python / Django | Django migrations (built-in) |
| Python / FastAPI | Alembic |
| Go | golang-migrate/migrate or goose |
| .NET / ASP.NET Core | EF Core Migrations (built-in) |
| Rust / Actix-web | sqlx migrate or diesel_migrations |

---

## Section 3 — Caching Library Matrix

| Backend | Redis | Memcached | In-Memory |
|---------|-------|-----------|-----------|
| Spring Boot | spring-boot-starter-data-redis + Lettuce | spring-boot-starter-cache + XMemcached | Caffeine + spring-boot-starter-cache |
| Node.js / Express | ioredis or redis (v4+) | memcached or memjs | node-cache or lru-cache |
| Python / Django | django-redis | django.core.cache.backends.memcached.PyMemcacheCache | django.core.cache.backends.locmem.LocMemCache |
| Python / FastAPI | redis-py (async mode) | aiomcache | cachetools or functools.lru_cache |
| Go | go-redis/redis | bradfitz/gomemcache | dgraph-io/ristretto or hashicorp/golang-lru |
| .NET / ASP.NET Core | StackExchange.Redis + IDistributedCache | EnyimMemcachedCore | IMemoryCache (built-in) |
| Rust / Actix-web | redis-rs (async) | memcache-rs | moka (concurrent cache) |

### Caching Strategy Guidance

| Strategy | When to Use | Typical TTL |
|----------|-------------|-------------|
| **Redis** | Multi-instance apps, session storage, rate limiting, pub/sub | 5 min – 24 hr |
| **Memcached** | Simple key-value caching, large cache pools, no persistence needed | 5 min – 1 hr |
| **In-Memory** | Single-instance apps, frequently accessed config/lookup data | App lifetime |
| **CDN** | Static assets, public API responses, media files | 1 hr – 7 days |
| **Multi-layer** | High-traffic apps: L1 in-memory → L2 Redis → L3 CDN | Varies per layer |

---

## Section 4 — Authentication Library Matrix

| Backend | JWT | Session-based | OAuth 2.0 / OIDC | Framework Built-in |
|---------|-----|--------------|-------------------|-------------------|
| Spring Boot | spring-security-oauth2-jose + nimbus-jose-jwt | Spring Session + spring-session-data-redis | Spring Security OAuth2 Client | Spring Security (full stack) |
| Node.js / Express | jsonwebtoken + express-jwt | express-session + connect-redis | passport + passport-google-oauth20 | Passport.js (strategy-based) |
| Python / Django | djangorestframework-simplejwt | Django sessions (built-in) | django-allauth | Django Auth + django.contrib.auth |
| Python / FastAPI | python-jose + fastapi.security | N/A (use JWT for stateless APIs) | authlib | N/A (compose from libraries) |
| Go | golang-jwt/jwt | gorilla/sessions | golang.org/x/oauth2 | N/A (compose from libraries) |
| .NET / ASP.NET Core | Microsoft.AspNetCore.Authentication.JwtBearer | ASP.NET Core sessions (built-in) | Microsoft.AspNetCore.Authentication.OpenIdConnect | ASP.NET Core Identity |
| Rust / Actix-web | jsonwebtoken crate | actix-session | oxide-auth | N/A (compose from crates) |

### Managed Auth Services

| Service | Best For | Pricing Model |
|---------|----------|--------------|
| **Auth0** | Full-featured identity, social login, enterprise SSO | Free tier (7.5K MAU), then per-MAU |
| **Firebase Auth** | Mobile apps, rapid prototyping, Google ecosystem | Free tier (50K MAU), then per-verification |
| **Keycloak** | Self-hosted, full control, enterprise on-prem | Free (open source), self-manage infra |
| **AWS Cognito** | AWS-native apps, serverless | Free tier (50K MAU), then per-MAU |
| **Supabase Auth** | Supabase users, PostgreSQL-backed auth | Free tier, then per-MAU |

---

## Section 5 — Mermaid Diagram Templates

### Monolith Architecture

```
graph TB
    Client[Client / Browser]
    LB[Load Balancer<br>nginx / ALB]
    App[Application Server<br>BACKEND_STACK]
    Cache[(Cache<br>CACHE_CHOICE)]
    DB[(Database<br>DB_CHOICE)]

    Client -->|HTTPS| LB
    LB --> App
    App <--> Cache
    App <--> DB
```

### Full-Stack Monolith

```
graph TB
    Browser[Browser]
    CDN[CDN / Static Hosting<br>CloudFront / Vercel]
    LB[Load Balancer]
    FE[Frontend<br>FRONTEND_STACK]
    API[API Server<br>BACKEND_STACK]
    Cache[(Cache<br>CACHE_CHOICE)]
    DB[(Database<br>DB_CHOICE)]

    Browser -->|Static Assets| CDN
    Browser -->|API Calls| LB
    CDN --> FE
    LB --> API
    API <--> Cache
    API <--> DB
```

### Microservices Architecture

```
graph TB
    Client[Client]
    GW[API Gateway<br>Kong / AWS API GW]
    SVC_A[Service A<br>STACK_A]
    SVC_B[Service B<br>STACK_B]
    SVC_C[Service C<br>STACK_C]
    DB_A[(DB A<br>DB_CHOICE_A)]
    DB_B[(DB B<br>DB_CHOICE_B)]
    DB_C[(DB C<br>DB_CHOICE_C)]
    MQ[Message Broker<br>MESSAGING_CHOICE]
    Cache[(Shared Cache<br>CACHE_CHOICE)]

    Client -->|HTTPS| GW
    GW --> SVC_A
    GW --> SVC_B
    GW --> SVC_C
    SVC_A <--> DB_A
    SVC_B <--> DB_B
    SVC_C <--> DB_C
    SVC_A --> MQ
    MQ --> SVC_B
    MQ --> SVC_C
    SVC_A <--> Cache
    SVC_B <--> Cache
```

### Serverless Architecture

```
graph TB
    Client[Client]
    APIGW[API Gateway<br>AWS API GW / Azure APIM]
    FN_A[Function A<br>Lambda / Azure Func]
    FN_B[Function B<br>Lambda / Azure Func]
    Queue[Queue<br>SQS / Service Bus]
    DB[(Database<br>DynamoDB / Cosmos DB)]
    Storage[Object Storage<br>S3 / Blob Storage]

    Client -->|HTTPS| APIGW
    APIGW --> FN_A
    APIGW --> FN_B
    FN_A --> DB
    FN_A --> Queue
    Queue --> FN_B
    FN_B --> DB
    FN_B --> Storage
```

### Deployment Topology

```
graph TB
    subgraph CLOUD_PROVIDER
        subgraph VPC / Virtual Network
            subgraph Public Subnet
                LB[Load Balancer]
                Bastion[Bastion Host]
            end
            subgraph Private Subnet - App
                App1[App Instance 1]
                App2[App Instance 2]
            end
            subgraph Private Subnet - Data
                DB[(Primary DB)]
                DB_R[(Read Replica)]
                Cache[(Cache Cluster)]
            end
        end
    end

    Internet[Internet] -->|HTTPS| LB
    LB --> App1
    LB --> App2
    App1 <--> DB
    App2 <--> DB_R
    App1 <--> Cache
    App2 <--> Cache
    DB -->|Replication| DB_R
```

### CI/CD Pipeline

```
graph LR
    Push[Git Push] --> Build[Build & Compile]
    Build --> UnitTest[Unit Tests]
    UnitTest --> Lint[Lint & SAST]
    Lint --> IntTest[Integration Tests]
    IntTest --> DockerBuild[Build Image]
    DockerBuild --> Staging[Deploy to Staging]
    Staging --> Approval{Manual Approval}
    Approval -->|Approved| Prod[Deploy to Production]
    Approval -->|Rejected| Fix[Fix & Re-push]
```

---

## Section 6 — Output Document Template

Use this template when generating the architecture document. Replace all `{PLACEHOLDER}` values with the user's choices.

```markdown
# Architecture Document: {PROJECT_NAME}

_Generated: {DATE} | Stack: {BACKEND_STACK} + {FRONTEND_STACK} + {DATABASE}_

## 1. System Overview

{2-3 paragraph description of the system, its purpose, and the key architectural decisions made. Reference the project type, expected scale, and primary technology choices.}

### System Architecture Diagram

{Insert Mermaid diagram from Section 5 templates, customized with actual technology choices}

## 2. Component Breakdown

### {Component/Service 1}
- **Responsibility:** {what it does}
- **Technology:** {framework, language, key libraries}
- **Exposes:** {APIs, events, or interfaces it provides}
- **Depends on:** {other components or external services}

### {Component/Service 2}
{Repeat for each component}

## 3. Data Model

### Core Entities

#### {Entity Name}
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | {type} | PK, auto-generated | Unique identifier |
| created_at | timestamp | NOT NULL, DEFAULT now() | Record creation time |
| {field} | {type} | {constraints} | {description} |

### Entity Relationship Diagram

{Mermaid erDiagram showing relationships between core entities}

## 4. API Design

- **Style:** {REST / GraphQL / gRPC}
- **Base URL:** `/api/v1`
- **Versioning:** {URL path / header / query param}
- **Content type:** {application/json / protobuf}
- **Rate limiting:** {strategy — e.g., 100 req/min per API key}

### Key Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /api/v1/auth/login | Authenticate user | Public |
| GET | /api/v1/{resource} | List {resources} | {AUTH_APPROACH} |
| POST | /api/v1/{resource} | Create {resource} | {AUTH_APPROACH} |
| GET | /api/v1/{resource}/:id | Get {resource} by ID | {AUTH_APPROACH} |
| PUT | /api/v1/{resource}/:id | Update {resource} | {AUTH_APPROACH} |
| DELETE | /api/v1/{resource}/:id | Delete {resource} | {AUTH_APPROACH} |

## 5. Security Architecture

### Authentication
- **Method:** {AUTH_APPROACH with specific library}
- **Token storage:** {httpOnly cookie / localStorage / Authorization header}
- **Token lifetime:** {access: 15 min, refresh: 7 days — adjust per requirements}

### Authorization
- **Model:** {RBAC / ABAC / policy-based}
- **Roles:** {admin, user, viewer — customize per project}

### Data Protection
- **In transit:** TLS 1.3 (HTTPS everywhere)
- **At rest:** {AES-256 / transparent DB encryption / cloud KMS}
- **Secrets management:** {environment variables / HashiCorp Vault / AWS Secrets Manager / Azure Key Vault}
- **PII handling:** {encryption, masking, GDPR compliance notes}

## 6. Caching Strategy

- **Technology:** {CACHE_CHOICE}
- **Library:** {specific library from Section 3}
- **Cache-aside pattern:** Application checks cache first, falls back to DB, then populates cache
- **Invalidation:** {TTL-based / event-based / write-through}
- **Key namespacing:** `{service}:{entity}:{id}` — e.g., `user-svc:user:123`

## 7. Deployment Architecture

### Deployment Topology Diagram

{Insert deployment Mermaid diagram from Section 5, customized}

### Environment Strategy

| Environment | Purpose | Infrastructure | URL |
|-------------|---------|---------------|-----|
| Development | Local dev | Docker Compose | localhost:{port} |
| Staging | Pre-production testing | {DEPLOYMENT_CHOICE} | staging.{domain} |
| Production | Live traffic | {DEPLOYMENT_CHOICE} | {domain} |

### Scaling
- **Strategy:** {horizontal auto-scaling / vertical / manual}
- **Min/Max instances:** {2 / 10 — adjust per scale}
- **Scaling triggers:** CPU > 70%, memory > 80%, request latency > 500ms

### Disaster Recovery
- **Database backups:** {automated daily snapshots, 30-day retention}
- **RTO / RPO:** {Recovery Time Objective / Recovery Point Objective}
- **Multi-region:** {yes/no — based on scale}

## 8. Project Structure

{Insert project structure template from Section 7, customized for the chosen backend stack}

## 9. Dependencies

| Category | Library | Version | Purpose |
|----------|---------|---------|---------|
| Framework | {BACKEND_FRAMEWORK} | {VERSION} | Web framework |
| ORM / Data Access | {ORM_LIBRARY} | {VERSION} | Database access |
| Migration | {MIGRATION_TOOL} | {VERSION} | Schema migrations |
| Cache | {CACHE_LIBRARY} | {VERSION} | Caching layer |
| Auth | {AUTH_LIBRARY} | {VERSION} | Authentication |
| Validation | {VALIDATION_LIB} | {VERSION} | Input validation |
| Logging | {LOGGING_LIB} | {VERSION} | Structured logging |
| Testing | {TEST_FRAMEWORK} | {VERSION} | Unit/integration tests |
| HTTP Client | {HTTP_CLIENT} | {VERSION} | External API calls |
| Config | {CONFIG_LIB} | {VERSION} | Configuration management |

## 10. CI/CD Pipeline

### Pipeline Diagram

{Insert CI/CD Mermaid diagram from Section 5}

### Pipeline Stages

| Stage | Tool | Description |
|-------|------|-------------|
| Build | {CICD_CHOICE} | Compile, resolve dependencies |
| Unit Test | {TEST_FRAMEWORK} | Run unit tests, fail on < 80% coverage |
| Lint / SAST | {linter + security scanner} | Code quality and security checks |
| Integration Test | {TEST_FRAMEWORK} | Test with real DB (Docker) |
| Build Image | Docker | Build and push container image |
| Deploy Staging | {DEPLOYMENT_CHOICE} | Deploy to staging environment |
| Smoke Test | curl / Postman / k6 | Verify staging health |
| Deploy Production | {DEPLOYMENT_CHOICE} | Deploy to production (manual approval) |

## 11. Monitoring & Observability

### Metrics
- **Tool:** {MONITORING_CHOICE}
- **Key metrics:** request rate, error rate, latency (p50/p95/p99), CPU, memory, DB connections
- **Dashboards:** {list key dashboards to create}

### Logging
- **Format:** Structured JSON
- **Library:** {stack-specific: logback/winston/structlog/slog/Serilog}
- **Aggregation:** {ELK / CloudWatch Logs / Datadog Logs}

### Distributed Tracing
- **Tool:** {OpenTelemetry / Jaeger / Datadog APM / X-Ray}
- **Propagation:** W3C Trace Context headers

### Alerting
- **Critical:** Service down, error rate > 5%, latency p99 > 2s → PagerDuty / Slack
- **Warning:** CPU > 70%, memory > 80%, disk > 85% → Slack
- **Info:** Deployment completed, scaling event → Slack
```

---

## Section 7 — Project Structure Templates

### Java / Spring Boot

```
project-root/
├── src/
│   ├── main/
│   │   ├── java/com/example/{project}/
│   │   │   ├── config/              # Spring configuration classes
│   │   │   ├── controller/          # REST controllers
│   │   │   ├── service/             # Business logic
│   │   │   ├── repository/          # JPA repositories
│   │   │   ├── model/               # JPA entities
│   │   │   ├── dto/                 # Request/Response DTOs
│   │   │   ├── exception/           # Custom exceptions + handler
│   │   │   ├── security/            # Auth filters, JWT utils
│   │   │   └── Application.java     # Main entry point
│   │   └── resources/
│   │       ├── application.yml      # Config (profiles: dev, prod)
│   │       └── db/migration/        # Flyway migrations
│   └── test/
│       └── java/com/example/{project}/
│           ├── controller/          # Controller integration tests
│           ├── service/             # Service unit tests
│           └── repository/          # Repository tests (@DataJpaTest)
├── pom.xml                          # Maven (or build.gradle for Gradle)
├── Dockerfile
└── docker-compose.yml
```

### Node.js / Express

```
project-root/
├── src/
│   ├── config/                      # Environment, DB, cache config
│   │   ├── database.ts
│   │   ├── cache.ts
│   │   └── index.ts
│   ├── controllers/                 # Route handlers
│   ├── middleware/                   # Auth, validation, error handling
│   ├── models/                      # Prisma schema or TypeORM entities
│   ├── routes/                      # Express route definitions
│   ├── services/                    # Business logic
│   ├── utils/                       # Shared utilities
│   ├── validators/                  # Request validation schemas (Zod/Joi)
│   └── app.ts                       # Express app setup
├── prisma/
│   └── schema.prisma                # Prisma schema (if using Prisma)
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
├── tsconfig.json
├── Dockerfile
└── docker-compose.yml
```

### Python / Django

```
project-root/
├── apps/
│   ├── core/                        # Shared models, utilities
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tests/
│   │   └── migrations/
│   ├── users/                       # User management app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── tests/
│   └── {feature}/                   # Additional feature apps
├── config/
│   ├── settings/
│   │   ├── base.py                  # Shared settings
│   │   ├── dev.py                   # Development overrides
│   │   └── prod.py                  # Production overrides
│   ├── urls.py                      # Root URL config
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt                 # or pyproject.toml (Poetry)
├── Dockerfile
└── docker-compose.yml
```

### Python / FastAPI

```
project-root/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/           # Route handlers per resource
│   │       │   ├── auth.py
│   │       │   └── {resource}.py
│   │       └── router.py            # Aggregates all v1 routes
│   ├── core/
│   │   ├── config.py                # Settings via pydantic-settings
│   │   ├── security.py              # JWT, password hashing
│   │   └── dependencies.py          # Shared FastAPI dependencies
│   ├── db/
│   │   ├── session.py               # SQLAlchemy async session
│   │   └── base.py                  # Declarative base
│   ├── models/                      # SQLAlchemy models
│   ├── schemas/                     # Pydantic request/response models
│   ├── services/                    # Business logic
│   ├── main.py                      # FastAPI app entry point
│   └── __init__.py
├── alembic/                         # Alembic migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_{resource}.py
├── alembic.ini
├── requirements.txt                 # or pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

### Go

```
project-root/
├── cmd/
│   └── server/
│       └── main.go                  # Entry point
├── internal/
│   ├── config/                      # Configuration loading
│   ├── handler/                     # HTTP handlers (controllers)
│   ├── middleware/                   # Auth, logging, CORS
│   ├── model/                       # Domain models / DB structs
│   ├── repository/                  # Database access layer
│   ├── service/                     # Business logic
│   └── router/                      # Route definitions
├── pkg/                             # Shared/exported packages
│   └── response/                    # Standardized API responses
├── migrations/                      # SQL migration files
├── go.mod
├── go.sum
├── Dockerfile
└── docker-compose.yml
```

### .NET / ASP.NET Core (Clean Architecture)

```
project-root/
├── src/
│   ├── {Project}.API/
│   │   ├── Controllers/             # API controllers
│   │   ├── Middleware/              # Custom middleware
│   │   ├── Filters/                # Action/exception filters
│   │   ├── Program.cs              # Entry point + DI config
│   │   └── appsettings.json        # Configuration
│   ├── {Project}.Core/
│   │   ├── Entities/               # Domain entities
│   │   ├── Interfaces/             # Repository + service interfaces
│   │   ├── Services/               # Business logic implementations
│   │   └── DTOs/                   # Data transfer objects
│   ├── {Project}.Infrastructure/
│   │   ├── Data/
│   │   │   ├── AppDbContext.cs      # EF Core DbContext
│   │   │   └── Migrations/         # EF Core migrations
│   │   ├── Repositories/           # Repository implementations
│   │   └── Identity/               # ASP.NET Identity config
├── tests/
│   ├── {Project}.UnitTests/
│   └── {Project}.IntegrationTests/
├── {Project}.sln
├── Dockerfile
└── docker-compose.yml
```

### Rust / Actix-web

```
project-root/
├── src/
│   ├── config.rs                    # Configuration
│   ├── db.rs                        # Database pool setup
│   ├── handlers/                    # Request handlers
│   │   ├── mod.rs
│   │   ├── auth.rs
│   │   └── {resource}.rs
│   ├── models/                      # Database models (sqlx/Diesel)
│   ├── middleware/                   # Custom middleware
│   ├── errors.rs                    # Error types
│   ├── routes.rs                    # Route configuration
│   └── main.rs                      # Entry point
├── migrations/                      # sqlx or Diesel migrations
├── Cargo.toml
├── Dockerfile
└── docker-compose.yml
```

---

## Section 8 — Library Version Reference

_Recommended versions as of early 2026. Update periodically._

### Java / Spring Boot
| Library | Version | Purpose |
|---------|---------|---------|
| Spring Boot | 3.3.x | Framework |
| Spring Data JPA | 3.3.x | ORM |
| Spring Security | 6.3.x | Auth |
| Flyway | 10.x | Migrations |
| HikariCP | 5.x | Connection pool |
| Caffeine | 3.1.x | In-memory cache |
| jjwt | 0.12.x | JWT |
| JUnit 5 | 5.10.x | Testing |

### Node.js / Express
| Library | Version | Purpose |
|---------|---------|---------|
| Express | 4.21.x / 5.x | Framework |
| Prisma | 6.x | ORM |
| ioredis | 5.x | Redis client |
| jsonwebtoken | 9.x | JWT |
| Zod | 3.x | Validation |
| Jest | 29.x | Testing |
| Vitest | 2.x | Testing (alternative) |
| Winston | 3.x | Logging |

### Python / Django
| Library | Version | Purpose |
|---------|---------|---------|
| Django | 5.1.x | Framework |
| djangorestframework | 3.15.x | REST API |
| psycopg2-binary | 2.9.x | PostgreSQL driver |
| django-redis | 5.4.x | Redis cache |
| djangorestframework-simplejwt | 5.3.x | JWT auth |
| django-allauth | 65.x | OAuth/social auth |
| pytest-django | 4.x | Testing |

### Python / FastAPI
| Library | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.115.x | Framework |
| SQLAlchemy | 2.0.x | ORM |
| Alembic | 1.14.x | Migrations |
| asyncpg | 0.30.x | Async PostgreSQL |
| redis | 5.x | Redis client (async) |
| python-jose | 3.3.x | JWT |
| pydantic | 2.10.x | Validation |
| httpx | 0.28.x | HTTP client + testing |

### Go
| Library | Version | Purpose |
|---------|---------|---------|
| Gin | 1.10.x | Framework |
| pgx | 5.x | PostgreSQL driver |
| GORM | 1.25.x | ORM (alternative) |
| go-redis | 9.x | Redis client |
| golang-jwt/jwt | 5.x | JWT |
| testify | 1.9.x | Testing assertions |
| golang-migrate | 4.x | Migrations |
| slog | stdlib | Structured logging |

### .NET / ASP.NET Core
| Library | Version | Purpose |
|---------|---------|---------|
| ASP.NET Core | 8.x / 9.x | Framework |
| EF Core | 8.x / 9.x | ORM |
| Npgsql.EntityFrameworkCore | 8.x | PostgreSQL provider |
| StackExchange.Redis | 2.8.x | Redis client |
| Microsoft.AspNetCore.Authentication.JwtBearer | 8.x | JWT auth |
| xUnit | 2.9.x | Testing |
| Moq | 4.20.x | Mocking |
| Serilog | 4.x | Structured logging |

### Rust / Actix-web
| Library | Version | Purpose |
|---------|---------|---------|
| actix-web | 4.x | Framework |
| sqlx | 0.8.x | Database (compile-time checked) |
| redis-rs | 0.27.x | Redis client |
| jsonwebtoken | 9.x | JWT |
| serde | 1.x | Serialization |
| tokio | 1.x | Async runtime |
| tracing | 0.1.x | Structured logging |
| moka | 0.12.x | In-memory cache |
