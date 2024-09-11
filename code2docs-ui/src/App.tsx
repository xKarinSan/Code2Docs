import { Routes, Route, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import axios from "axios";
import { getGithubTokenURL } from "./constants.ts";
import "./main.css";

import { useUserStore } from "./store/userStore.ts";

// pages
import Homepage from "./pages/Homepage.tsx";
import RegistrationPage from "./pages/authentication/RegistrationPage.tsx";
import LoginPage from "./pages/authentication/LoginPage.tsx";
import ErrorPage from "./pages/authentication/ErrorPage.tsx";

function App() {
    const navigate = useNavigate();
    const currentUserToken = useUserStore((state: any) => state.githubAuthToken);
    const setUserToken = useUserStore((state:any) => state.setGithubAuthToken);

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
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
                            console.info(data.access_token)
                            setUserToken(data.access_token)

                            navigate("/home");
                        }
                    });
            };
            getAccessToken();
        }
        if (currentUserToken) {
            navigate("/home");
        }
    }, []);
    return (
        <>
            <Routes>
                <Route path="/error" element={<ErrorPage />} />
                <Route path="/home" element={<Homepage />} />
                <Route path="/register" element={<RegistrationPage />} />
                <Route path="/login" element={<LoginPage />} />
            </Routes>
        </>
    );
}

export default App;
