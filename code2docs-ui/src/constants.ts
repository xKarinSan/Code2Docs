const githubAuthClientId = import.meta.env.VITE_GITHUB_CLIENT_ID;
const githubAuthURL = `https://github.com/login/oauth/authorize?client_id=${githubAuthClientId}`;

export { githubAuthURL };
