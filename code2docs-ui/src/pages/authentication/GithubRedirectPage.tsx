import { useNavigate } from "react-router-dom";

import axios from "axios";
import React from "react";
import { useEffect } from "react";
import { githubAppInstallURL, getGithubTokenURL,getGithubAppTokenURL } from "../../constants.ts";
import { useUserStore } from "../../store/userStore.ts";

function GithubRedirectPage() {
    const navigate = useNavigate();
    const currentUserToken = useUserStore(
        (state: any) => state.githubAuthToken
    );
    const setUserToken = useUserStore((state: any) => state.setGithubAuthToken);
    const setUserInstallationId = useUserStore((state: any) => state.setGsetUserInstallationIdit);

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const installationIdParam = urlParams.get("installation_id");
        const codeParam = urlParams.get("code");
        const errorParam = urlParams.get("error");
        if (errorParam) {
            navigate("/error");
        }

        if (codeParam && !currentUserToken) {
            const getAccessToken = async () => {
                await axios
                    .get(getGithubTokenURL + codeParam)
                    .then((res) => {
                        return res.data;
                    })
                    .then((data) => {
                        if (data.access_token) {
                            console.info(data.access_token);
                            setUserToken(data.access_token);

                            // navigate("/home");
                        }
                    });
            };
            getAccessToken();
            window.location.assign(githubAppInstallURL);
        }
        if (installationIdParam) {
            const getAppAccessToken = async () => {
                await axios
                    .get(getGithubAppTokenURL + installationIdParam)
                    .then((res) => {
                        return res.data;
                    })
                    .then((data) => {
                        if (data.access_token) {
                            console.info(data.access_token);
                            (data.access_token);

                            // navigate("/home");
                        }
                    });
            };
            getAppAccessToken();
        }
        // if (currentUserToken) {
        // }
        // console.log("githubAppInstallURL", githubAppInstallURL);
        // window.location.assign(githubAppInstallURL);
    }, []);
    return <div></div>;
}

export default GithubRedirectPage;
