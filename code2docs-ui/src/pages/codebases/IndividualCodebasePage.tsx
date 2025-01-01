import {
    Card,
    Heading,
    Box,
    Grid,
    GridItem,
    Button,
    useToast,
    Breadcrumb,
    BreadcrumbItem,
    Text,
    Image,
    BreadcrumbLink,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    useDisclosure,
} from "@chakra-ui/react";
import JSZip from "jszip";
import Lottie from "lottie-react";
import writing from "../../assets/writing.json";
import axios from "axios";

import { useEffect, useState } from "react";
import { NavLink, useParams, useNavigate } from "react-router-dom";
import { FileNode, buildFileTree } from "../../helpers/FileNode";
import { FileTree } from "../../components/documentation/FileTree";
import { useUserStore } from "../../store/userStore";
import { CodeBlock } from "react-code-blocks";
import { FaPencilAlt } from "react-icons/fa";

import imageUploadImg from "../../assets/image-upload-concept-landing-page.png";
import selectFileImg from "../../assets/search-concept-yellow-folder-magnifier-icons-hand-drawn-cartoon-art-illustration.png";
import { getUserGithubRepoZippedURL } from "../../global/constants";

function IndividualCodebasePage() {
    const navigate = useNavigate();
    const { isOpen, onOpen, onClose } = useDisclosure();
    const githubAuthToken = useUserStore((state: any) => state.githubAuthToken);
    const githubInstallationId = useUserStore(
        (state: any) => state.githubInstallationId
    );

    const codebaseInfo = useParams();
    const [repoName, setRepoName] = useState<string | undefined>("");

    const [isLoading, setIsLoading] = useState(true);
    const toast = useToast({
        duration: 5000,
        isClosable: true,
        position: "top",
    });
    const [fileTree, setFileTree] = useState<FileNode | null>(null);
    const [currentReadFile, setCurrentReadFile] = useState<FileNode | null>(
        null
    );
    const [currentReadFilePath, setCurrentReadFilePath] = useState<string>("");
    const [currentReadDirectory, setCurrentReadDirectory] =
        useState<FileNode | null>(null);

    const loadCodebaseContents = async () => {
        try {
            const { username, repository } = codebaseInfo;
            setRepoName(repository);
            await fetch(
                `${getUserGithubRepoZippedURL}${username}/${repository}`,
                {
                    headers: {
                        authorization: `Bearer ${githubAuthToken}`,
                    },
                }
            ).then(async (res) => {
                console.log("res", res);
                if (!res.ok) {
                    toast({
                        title: "Loading failed.",
                        status: "error",
                    });
                }
                const reader = res.body?.getReader();
                const dataArr: Uint8Array[] = [];
                while (true) {
                    if (reader) {
                        const { done, value } = await reader.read();
                        if (done) break;
                        console.log(value);
                        dataArr.push(value);
                    }
                }
                // turn it into zip
                const zip = new JSZip();
                const blob = new Blob(dataArr);
                console.log("blob", blob);

                // Load the generated zip file
                const contents = await zip.loadAsync(blob);
                const extractedFiles = [];
                for (const [filename, fileData] of Object.entries(
                    contents.files
                )) {
                    if (!fileData.dir) {
                        const content = await fileData.async("binarystring");
                        extractedFiles.push({ filename, content });
                    }
                }
                const tree = buildFileTree(extractedFiles);
                setFileTree(tree);
                toast({
                    title: "Codebase uploaded!",
                    status: "success",
                });
                setIsLoading(false);
            });
        } catch (e) {
            console.log("E", e);
            toast({
                title: "Loading failed.",
                status: "error",
            });
            setIsLoading(false);
        }
    };
    useEffect(() => {
        // load the codebase
        loadCodebaseContents();
        console.log(codebaseInfo);
    }, []);
    const createZipFile = async () => {
        const zip = new JSZip();
        const addToZip = (node: FileNode, currentPath: string = "") => {
            const newPath = currentPath
                ? `${currentPath}/${node.name}`
                : node.name;

            if (node.isDirectory) {
                // Create a folder in the zip
                zip.folder(newPath);

                // Recursively add children
                node.children.forEach((child) => addToZip(child, newPath));
            } else {
                // Add file to the zip
                zip.file(newPath, node.content || "");
            }
        };

        // Start with the root node (currentReadDirectory)
        if (currentReadDirectory) {
            addToZip(currentReadDirectory);
        }

        // Generate the zip file
        const content = await zip.generateAsync({ type: "blob" });
        return content;
    };
    const generateDocumentation = async () => {
        if (!currentReadDirectory) {
            toast({
                title: "Please select a folder!",
                status: "error",
            });
            return;
        }
        onOpen();
        const zipBlob = await createZipFile();
        const formData = new FormData();
        // use axios
        formData.append("file", zipBlob, `${currentReadDirectory.name}.zip`);
        await axios
            .post(
                `${
                    import.meta.env.VITE_API_URL
                }/docgen/upload/${githubInstallationId}`,
                formData
            )
            .then((res) => {
                const { docset_id } = res.data;
                onClose();
                navigate(`/documentations/${docset_id}`);
            })
            .catch(() => {
                onClose();
                toast({
                    title: "Failed to create documentation!",
                    status: "error",
                });
            });
        toast({
            title: "Documentation successfully created!",
            status: "success",
        });
    };

    return (
        <>
            {" "}
            {isLoading ? (
                <>Loading ...</>
            ) : (
                <>
                    {" "}
                    <Box margin="auto" overflow={"scroll"}>
                        <Heading margin={5} textAlign={"center"}>
                            {repoName}
                        </Heading>
                        <Breadcrumb>
                            <BreadcrumbItem>
                                <NavLink to="/home">
                                    <BreadcrumbLink>Home</BreadcrumbLink>
                                </NavLink>
                            </BreadcrumbItem>
                            <BreadcrumbItem>
                                <BreadcrumbLink>{repoName}</BreadcrumbLink>
                            </BreadcrumbItem>
                        </Breadcrumb>
                        <Grid
                            gridTemplateColumns={"49% 49%"}
                            justifyContent={"space-between"}
                            gap={1}
                        >
                            <GridItem>
                                <Card
                                    height="700px"
                                    width="100%"
                                    overflow={"scroll"}
                                >
                                    {fileTree ? (
                                        <Box
                                            overflow="scroll"
                                            height="600px"
                                            width="100%"
                                        >
                                            <FileTree
                                                node={fileTree}
                                                setReadFile={setCurrentReadFile}
                                                setReadFilePath={
                                                    setCurrentReadFilePath
                                                }
                                                setReadDirectory={
                                                    setCurrentReadDirectory
                                                }
                                                currentReadFilePath={
                                                    currentReadFilePath
                                                }
                                                currentReadDirectory={
                                                    currentReadDirectory
                                                }
                                            />
                                        </Box>
                                    ) : (
                                        <Box
                                            display="grid"
                                            fontSize={"18px"}
                                            margin="auto"
                                            textAlign={"center"}
                                        >
                                            <Image
                                                src={imageUploadImg}
                                                alt={
                                                    "Image by pikisuperstar on Freepik. Souce: https://www.freepik.com/free-vector/image-upload-concept-landing-page_5337069.htm#fromView=search&page=1&position=1&uuid=1cc93512-6c6d-4455-acb0-2c9815533841"
                                                }
                                                width={{
                                                    base: "100px",
                                                    sm: "150px",
                                                    md: "200px",
                                                    lg: "300px",
                                                    xl: "400px",
                                                }}
                                            />
                                            Upload your code
                                        </Box>
                                    )}
                                    <Box background="#f7f8fa">
                                        <Grid gap={2} padding="10px">
                                            <GridItem
                                                margin="10px"
                                                alignSelf={"center"}
                                                overflow="scroll"
                                            >
                                                <b>Selected Folder: </b>
                                                {currentReadDirectory
                                                    ? currentReadDirectory.name
                                                    : ""}
                                            </GridItem>
                                            <GridItem margin="10px">
                                                <Button
                                                    leftIcon={<FaPencilAlt />}
                                                    background="#2809E3"
                                                    color="white"
                                                    borderRadius={5}
                                                    size="md"
                                                    onClick={
                                                        generateDocumentation
                                                    }
                                                >
                                                    Write Docs
                                                </Button>
                                            </GridItem>
                                        </Grid>
                                    </Box>
                                </Card>
                            </GridItem>
                            <GridItem>
                                <Card
                                    height="700px"
                                    width="100%"
                                    overflow={"scroll"}
                                >
                                    {currentReadFile ? (
                                        <Box>
                                            <Box
                                                background="#2809E3"
                                                color="white"
                                            >
                                                <Text
                                                    padding="10px"
                                                    overflow={"scroll"}
                                                    marginBottom={"5px"}
                                                >
                                                    {currentReadFilePath ||
                                                        "Select a file"}
                                                </Text>
                                            </Box>
                                            <Box
                                                height="600px"
                                                overflow={"scroll"}
                                            >
                                                <CodeBlock
                                                    text={
                                                        currentReadFile?.content
                                                    }
                                                    showLineNumbers={true}
                                                />
                                            </Box>
                                        </Box>
                                    ) : (
                                        <Box
                                            display="grid"
                                            fontSize={"18px"}
                                            margin="10px auto"
                                            textAlign={"center"}
                                        >
                                            <Image
                                                src={selectFileImg}
                                                alt={
                                                    "Image by mamewmy on Freepik. Souce: https://www.freepik.com/free-vector/search-concept-yellow-folder-magnifier-icons-hand-drawn-cartoon-art-illustration_18508166.htm#fromView=search&page=1&position=16&uuid=60aa9ddc-3696-44c7-98d3-ff85fdf748aa"
                                                }
                                                width={{
                                                    base: "100px",
                                                    sm: "150px",
                                                    md: "200px",
                                                    lg: "300px",
                                                    xl: "400px",
                                                }}
                                            />
                                            Select a file
                                        </Box>
                                    )}
                                </Card>
                            </GridItem>
                        </Grid>
                        <Modal
                            isOpen={isOpen}
                            onClose={onClose}
                            closeOnOverlayClick={false}
                        >
                            <ModalOverlay />
                            <ModalContent>
                                <ModalHeader>
                                    Writing in progress ...
                                </ModalHeader>
                                <ModalBody pb={6}>
                                    <Lottie
                                        animationData={writing}
                                        loop={true}
                                    />
                                </ModalBody>
                            </ModalContent>
                        </Modal>
                    </Box>
                </>
            )}
        </>
    );
}

export default IndividualCodebasePage;
