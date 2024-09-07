import { Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import Homepage from "./pages/Homepage.tsx";
import RegistrationPage from "./pages/authentication/RegistrationPage.tsx";
import LoginPage from "./pages/authentication/LoginPage.tsx";

function App() {
    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const codeParam = urlParams.get("code");
        if (codeParam) {
            localStorage.setItem("githubAuthCode", codeParam);
            // call the token endpoint
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
