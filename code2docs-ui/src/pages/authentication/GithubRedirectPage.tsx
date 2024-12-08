import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useEffect } from "react";
import {
    githubAppInstallURL,
    getGithubInstallationCheck,
    getGithubTokenURL,
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
    // username (unique)
    const setUsername = useUserStore((state: any) => state.setGithubUsername);
    const username = useUserStore((state: any) => state.githubUsername);
    // profile pic url
    const setProfilePicUrl = useUserStore(
        (state: any) => state.setGithubProfilePicUrl
    );
    // displayname
    const setDisplayName = useUserStore(
        (state: any) => state.setGithubDisplayName
    );

    const setInstallationId = useUserStore(
        (state: any) => state.setGithubInstallationId
    );
    const installationId = useUserStore(
        (state: any) => state.githubInstallationId
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
        if (currentUserAuthToken) {
            // user token
            navigate("/home");
        }
        if (installationIdParam) {
            setInstallationId(installationIdParam);
        }
        console.log(codeParam)
        console.log(installationIdParam)
        console.log(currentUserAuthToken)

        if (codeParam && !currentUserAuthToken) {
            const authenticateUser = async () => {
                console.log("[authenticateUser]")
                await axios
                    .get(getGithubTokenURL + codeParam)
                    .then((res) => {
                        console.log("[res]",res)
                        return res.data;
                    })
                    .then((data) => {
                        console.log("[data]",data)
                        const {
                            access_token,
                            username,
                            display_name,
                            profile_pic_url,
                        } = data;
                        setUserAuthToken(access_token);
                        setUsername(username);
                        setDisplayName(display_name);
                        setProfilePicUrl(profile_pic_url);
                    })
                    .catch((e) => {
                        console.log("e",e)
                        navigate("/error");
                    });
            };
            authenticateUser();
        }
        if (!installationId || installationId == -1) {
            const confirmInstall = async () => {
                await axios
                    .get(getGithubInstallationCheck + username)
                    .then((res) => {
                        return res.data;
                    })
                    .then((data) => {
                        const { installation_id } = data;
                        if (installation_id == -1) {
                            window.location.assign(githubAppInstallURL);
                        } else {
                            setInstallationId(installation_id);
                            navigate("/home");
                        }
                    });
            };
            confirmInstall();
        }
        if (installationId != -1) {
            navigate("/home");
        }
    }, []);
    return <div></div>;
}

export default GithubRedirectPage;
