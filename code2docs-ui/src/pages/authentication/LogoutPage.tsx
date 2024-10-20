import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUserStore } from "../../store/userStore";
export default function LogoutPage() {
    const navigate = useNavigate();
    const removeUserToken = useUserStore(
        (state: any) => state.removeGithubAuthToken
    );
    const removeInstallationId = useUserStore(
        (state: any) => state.removeGithubInstallationId
    );
    const removeUsername = useUserStore(
        (state: any) => state.removeGithubUsername
    );
    const removeProfielPic = useUserStore(
        (state: any) => state.removeGithubProfilePicUrl
    );
    const removeDisplayName = useUserStore(
        (state: any) => state.removeGithubDisplayName
    );
    const logoutUser = () => {
        removeUserToken();
        removeInstallationId();
        removeUsername();
        removeProfielPic();
        removeDisplayName();
        navigate("/login");
    };
    useEffect(() => {
        logoutUser();
    }, []);
    return <div>Logging out ...</div>;
}
