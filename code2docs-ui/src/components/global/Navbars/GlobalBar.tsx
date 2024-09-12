import { ReactNode } from "react";
import { useUserStore } from "../../../store/userStore";
import LandingNavbar from "./LandingNavbar";
import UserSidebar from "./UserSidebar";

function GlobalBar({ children }: { children: ReactNode }) {
    const currentUserToken = useUserStore(
        (state: any) => state.githubAuthToken
    );
    return (
        <div>
            {currentUserToken ? (
                <>
                    <UserSidebar>{children}</UserSidebar>
                </>
            ) : (
                <>
                    <LandingNavbar>{children}</LandingNavbar>
                </>
            )}
        </div>
    );
}

export default GlobalBar;
