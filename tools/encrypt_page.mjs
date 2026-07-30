#!/usr/bin/env node
/**
 * Encrypt one HTML page into a self-decrypting page, for pages marked
 * `protected` in tools/site-manifest.json.
 *
 *   node tools/encrypt_page.mjs <in.html> <out.html> "<title>"
 *
 * The passphrase comes from SITE_PASSPHRASE in the environment and is never
 * written anywhere — not to the output, not to a log, not to the repo.
 *
 * Why this exists
 * ---------------
 * The published site is on GitHub Pages, which serves static files with no
 * server. A JavaScript "password" check would ship the content and the password
 * to the visitor and check it afterwards — anyone could read the source. This
 * instead ships *ciphertext*: without the passphrase there is nothing to read,
 * and a search engine cannot index the plaintext.
 *
 * What it does NOT give you
 * -------------------------
 * - One shared secret. No per-person access, no revocation, no audit trail.
 * - Anyone who knows the passphrase can decrypt and reshare the plaintext.
 * - The ciphertext is public, so an attacker can brute-force offline at their
 *   leisure. **The passphrase strength is the entire security model.** A short
 *   or guessable one puts the content on the open internet with extra steps.
 * Treat it as "not casually readable or indexable", not as confidentiality.
 *
 * Crypto: PBKDF2-SHA256 (600k iterations, OWASP-recommended floor at time of
 * writing) over a random 16-byte salt to derive a 256-bit key; AES-256-GCM with
 * a random 12-byte IV. Decryption in-browser via WebCrypto. Node builtins and
 * WebCrypto only — no dependency on either side, so there is nothing to audit
 * but this file.
 */

import { readFileSync, writeFileSync } from "node:fs";
import { pbkdf2Sync, randomBytes, createCipheriv } from "node:crypto";

const ITERATIONS = 600_000;
const [, , inPath, outPath, pageTitle = "Protected"] = process.argv;

if (!inPath || !outPath) {
  console.error("usage: encrypt_page.mjs <in.html> <out.html> [title]");
  process.exit(2);
}

const passphrase = process.env.SITE_PASSPHRASE;
if (!passphrase) {
  // Fail closed. The caller must not fall back to publishing plaintext.
  console.error("SITE_PASSPHRASE is not set — refusing to emit an unencrypted page.");
  process.exit(3);
}
if (passphrase.length < 16) {
  console.error(
    `SITE_PASSPHRASE is ${passphrase.length} characters. The ciphertext is public, so a ` +
    "short passphrase can be brute-forced offline. Use at least 16 characters."
  );
  process.exit(4);
}

const plaintext = readFileSync(inPath);
const salt = randomBytes(16);
const iv = randomBytes(12);
const key = pbkdf2Sync(passphrase, salt, ITERATIONS, 32, "sha256");
const cipher = createCipheriv("aes-256-gcm", key, iv);
const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
const tag = cipher.getAuthTag();

const payload = {
  v: 1,
  kdf: { name: "PBKDF2", hash: "SHA-256", iterations: ITERATIONS,
         salt: salt.toString("base64") },
  iv: iv.toString("base64"),
  // GCM in WebCrypto expects the tag appended to the ciphertext.
  data: Buffer.concat([ciphertext, tag]).toString("base64"),
};

const esc = (s) => String(s).replace(/[&<>"]/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

writeFileSync(outPath, `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>${esc(pageTitle)}</title>
<style>
  :root{--bg:#f4f6fa;--panel:#fff;--ink:#151b26;--muted:#59636f;--line:#e2e7ef;
    --accent:#0e7c86;--warn:#c2410c;
    --shadow:0 1px 2px rgba(21,27,38,.05),0 9px 24px rgba(21,27,38,.06)}
  @media (prefers-color-scheme:dark){:root{--bg:#0a0e15;--panel:#131a24;--ink:#e7ecf3;
    --muted:#93a0b1;--line:#222c39;--accent:#2dd4bf;--warn:#f0894e;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.5)}}
  *{box-sizing:border-box}
  body{margin:0;min-height:100svh;display:grid;place-items:center;background:var(--bg);
    color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
    Helvetica,Arial,sans-serif;line-height:1.5;padding:24px}
  .box{background:var(--panel);border:1px solid var(--line);border-radius:14px;
    box-shadow:var(--shadow);padding:28px;max-width:420px;width:100%}
  .eyebrow{font-size:11px;letter-spacing:.15em;text-transform:uppercase;
    color:var(--muted);font-weight:650}
  h1{font-size:20px;margin:8px 0 6px;letter-spacing:-.01em}
  p{margin:0 0 16px;font-size:13.5px;color:var(--muted)}
  label{display:block;font-size:12.5px;font-weight:650;margin-bottom:6px}
  input{width:100%;padding:10px 12px;font:inherit;font-size:14px;color:var(--ink);
    background:var(--bg);border:1px solid var(--line);border-radius:8px}
  input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  button{margin-top:12px;width:100%;padding:10px 14px;font:inherit;font-size:14px;
    font-weight:650;color:#fff;background:var(--accent);border:0;border-radius:8px;
    cursor:pointer}
  button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .err{margin:12px 0 0;font-size:12.5px;color:var(--warn);font-weight:650}
  .note{margin-top:16px;font-size:11.5px;color:var(--muted)}
</style>
</head>
<body>
<main class="box" id="gate">
  <div class="eyebrow">Orbit Design Brain</div>
  <h1>${esc(pageTitle)}</h1>
  <p>This page names internal product surfaces, so it is encrypted. Enter the passphrase
     to read it.</p>
  <form id="f">
    <label for="p">Passphrase</label>
    <input id="p" type="password" autocomplete="current-password" autofocus>
    <button type="submit">Unlock</button>
  </form>
  <p class="err" id="e" role="alert" hidden>That passphrase didn't work.</p>
  <p class="note">Nothing is sent anywhere — the page is decrypted in your browser.</p>
</main>
<script id="payload" type="application/json">${JSON.stringify(payload)}</script>
<script>
(function () {
  var P = JSON.parse(document.getElementById('payload').textContent);
  var f = document.getElementById('f'), err = document.getElementById('e');
  function b64(s) { return Uint8Array.from(atob(s), function (c) { return c.charCodeAt(0); }); }
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    err.hidden = true;
    var pass = document.getElementById('p').value;
    var enc = new TextEncoder();
    crypto.subtle.importKey('raw', enc.encode(pass), 'PBKDF2', false, ['deriveKey'])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: 'PBKDF2', salt: b64(P.kdf.salt), iterations: P.kdf.iterations,
            hash: P.kdf.hash },
          base, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      })
      .then(function (key) {
        return crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64(P.iv) }, key, b64(P.data));
      })
      .then(function (buf) {
        // Replace the whole document with the decrypted page. document.write is
        // the one reliable way to swap a full document including its <head>.
        var html = new TextDecoder().decode(buf);
        document.open(); document.write(html); document.close();
      })
      .catch(function () {
        // A wrong passphrase fails GCM authentication — indistinguishable from
        // tampering, and reported the same way.
        err.hidden = false;
        document.getElementById('p').select();
      });
  });
})();
</script>
</body>
</html>
`);

console.log(`Encrypted ${inPath} -> ${outPath} ` +
            `(${plaintext.length} bytes plaintext, PBKDF2 ${ITERATIONS} iters, AES-256-GCM)`);
