Concept Build a REST API that lets users store, tag, search, and manage notes or knowledge entries (like a lightweight personal wiki or PKM backend). This is realistic, simple, and covers all core REST operations. 

## ERD
```mermaid
erDiagram
    USERS {
        int id PK
        string username "unique, not null"
        string email "unique"
        string password_hash "not null"
        datetime created_at
    }

    NOTES {
        int id PK
        int user_id FK
        string title "not null"
        text context
        datetime created_at
        datetime updated_at
        boolean is_archived
    }

    USERS ||--o{ NOTES : "has"
```
