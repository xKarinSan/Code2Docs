import { Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import Homepage from "./pages/Homepage.tsx";
import RegistrationPage from "./pages/authentication/RegistrationPage.tsx";
import LoginPage from "./pages/authentication/LoginPage.tsx";
import axios from "axios";
import { getGithubTokenURL } from "./constants.ts";

function App() {
    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const codeParam = urlParams.get("code");
        if (codeParam && !localStorage.getItem("githubAccessToken")) {
            const getAccessToken = async () => {
                await axios
                    .get(getGithubTokenURL + codeParam)
                    .then((res) => {
                        return res.data;
                    })
                    .then((data) => {
                        if (data.access_token) {
                            localStorage.setItem(
                                "githubAccessToken",
                                data.access_token
                            );
                        }
                    });
            };
            getAccessToken();
        }
    });
    return (
        <>
            <Routes>
                <Route path="/" element={<Homepage />} />
                <Route path="/register" element={<RegistrationPage />} />
                <Route path="/login" element={<LoginPage />} />
            </Routes>
        </>
    );
}

export default App;
