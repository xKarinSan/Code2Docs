import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
export default function LoginPage() {
    const navigate = useNavigate();
    const loginUser = () => {
        navigate("/");
    };

    return (
        <>
            <h1>Login Page</h1>
            <Button onClick={loginUser}>Login with github</Button>
        </>
    );
}
