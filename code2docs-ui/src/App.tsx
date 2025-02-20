import { Routes, Route } from "react-router-dom";
import "./main.css";

// ================== pages ==================
// ======== auth ========
import RegistrationPage from "./pages/authentication/RegistrationPage.tsx";
import LoginPage from "./pages/authentication/LoginPage.tsx";
import ErrorPage from "./pages/authentication/ErrorPage.tsx";
import LogoutPage from "./pages/authentication/LogoutPage.tsx";
import GithubRedirectPage from "./pages/authentication/GithubRedirectPage.tsx";
// ======== codebases ========
import CodeBaseListPage from "./pages/codebases/CodeBaseListPage.tsx";
import IndividualCodebasePage from "./pages/codebases/IndividualCodebasePage.tsx";
// ======== documentation ========
import DocumentationListPage from "./pages/documentations/DocumentationListPage.tsx";
import IndividualDocumentationPage from "./pages/documentations/IndividualDocumentationPage.tsx";
// ======== user ========
import UserAccountPage from "./pages/user/UserAccountPage.tsx";

// ======== etc ========
import Landingpage from "./pages/Landingpage.tsx";
import Homepage from "./pages/Homepage.tsx";

function App() {
    return (
        <>
            <Routes>
                {/* authentication */}
                <Route path="/register" element={<RegistrationPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/error" element={<ErrorPage />} />
                <Route path="/logout" element={<LogoutPage />} />
                <Route path="/gh/redirect" element={<GithubRedirectPage />} />

                {/* codebases */}
                <Route path="/codebases" element={<CodeBaseListPage />} />
                <Route
                    path="/codebases/:username/:repository"
                    element={<IndividualCodebasePage />}
                />

                {/* documentations */}
                <Route
                    path="/documentations"
                    element={<DocumentationListPage />}
                />
                <Route
                    path="/documentations/:docset_id"
                    element={<IndividualDocumentationPage />}
                />

                {/* user */}
                <Route path="/profile" element={<UserAccountPage />} />

                {/* etc */}
                <Route path="/home" element={<Homepage />} />
                <Route path="/" element={<Landingpage />} />
            </Routes>
        </>
    );
}

export default App;
