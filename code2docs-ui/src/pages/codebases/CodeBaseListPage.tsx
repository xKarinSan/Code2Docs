import { useEffect, useState } from "react";
import axios from "axios";
import { useUserStore } from "../../store/userStore";

import { getUserGithubRepoURL } from "../../constants";
function CodeBaseListPage() {
    const githubUsername = useUserStore((state: any) => state.githubUsername);
    const githubAppToken = useUserStore((state: any) => state.githubAppToken);

    const [codebases, setCodebases] = useState([]);
    const getUserRepos = async (pageNumber: number = 1) => {
        const config = {
            headers: {
                Authorization: `Bearer ${githubAppToken}`,
            },
        };
        console.log(`githubUsername ${githubUsername}`);
        await axios
            .get(
                `${getUserGithubRepoURL}${githubUsername}?page_num=${pageNumber}`,
                config
            )
            .then((res) => {
                return res.data;
            })
            .then((data) => {
                const { repos } = data;
                console.log(`Repos`, repos);
                setCodebases(repos);
            });
    };

    useEffect(() => {
        getUserRepos();
    }, []);
    return <div>Codebases</div>;
}

export default CodeBaseListPage;
