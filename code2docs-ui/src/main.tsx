import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import GlobalBar from "./components/global/Navbars/GlobalBar.tsx";

import { BrowserRouter } from "react-router-dom";

import { ChakraProvider } from "@chakra-ui/react";

createRoot(document.getElementById("root")!).render(
    // <StrictMode>
    <ChakraProvider>
        <BrowserRouter>
            <GlobalBar>
                <App />
            </GlobalBar>
        </BrowserRouter>
    </ChakraProvider>
    // </StrictMode>
);
