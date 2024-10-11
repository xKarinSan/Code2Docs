import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

import axios from "axios";
import { useEffect } from "react";
import {
    githubAppInstallURL,
    getGithubTokenURL,
    getGithubAppTokenURL,
} from "../../global/constants.ts";
import { useUserStore } from "../../store/userStore.ts";

function GithubRedirectPage() {
    const navigate = useNavigate();
    // auth token
    const currentUserAuthToken = useUserStore(
        (state: any) => state.githubAuthToken
    );
    const setUserAuthToken = useUserStore(
        (state: any) => state.setGithubAuthToken
    );
    // app token
    const currentUserAppToken = useUserStore(
        (state: any) => state.githubAppToken
    );
    const setUserAppToken = useUserStore(
        (state: any) => state.setGithubAppToken
    );
    // username (unique)
    const setUsername = useUserStore((state: any) => state.setGithubUsername);
    // profile pic url
    const setProfilePicUrl = useUserStore(
        (state: any) => state.setGithubProfilePicUrl
    );
    // displayname
    const setDisplayName = useUserStore(
        (state: any) => state.setGithubDisplayName
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
            // user token
            navigate("/home");
        }

        if (codeParam && !currentUserAuthToken) {
            const authenticateUser = async () => {
                await axios
                    .get(getGithubTokenURL + codeParam)
                    .then((res) => {
                        return res.data;
                    })
                    .then((data) => {
                        const {
                            access_token,
                            refresh_token,
                            app_install_jwt,
                            username,
                            display_name,
                            profile_pic_url,
                        } = data;
                        console.log("data", data);
                        setUserAuthToken(access_token);
                        setUsername(username);
                        setDisplayName(display_name);
                        setProfilePicUrl(profile_pic_url);
                        // Cookies.set(
                        //     "code2docs_github_auth_refresh_token",
                        //     refresh_token
                        // );
                        Cookies.set("code2docs_github_jwt", app_install_jwt);
                    })
                    .catch(() => {
                        navigate("/error");
                    });
            };
            authenticateUser();
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
                        console.log("data:", data);
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
