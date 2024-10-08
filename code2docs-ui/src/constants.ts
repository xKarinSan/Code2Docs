const githubAuthClientId = import.meta.env.VITE_GITHUB_CLIENT_ID;
const githubAuthURL = `https://github.com/login/oauth/authorize?client_id=${githubAuthClientId}`;
const githubAppInstallURL = `https://github.com/apps/${import.meta.env.VITE_GITHUB_APP_APP_NAME}/installations/new`;
const backendURL = import.meta.env.VITE_API_URL;
const getGithubTokenURL = backendURL + "/gh/login/?code=";
const getGithubAppTokenURL = backendURL + "/gh/install/?installation_id=";

export { githubAuthURL, getGithubTokenURL, githubAppInstallURL ,getGithubAppTokenURL};
