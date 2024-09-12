import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";


export const useUserStore = create(
    persist(
        (set) => ({
            githubAuthToken: "",
            setGithubAuthToken: (token: string) =>
                set({ githubAuthToken: token }),
            removeGithubAuthToken: () => set({ githubAuthToken: "" }),
        }),
        {
            name: "user-storage", // name of the item in the storage (must be unique)
            storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
        }
    )
);
