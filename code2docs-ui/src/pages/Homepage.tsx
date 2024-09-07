import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
export default function Homepage() {
    const navigate = useNavigate();
    const logoutUser = () => {
        navigate("/login");
    };
    return (
        <>
            <h3>Home Page</h3>
            <Button onClick={logoutUser}>Logout</Button>
        </>
    );
}
