import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "../../store/userStore";
export default function LogoutPage() {
    const navigate = useNavigate();
    const removeUserToken = useUserStore(
        (state: any) => state.removeGithubAuthToken
    );
    const logoutUser = () => {
        removeUserToken();
        navigate("/login");
    };
    useEffect(() => {
        logoutUser();
    }, []);
    return <div>Logging out ...</div>;
}
