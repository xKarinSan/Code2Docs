import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { githubAuthURL } from "../../constants";
export default function LoginPage() {
    const navigate = useNavigate();
    const loginUser = () => {
        // navigate("/");
        window.location.assign(githubAuthURL);
    };

    return (
        <>
            <h1>Login Page</h1>
            <Button onClick={loginUser}>Login with github</Button>
        </>
    );
}
