import { useEffect, useState } from "react";
import axios from "axios";
import { useUserStore } from "../../store/userStore";

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
} from "@chakra-ui/react";
function CodeBaseListPage() {
    const githubUsername = useUserStore((state: any) => state.githubUsername);
    const githubAuthToken = useUserStore((state: any) => state.githubAuthToken);

    const [codebases, setCodebases] = useState([]);
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
                console.log(`Repos`, repos);
                setCodebases(repos);
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
                            <Th> Link</Th>
                        </Thead>
                        {codebases ? (
                            <>
                                <Tbody>
                                    {codebases.map((codebase) => {
                                        const { name, private: isPrivate } =
                                            codebase;
                                        return (
                                            <>
                                                <Tr>
                                                    <Td>
                                                        {name}{" "}
                                                        {isPrivate
                                                            ? "Private"
                                                            : "Public"}
                                                    </Td>
                                                    <Td></Td>
                                                </Tr>
                                            </>
                                        );
                                    })}
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
