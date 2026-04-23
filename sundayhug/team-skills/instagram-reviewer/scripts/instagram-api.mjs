#!/usr/bin/env node
/**
 * Instagram API Client - RapidAPI Social API4
 *
 * Usage:
 *   node --env-file=.env scripts/instagram-api.mjs <command> [options]
 *
 * Commands:
 *   search-users  --query "육아맘"            Search users by keyword
 *   similar       --username "account"         Find similar accounts
 *   hashtag       --tag "육아템"               Hashtag posts & reels
 *   info          --username "account"         User profile details
 *   posts         --username "account"         User posts & reels
 *   tagged        --username "account"         Tagged posts
 *   reels         --username "account"         User reels
 *
 * Options:
 *   --output, -o   Output file path (stdout if omitted)
 *   --format, -f   json | csv (default: json)
 */

import { parseArgs } from 'node:util';
import { writeFileSync } from 'node:fs';

const BASE_URL = 'https://social-api4.p.rapidapi.com';
const HOST = 'social-api4.p.rapidapi.com';
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 2000;

// ── CLI Argument Parsing ──────────────────────────────────────────

function parseCli() {
  const options = {
    query:    { type: 'string', short: 'q' },
    username: { type: 'string', short: 'u' },
    tag:      { type: 'string', short: 't' },
    output:   { type: 'string', short: 'o' },
    format:   { type: 'string', short: 'f', default: 'json' },
    help:     { type: 'boolean', short: 'h' },
  };

  const { values, positionals } = parseArgs({ options, allowPositionals: true });

  if (values.help || positionals.length === 0) {
    printHelp();
    process.exit(0);
  }

  return {
    command:  positionals[0],
    query:    values.query,
    username: values.username,
    tag:      values.tag,
    output:   values.output,
    format:   values.format || 'json',
  };
}

function printHelp() {
  console.log(`
Instagram API Client — RapidAPI Social API4

Usage:
  node --env-file=.env instagram-api.mjs <command> [options]

Commands:
  search-users  --query "keyword"       Search users
  similar       --username "account"    Find similar accounts
  hashtag       --tag "hashtag"         Hashtag posts & reels
  info          --username "account"    User profile details
  posts         --username "account"    User posts & reels
  tagged        --username "account"    Tagged posts
  reels         --username "account"    User reels

Options:
  --output, -o   Output file path (stdout if omitted)
  --format, -f   json | csv (default: json)
  --help, -h     Show this help
`);
}

// ── API Call ───────────────────────────────────────────────────────

async function callApi(endpoint, params = {}) {
  const apiKey = process.env.RAPIDAPI_KEY;
  if (!apiKey) {
    console.error('Error: RAPIDAPI_KEY not found in environment.');
    console.error('Add to .env: RAPIDAPI_KEY=your_key_here');
    process.exit(1);
  }

  const url = new URL(`${BASE_URL}${endpoint}`);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) url.searchParams.set(k, v);
  }

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    const res = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'x-rapidapi-host': HOST,
        'x-rapidapi-key': apiKey,
      },
    });

    if (res.status === 429) {
      if (attempt < MAX_RETRIES) {
        const wait = RETRY_DELAY_MS * attempt;
        console.error(`Rate limited (429). Retrying in ${wait}ms... (${attempt}/${MAX_RETRIES})`);
        await sleep(wait);
        continue;
      }
      console.error('Error: Rate limit exceeded after retries.');
      process.exit(1);
    }

    if (!res.ok) {
      const text = await res.text();
      console.error(`Error: API ${res.status} — ${text}`);
      process.exit(1);
    }

    return res.json();
  }
}

// ── Command Handlers ──────────────────────────────────────────────

const commands = {
  'search-users': async (args) => {
    if (!args.query) { console.error('Error: --query required'); process.exit(1); }
    return callApi('/v1/search_users', { search_query: args.query });
  },

  similar: async (args) => {
    if (!args.username) { console.error('Error: --username required'); process.exit(1); }
    return callApi('/v1/similar_accounts', { username_or_id_or_url: args.username });
  },

  hashtag: async (args) => {
    if (!args.tag) { console.error('Error: --tag required'); process.exit(1); }
    return callApi('/v1/hashtag', { hashtag: args.tag });
  },

  info: async (args) => {
    if (!args.username) { console.error('Error: --username required'); process.exit(1); }
    return callApi('/v1/info', { username_or_id_or_url: args.username });
  },

  posts: async (args) => {
    if (!args.username) { console.error('Error: --username required'); process.exit(1); }
    return callApi('/v1/posts', { username_or_id_or_url: args.username });
  },

  tagged: async (args) => {
    if (!args.username) { console.error('Error: --username required'); process.exit(1); }
    return callApi('/v1/tagged', { username_or_id_or_url: args.username });
  },

  reels: async (args) => {
    if (!args.username) { console.error('Error: --username required'); process.exit(1); }
    return callApi('/v1/reels', { username_or_id_or_url: args.username });
  },
};

// ── Output Formatting ─────────────────────────────────────────────

function outputResult(data, format, outputPath) {
  let content;

  if (format === 'csv') {
    content = toCsv(data);
  } else {
    content = JSON.stringify(data, null, 2);
  }

  if (outputPath) {
    writeFileSync(outputPath, content, 'utf-8');
    console.log(`Saved to: ${outputPath}`);
  } else {
    console.log(content);
  }
}

function toCsv(data) {
  // Normalise: if data has a nested array, extract it
  let rows = Array.isArray(data) ? data : (data.data || data.items || data.users || [data]);
  if (!Array.isArray(rows)) rows = [rows];
  if (rows.length === 0) return '';

  const headers = Object.keys(flattenObj(rows[0]));
  const lines = [headers.join(',')];

  for (const row of rows) {
    const flat = flattenObj(row);
    const vals = headers.map((h) => {
      let v = flat[h];
      if (v === null || v === undefined) return '';
      v = String(v);
      if (v.length > 200) v = v.slice(0, 200) + '...';
      if (v.includes(',') || v.includes('"') || v.includes('\n')) {
        return `"${v.replace(/"/g, '""')}"`;
      }
      return v;
    });
    lines.push(vals.join(','));
  }

  return lines.join('\n');
}

function flattenObj(obj, prefix = '') {
  const result = {};
  for (const [k, v] of Object.entries(obj || {})) {
    const key = prefix ? `${prefix}.${k}` : k;
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      Object.assign(result, flattenObj(v, key));
    } else if (Array.isArray(v)) {
      result[key] = JSON.stringify(v);
    } else {
      result[key] = v;
    }
  }
  return result;
}

// ── Utilities ─────────────────────────────────────────────────────

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// ── Main ──────────────────────────────────────────────────────────

async function main() {
  const args = parseCli();
  const handler = commands[args.command];

  if (!handler) {
    console.error(`Unknown command: ${args.command}`);
    console.error(`Available: ${Object.keys(commands).join(', ')}`);
    process.exit(1);
  }

  console.error(`[instagram-api] ${args.command} ...`);
  const data = await handler(args);
  outputResult(data, args.format, args.output);
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
