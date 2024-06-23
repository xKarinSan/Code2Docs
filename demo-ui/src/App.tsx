import { Routes, Route } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import BrowsePage from "./pages/BrowsePage";
import "./main.css"
function App() {
    return (
        <>
            <Routes>
                <Route path="/upload" element={<UploadPage />} />
                <Route path="/browse" element={<BrowsePage />} />
            </Routes>
        </>
    );
}

export default App;
