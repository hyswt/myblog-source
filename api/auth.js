function randomState() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

module.exports = async function handler(req, res) {
  const clientId = process.env.GITHUB_CLIENT_ID;
  if (!clientId) {
    res.status(500).send("Missing GITHUB_CLIENT_ID");
    return;
  }

  const host = req.headers["x-forwarded-host"] || req.headers.host;
  const proto = req.headers["x-forwarded-proto"] || "https";
  const origin = `${proto}://${host}`;
  const redirectUri = `${origin}/api/callback`;
  const state = randomState();

  res.setHeader(
    "Set-Cookie",
    `decap_oauth_state=${state}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=600`
  );

  const scope = encodeURIComponent("repo");
  const authorizeUrl =
    `https://github.com/login/oauth/authorize?client_id=${encodeURIComponent(clientId)}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&scope=${scope}` +
    `&state=${encodeURIComponent(state)}`;

  res.writeHead(302, { Location: authorizeUrl });
  res.end();
};
