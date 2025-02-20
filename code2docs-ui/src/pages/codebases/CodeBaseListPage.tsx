import { useEffect, useState } from "react";
import axios from "axios";
import { useUserStore } from "../../store/userStore";
import { type GithubRepoLink } from "../../global/types";
import { getUserGithubRepoURL } from "../../global/constants";
import {
    Badge,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
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
    Text,
} from "@chakra-ui/react";
import { FaAngleLeft, FaAngleRight } from "react-icons/fa";
import { NavLink } from "react-router-dom";

function CodeBaseListPage() {
    const githubUsername = useUserStore((state: any) => state.githubUsername);
    const githubAuthToken = useUserStore((state: any) => state.githubAuthToken);

    const [codebases, setCodebases] = useState<GithubRepoLink[]>();
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [pageCount, setPageCount] = useState<number>(0);

    const [repoCache, setRepoCache] = useState<
        Record<number, GithubRepoLink[]>
    >({});

    const getUserRepos = async () => {
        if (repoCache[pageNumber]) {
            setCodebases(repoCache[pageNumber]); // Load from cache
            return;
        }

        setIsLoading(true);
        try {
            const config = {
                headers: {
                    Authorization: `Bearer ${githubAuthToken}`,
                },
            };
            const res = await axios.get(
                `${getUserGithubRepoURL}${githubUsername.toLowerCase()}?page_num=${pageNumber}&per_page=10`,
                config
            );

            const { repos, pages_count } = res.data;
            setPageCount(pages_count);
            const githubRepos: GithubRepoLink[] = repos.map(
                ({ name, full_name, html_url, visibility }: any) => ({
                    displayName: name,
                    fullRepoName: full_name,
                    repoUrl: html_url,
                    visibility,
                })
            );

            setCodebases(githubRepos);
            setRepoCache((prevCache) => ({
                ...prevCache,
                [pageNumber]: githubRepos,
            }));
        } catch (error) {
            console.error("Error fetching repos:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const goToNextPage = () => {
        setPageNumber(pageNumber + 1 > pageCount ? pageCount : pageNumber + 1);
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
            <Breadcrumb>
                <BreadcrumbItem>
                    <NavLink to="/home">
                        <BreadcrumbLink>Home</BreadcrumbLink>
                    </NavLink>
                </BreadcrumbItem>
                <BreadcrumbItem>
                    <BreadcrumbLink>Codebases</BreadcrumbLink>
                </BreadcrumbItem>
            </Breadcrumb>
            <Card>
                <TableContainer>
                    <Table variant="simple">
                        <Thead>
                            <Th>Codebase Name</Th>
                            {/* <Th>Link</Th> */}
                            {/* <Th>Original URL</Th> */}
                        </Thead>
                        {!isLoading && codebases ? (
                            <>
                                <Tbody>
                                    {codebases.map(
                                        (codebase: GithubRepoLink) => {
                                            const {
                                                displayName,
                                                visibility,
                                                // repoUrl,
                                                fullRepoName,
                                            } = codebase;
                                            return (
                                                <>
                                                    <Tr>
                                                        <Td textAlign={"left"}>
                                                            <NavLink
                                                                to={
                                                                    "/codebases/" +
                                                                    fullRepoName
                                                                }
                                                            >
                                                                {displayName}
                                                            </NavLink>
                                                            <Badge
                                                                margin={2}
                                                                colorScheme={
                                                                    visibility ==
                                                                    "private"
                                                                        ? "red"
                                                                        : "green"
                                                                }
                                                            >
                                                                {visibility ==
                                                                "private"
                                                                    ? "Private"
                                                                    : "Public"}
                                                            </Badge>
                                                        </Td>
                                                    </Tr>
                                                </>
                                            );
                                        }
                                    )}
                                </Tbody>
                            </>
                        ) : (
                            <>
                                <Tbody>
                                    {isLoading ? (
                                        <Tr>
                                            <Td colSpan={3}>
                                                <Card
                                                    margin="5px auto"
                                                    padding="25px"
                                                    textAlign={"center"}
                                                >
                                                    Loading ...
                                                </Card>
                                            </Td>
                                        </Tr>
                                    ) : (
                                        <></>
                                    )}
                                </Tbody>
                            </>
                        )}
                    </Table>
                </TableContainer>

                <Stack direction="column" margin="5px auto">
                    <ButtonGroup>
                        <IconButton
                            background={"black"}
                            color={"white"}
                            isDisabled={pageNumber == 1}
                            aria-label="Previous Page"
                            size="lg"
                            icon={<FaAngleLeft />}
                            onClick={goToPreviousPage}
                        />
                        <Text margin="auto" width="50px" textAlign={"center"}>
                            {pageNumber}
                        </Text>
                        <IconButton
                            background={"black"}
                            color={"white"}
                            isDisabled={pageNumber == pageCount}
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
