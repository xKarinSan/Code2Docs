import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import GlobalBar from "./components/global/Navbars/GlobalBar.tsx";

import { BrowserRouter } from "react-router-dom";

import { ChakraProvider, extendTheme, Heading } from "@chakra-ui/react";
import "@fontsource/open-sans";
import "@fontsource/raleway";

const theme = extendTheme({
    fonts: {
        heading: `'Open Sans', sans-serif`,
        body: `'Raleway', sans-serif`,
    },
    components: {
        Table: {
            variants: {
                simple: {
                    th: {
                        textTransform: "none",
                    },
                },
            },
        },
    },
});

createRoot(document.getElementById("root")!).render(
    // <StrictMode>
    <ChakraProvider theme={theme}>
        <BrowserRouter>
            <GlobalBar>
                <App />
            </GlobalBar>
        </BrowserRouter>
    </ChakraProvider>
    // </StrictMode>
);
