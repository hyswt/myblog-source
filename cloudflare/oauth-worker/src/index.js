function randomState() {
  const arr = new Uint8Array(16);
  crypto.getRandomValues(arr);
  return Array.from(arr, (b) => b.toString(16).padStart(2, "0")).join("");
}

function html(body) {
  return new Response(body, {
    status: 200,
    headers: { "content-type": "text/html; charset=utf-8" },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) {
      return new Response("Missing GitHub OAuth env vars", { status: 500 });
    }

    if (url.pathname === "/auth") {
      const state = randomState();
      const redirectUri = `${url.origin}/callback`;
      const authorize = new URL("https://github.com/login/oauth/authorize");
      authorize.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
      authorize.searchParams.set("redirect_uri", redirectUri);
      authorize.searchParams.set("scope", "repo");
      authorize.searchParams.set("state", state);

      const headers = new Headers();
      headers.set("location", authorize.toString());
      headers.append(
        "set-cookie",
        `decap_oauth_state=${state}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=600`
      );
      return new Response(null, { status: 302, headers });
    }

    if (url.pathname === "/callback") {
      const code = url.searchParams.get("code");
      const state = url.searchParams.get("state");
      const cookie = request.headers.get("cookie") || "";
      const stateCookie = cookie
        .split(";")
        .map((v) => v.trim())
        .find((v) => v.startsWith("decap_oauth_state="))
        ?.split("=")[1];

      if (!code || !state || !stateCookie || state !== stateCookie) {
        return html("<h1>Invalid OAuth state</h1>");
      }

      const redirectUri = `${url.origin}/callback`;
      const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "content-type": "application/json",
        },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code,
          redirect_uri: redirectUri,
          state,
        }),
      });

      const tokenData = await tokenRes.json();
      if (!tokenData.access_token) {
        return html(`<h1>OAuth failed</h1><pre>${JSON.stringify(tokenData)}</pre>`);
      }

      const payload = JSON.stringify({
        token: tokenData.access_token,
        provider: "github",
      }).replace(/</g, "\\u003c");

      return new Response(
        `<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Decap OAuth</title></head>
  <body>
    <script>
      (function () {
        var message = "authorization:github:success:" + '${payload}';
        if (window.opener) {
          window.opener.postMessage(message, window.location.origin);
        }
        window.close();
      })();
    </script>
    <p>Authentication complete. You can close this window.</p>
  </body>
</html>`,
        {
          status: 200,
          headers: {
            "content-type": "text/html; charset=utf-8",
            "set-cookie":
              "decap_oauth_state=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0",
          },
        }
      );
    }

    return new Response("Not Found", { status: 404 });
  },
};
