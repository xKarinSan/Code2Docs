import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

import { useUserStore } from "../store/userStore";

export default function Homepage() {
    const navigate = useNavigate();
    const removeUserToken = useUserStore((state:any) => state.removeGithubAuthToken);
    const logoutUser = () => {
        removeUserToken();
        navigate("/login");
    };
    return (
        <>
            <h3>Home Page</h3>
            <Button onClick={logoutUser}>Logout</Button>
        </>
    );
}
