import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

export const useUserStore = create(
    persist(
        (set) => ({
            githubAuthToken: "",
            githubAppToken: "",
            setGithubAuthToken: (token: string) =>
                set({ githubAuthToken: token }),
            removeGithubAuthToken: () => set({ githubAuthToken: "" }),

            setGithubAppToken: (token: string) =>
                set({ githubAppToken: token }),
            removeGithubAppToken: () => set({ githubAppToken: "" }),
        }),

        {
            name: "user-storage", // name of the item in the storage (must be unique)
            storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
        }
    )
);
