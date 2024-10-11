import { useEffect, useState } from "react";
import axios from "axios";
import { useUserStore } from "../../store/userStore";
import { type GithubRepoLink } from "../../global/types";
import { getUserGithubRepoURL } from "../../global/constants";
import {
    Card,
    Heading,
    TableContainer,
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    Link,
} from "@chakra-ui/react";
function CodeBaseListPage() {
    const githubUsername = useUserStore((state: any) => state.githubUsername);
    const githubAuthToken = useUserStore((state: any) => state.githubAuthToken);

    const [codebases, setCodebases] = useState<GithubRepoLink[]>();
    const getUserRepos = async (pageNumber: number = 3) => {
        const config = {
            headers: {
                Authorization: `Bearer ${githubAuthToken}`,
            },
        };
        console.log(`githubUsername ${githubUsername}`);
        console.log(
            `${getUserGithubRepoURL}${githubUsername}?page_num=${pageNumber}`
        );
        await axios
            .get(
                `${getUserGithubRepoURL}${githubUsername.toLowerCase()}?page_num=${pageNumber}`,
                config
            )
            .then((res) => {
                return res.data;
            })
            .then((data) => {
                const { repos } = data;
                let githubRepos: GithubRepoLink[] = [];
                repos.forEach((element: any) => {
                    const { name, full_name, html_url, visibility } = element;
                    githubRepos.push({
                        displayName: name,
                        fullRepoName: full_name,
                        repoUrl: html_url,
                        visibility,
                    });
                });
                console.log("repos", repos);
                setCodebases(githubRepos);
            });
    };

    useEffect(() => {
        getUserRepos();
    }, []);
    return (
        <div>
            <Heading>Codebases</Heading>
            <Card margin={5}>
                <TableContainer>
                    <Table variant="simple">
                        <Thead>
                            <Th>Codebase Name</Th>
                            <Th>Link</Th>
                            <Th>Original URL</Th>
                        </Thead>
                        {codebases ? (
                            <>
                                <Tbody>
                                    {codebases.map(
                                        (codebase: GithubRepoLink) => {
                                            const {
                                                displayName,
                                                visibility,
                                                repoUrl,
                                                fullRepoName,
                                            } = codebase;
                                            return (
                                                <>
                                                    <Tr>
                                                        <Td>
                                                            {displayName}{" "}
                                                            {visibility ==
                                                            "private"
                                                                ? "Private"
                                                                : "Public"}
                                                        </Td>
                                                        <Td>{fullRepoName}</Td>
                                                        <Td>
                                                            <Link
                                                                href={repoUrl}
                                                                target="_blank"
                                                            >
                                                                Original Repo
                                                            </Link>
                                                        </Td>
                                                    </Tr>
                                                </>
                                            );
                                        }
                                    )}
                                </Tbody>
                            </>
                        ) : (
                            <></>
                        )}
                    </Table>
                </TableContainer>
            </Card>
        </div>
    );
}

export default CodeBaseListPage;
