import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";


export const useUserStore = create(
    persist(
        (set) => ({
            githubAuthToken: "",
            userInstallationId:"",
            setGithubAuthToken: (token: string) =>
                set({ githubAuthToken: token }),
            removeGithubAuthToken: () => set({ githubAuthToken: "" }),

            setUserInstallationId: (token: string) =>
                set({ githubAuthToken: token }),
            removeInstallationId: () => set({ userInstallationId: "" }),
        }),
        
        {
            name: "user-storage", // name of the item in the storage (must be unique)
            storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
        }
    )
);
