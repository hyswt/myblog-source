function parseCookies(cookieHeader) {
  const out = {};
  if (!cookieHeader) return out;
  const pairs = cookieHeader.split(";");
  for (const pair of pairs) {
    const idx = pair.indexOf("=");
    if (idx === -1) continue;
    const key = pair.slice(0, idx).trim();
    const value = pair.slice(idx + 1).trim();
    out[key] = decodeURIComponent(value);
  }
  return out;
}

function htmlResponse(res, statusCode, html) {
  res.statusCode = statusCode;
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.end(html);
}

module.exports = async function handler(req, res) {
  const clientId = process.env.GITHUB_CLIENT_ID;
  const clientSecret = process.env.GITHUB_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    htmlResponse(res, 500, "<h1>Missing GitHub OAuth env vars</h1>");
    return;
  }

  const host = req.headers["x-forwarded-host"] || req.headers.host;
  const proto = req.headers["x-forwarded-proto"] || "https";
  const origin = `${proto}://${host}`;
  const redirectUri = `${origin}/api/callback`;

  const { code, state } = req.query || {};
  const cookies = parseCookies(req.headers.cookie);
  const cookieState = cookies.decap_oauth_state;

  if (!code || !state || !cookieState || state !== cookieState) {
    htmlResponse(res, 400, "<h1>Invalid OAuth state</h1>");
    return;
  }

  try {
    const tokenResp = await fetch("https://github.com/login/oauth/access_token", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code,
        redirect_uri: redirectUri,
        state,
      }),
    });

    const data = await tokenResp.json();
    if (!data.access_token) {
      htmlResponse(res, 400, `<h1>OAuth failed</h1><pre>${JSON.stringify(data)}</pre>`);
      return;
    }

    res.setHeader(
      "Set-Cookie",
      "decap_oauth_state=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0"
    );

    const payload = JSON.stringify({ token: data.access_token, provider: "github" });
    const safePayload = payload.replace(/</g, "\\u003c");

    htmlResponse(
      res,
      200,
      `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Decap CMS OAuth</title>
  </head>
  <body>
    <script>
      (function () {
        var message = "authorization:github:success:" + '${safePayload}';
        if (window.opener) {
          window.opener.postMessage(message, window.location.origin);
        }
        window.close();
      })();
    </script>
    <p>Authentication complete. You can close this window.</p>
  </body>
</html>`
    );
  } catch (err) {
    htmlResponse(res, 500, `<h1>OAuth exception</h1><pre>${String(err)}</pre>`);
  }
};
