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
    Link,
    Text,
    Icon,
} from "@chakra-ui/react";
import { FaAngleLeft, FaAngleRight, FaExternalLinkAlt } from "react-icons/fa";
import { NavLink } from "react-router-dom";

function CodeBaseListPage() {
    const githubUsername = useUserStore((state: any) => state.githubUsername);
    const githubAuthToken = useUserStore((state: any) => state.githubAuthToken);

    const [codebases, setCodebases] = useState<GithubRepoLink[]>();
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [pageCount, setPageCount] = useState<number>(0);

    const getUserRepos = async () => {
        setIsLoading(true);
        const config = {
            headers: {
                Authorization: `Bearer ${githubAuthToken}`,
            },
        };
        await axios
            .get(
                `${getUserGithubRepoURL}${githubUsername.toLowerCase()}?page_num=${pageNumber}&per_page=30`,
                config
            )
            .then((res) => {
                return res.data;
            })
            .then((data: any) => {
                const { repos, pages_count } = data;
                setPageCount(pages_count);
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
                setIsLoading(false);
            });
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
                            <Th>Link</Th>
                            <Th>Original URL</Th>
                        </Thead>
                        {!isLoading && codebases ? (
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
                                                        <Td>
                                                            <NavLink
                                                                to={
                                                                    "/codebases/" +
                                                                    fullRepoName
                                                                }
                                                            >
                                                                {fullRepoName}
                                                            </NavLink>
                                                        </Td>
                                                        <Td>
                                                            <Link
                                                                href={repoUrl}
                                                                target="_blank"
                                                            >
                                                                Original Repo
                                                                Link
                                                                <Icon
                                                                    margin={
                                                                        "0 5px 0"
                                                                    }
                                                                    as={
                                                                        FaExternalLinkAlt
                                                                    }
                                                                />
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
