import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
export default function RegistrationPage() {
    const navigate = useNavigate();
    const registerUser = () => {
        navigate("/");
    };

    return (
        <>
            <h3>Registration Page</h3>
            <Button onClick={registerUser}>Register with github</Button>
        </>
    );
}
