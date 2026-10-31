# Read the selected engine only

## SQLite

Use the application's existing file location and driver. Verify foreign-key enforcement on each
connection, use transactions for multi-step changes and handle busy/locked outcomes deliberately.
Keep the database outside a public web root. Evaluate concurrent writes before choosing SQLite
for a workload; do not add WAL or timeout settings without understanding the environment.
Reference: https://www.sqlite.org/docs.html

## MySQL / MariaDB

Inspect the actual product/version, storage engine, SQL mode, character set and collation.
Use constraints and transactions supported by that configuration; do not assume DDL rollback
behaves like ordinary row updates. Check index use with the engine's explain tools and test
migrations against an existing schema, including data conversions.
References: https://dev.mysql.com/doc/ and https://mariadb.com/docs/

## PostgreSQL / Supabase

Use constraints and explicit transaction boundaries. Check role privileges and row-level security
against the real application roles when used; a service/admin connection can hide authorization
bugs. Keep privileged service keys on the server. Test policy behavior for two different users
and unauthenticated access. Inspect query plans with representative data before adding indexes.
Review optional Supabase/Postgres skills only for the rule or operation needed.
References: https://www.postgresql.org/docs/ and https://supabase.com/docs/guides/database

## MongoDB

Choose embedding versus references from access patterns, update ownership and document growth.
Use schema validation and unique indexes for invariants where appropriate. Check required index
support, connection reuse, pool limits and transaction support against the actual topology and
driver version. Do not accept arbitrary client-provided query operators. Exercise queries and
authorization with representative documents rather than assuming SQL semantics.
Reference: https://www.mongodb.com/docs/
