import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const compiledSchemaPath = process.argv[2];
if (!compiledSchemaPath) {
  throw new Error('Pass the compiled MySQL SQL path as the first argument.');
}
if (!process.env.MYSQL_URL) {
  throw new Error('Set MYSQL_URL to a disposable MySQL 8.0 schema.');
}

const mysqlModule = process.argv[3]
  ? await import(pathToFileURL(process.argv[3]).href)
  : await import('mysql2/promise');
const mysql = mysqlModule.default ?? mysqlModule;
const connection = await mysql.createConnection(process.env.MYSQL_URL);
const packageRoot = fileURLToPath(new URL('../', import.meta.url));

async function executeScript(source) {
  let delimiter = ';';
  let statement = '';

  for (const line of source.split(/\r?\n/)) {
    const directive = line.match(/^DELIMITER\s+(.+)$/i);
    if (directive) {
      delimiter = directive[1];
      continue;
    }

    statement += `${line}\n`;
    if (statement.trimEnd().endsWith(delimiter)) {
      const sql = statement.trimEnd().slice(0, -delimiter.length).trim();
      if (sql) await connection.query(sql);
      statement = '';
    }
  }

  assert.equal(statement.trim(), '', 'SQL script ended with an incomplete statement');
}

try {
  await executeScript(readFileSync(compiledSchemaPath, 'utf8'));
  await executeScript(readFileSync(`${packageRoot}persistence.sql`, 'utf8'));

  await connection.query('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE');
  await connection.beginTransaction();
  const id = (n) => `00000000-0000-4000-8000-${String(n).padStart(12, '0')}`;
  const host = id(1);
  const session = id(10);
  await connection.query(
    'INSERT INTO principals(id, created_at) VALUES (?, UTC_TIMESTAMP())',
    [host],
  );
  await connection.query(
    `INSERT INTO sessions(id, kind, status, designated_host_principal_id, created_at)
     VALUES (?, 'VIDEO_CONFERENCE', 'LIVE', ?, UTC_TIMESTAMP())`,
    [session, host],
  );
  await connection.query(
    `INSERT INTO participants(
       id, session_id, principal_id, display_name, role, status, joined_at
     ) VALUES (?, ?, ?, 'Host', 'HOST', 'JOINED', UTC_TIMESTAMP())`,
    [id(20), session, host],
  );
  await connection.rollback();

  console.log('PASS: applied the generated schema and MySQL persistence supplement.');
} finally {
  await connection.end();
}
