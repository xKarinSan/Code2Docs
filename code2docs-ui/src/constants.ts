const githubAuthClientId = import.meta.env.VITE_GITHUB_CLIENT_ID;
const githubAuthURL = `https://github.com/login/oauth/authorize?client_id=${githubAuthClientId}`;
const backendURL = import.meta.env.VITE_API_URL;

const getGithubTokenURL = backendURL + "/gh/getAccessToken/?code=";

export { githubAuthURL, getGithubTokenURL };
