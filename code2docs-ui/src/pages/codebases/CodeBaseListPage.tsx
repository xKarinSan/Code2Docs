import { useEffect, useState } from "react";
import axios from "axios";
import { useUserStore } from "../../store/userStore";
import { type GithubRepoLink } from "../../global/types";
import { getUserGithubRepoURL } from "../../global/constants";
import {
    ButtonGroup,
    IconButton,
    Card,
    Heading,
    Stack,
    TableContainer,
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    Link,
    Text,
} from "@chakra-ui/react";
import { FaAngleLeft, FaAngleRight } from "react-icons/fa";

function CodeBaseListPage() {
    const githubUsername = useUserStore((state: any) => state.githubUsername);
    const githubAuthToken = useUserStore((state: any) => state.githubAuthToken);
    const [codebases, setCodebases] = useState<GithubRepoLink[]>();
    const [pageNumber, setPageNumber] = useState<number>(1);
    const getUserRepos = async () => {
        const config = {
            headers: {
                Authorization: `Bearer ${githubAuthToken}`,
            },
        };
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
                setCodebases(githubRepos);
            });
    };

    const goToNextPage = () => {
        setPageNumber(pageNumber + 1);
    };
    const goToPreviousPage = () => {
        setPageNumber(pageNumber - 1 < 1 ? 1 : pageNumber - 1);
    };
    useEffect(() => {
        getUserRepos();
    }, [pageNumber]);
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
                <Stack direction="column" margin="auto">
                    <ButtonGroup>
                        <IconButton
                            colorScheme="teal"
                            aria-label="Previous Page"
                            size="lg"
                            icon={<FaAngleLeft />}
                            onClick={goToPreviousPage}
                        />
                        <Text margin="auto" width="50px" textAlign={"center"}>
                            {pageNumber}
                        </Text>
                        <IconButton
                            colorScheme="teal"
                            aria-label="Next Page"
                            size="lg"
                            icon={<FaAngleRight />}
                            onClick={goToNextPage}
                        />
                    </ButtonGroup>
                </Stack>
            </Card>
        </div>
    );
}

export default CodeBaseListPage;
