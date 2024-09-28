import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

import axios from "axios";
import { useEffect } from "react";
import {
    githubAppInstallURL,
    getGithubTokenURL,
    getGithubAppTokenURL,
} from "../../constants.ts";
import { useUserStore } from "../../store/userStore.ts";

function GithubRedirectPage() {
    const navigate = useNavigate();
    const currentUserAuthToken = useUserStore(
        (state: any) => state.githubAuthToken
    );
    const currentUserAppToken = useUserStore(
        (state: any) => state.githubAppToken
    );
    const currentUserAuthRefreshToken = useUserStore(
        (state: any) => state.githubAuthRefreshToken
    );
    const setUserAuthToken = useUserStore(
        (state: any) => state.setGithubAuthToken
    );
    const setUserAppToken = useUserStore(
        (state: any) => state.setGithubAppToken
    );
    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const installationIdParam = urlParams.get("installation_id");
        const codeParam = urlParams.get("code");
        const errorParam = urlParams.get("error");

        if (errorParam) {
            navigate("/error");
        }
        if (currentUserAppToken && currentUserAuthToken) {
            navigate("/home");
        }

        if (codeParam && !currentUserAuthToken) {
            const getAccessToken = async () => {
                await axios
                    .get(getGithubTokenURL + codeParam)
                    .then((res) => {
                        return res.data;
                    })
                    .then((data) => {
                        if (data.access_token) {
                            setUserAuthToken(data.access_token);
                        }
                        if (data.refresh_token) {
                            Cookies.set(
                                "code2docs_github_auth_refresh_token",
                                data.refresh_token
                            );
                        }
                    })
                    .catch(() => {
                        navigate("/error");
                    });
            };
            getAccessToken();
        }
        if (!currentUserAppToken) {
            window.location.assign(githubAppInstallURL);
        }
        if (installationIdParam && !currentUserAppToken) {
            const getAppAccessToken = async () => {
                await axios
                    .get(getGithubAppTokenURL + installationIdParam)
                    .then((res) => {
                        return res.data;
                    })
                    .then((data) => {
                        if (data.token) {
                            setUserAppToken(data.token);
                            navigate("/home");
                        }
                    })
                    .catch(() => {
                        navigate("/error");
                    });
            };
            getAppAccessToken();
        }
    }, []);
    return <div></div>;
}

export default GithubRedirectPage;
