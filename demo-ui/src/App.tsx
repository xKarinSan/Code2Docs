import { Routes, Route } from "react-router-dom";
import DemoPage from "./pages/DemoPage";
import "./main.css";
function App() {
    return (
        <>
            <Routes>
                <Route path="/demo" element={<DemoPage />} />
            </Routes>
        </>
    );
}

export default App;
