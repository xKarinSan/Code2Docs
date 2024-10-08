import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

export const useUserStore = create(
    persist(
        (set) => ({
            githubAuthToken: "",
            githubAppToken: "",
            githubUsername:"",
            githubProfilePictureUrl:"",
            githubDisplayName:"",

            setGithubAuthToken: (token: string) =>
                set({ githubAuthToken: token }),
            removeGithubAuthToken: () => set({ githubAuthToken: "" }),
            setGithubAppToken: (token: string) =>
                set({ githubAppToken: token }),
            removeGithubAppToken: () => set({ githubAppToken: "" }),
            
            setGithubUsername: (username: string) =>
                set({ githubUsername: username }),
            removeGithubUsername: () => set({ githubUsername: "" }),

            setGithubProfilePicUrl: (profilePicUrl: string) =>
                set({ githubProfilePictureUrl: profilePicUrl }),
            removeGithubProfilePicUrl: () => set({ githubProfilePictureUrl: "" }),

            setGithubDisplayName: (displayName: string) =>
                set({ githubDisplayName: displayName }),
            removeGithubDisplayName: () => set({ githubDisplayName: "" }),
        }),

        {
            name: "user-storage", // name of the item in the storage (must be unique)
            storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
        }
    )
);
