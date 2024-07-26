import {
    ButtonGroup,
    Card,
    Heading,
    Input,
    Box,
    Grid,
    GridItem,
    Button,
    useToast,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    useDisclosure,
    Text,
    Image,
    FormLabel,
} from "@chakra-ui/react";

import JSZip from "jszip";
import { useRef, useState } from "react";
import { FileNode, buildFileTree } from "../helpers/FileNode";
import { FileTree } from "../components/global/FileTree";
import axios from "axios";

import Lottie from "lottie-react";
import writing from "../assets/writing.json";
import MarkdownEditor from "@uiw/react-markdown-editor";
import { CodeBlock } from "react-code-blocks";
import { DownloadIcon, DeleteIcon } from "@chakra-ui/icons";
import { FaPencilAlt } from "react-icons/fa";

import imageUploadImg from "../assets/image-upload-concept-landing-page.png";
import selectFileImg from "../assets/search-concept-yellow-folder-magnifier-icons-hand-drawn-cartoon-art-illustration.png";

export default function DemoPage() {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const zip = new JSZip();
    const toast = useToast({
        duration: 5000,
        isClosable: true,
        position: "top",
    });
    const fileInputRef = useRef<HTMLInputElement | null>(null);
    const [fileTree, setFileTree] = useState<FileNode | null>(null);
    const [currentReadFile, setCurrentReadFile] = useState<FileNode | null>(
        null
    );
    const [currentReadFilePath, setCurrentReadFilePath] = useState<string>("");
    const [currentReadDirectory, setCurrentReadDirectory] =
        useState<FileNode | null>(null);
    const [markdownDocumentation, setMarkdownDocumentation] = useState("");
    const [markdownName, setMarkdownName] = useState("");

    const selectFile = async (files: FileList | null) => {
        if (files) {
            const contents = await zip.loadAsync(files[0]);

            const extractedFiles = [];
            for (const [filename, fileData] of Object.entries(contents.files)) {
                if (!fileData.dir) {
                    const content = await fileData.async("binarystring");
                    extractedFiles.push({ filename, content });
                }
            }
            const tree = buildFileTree(extractedFiles);
            setFileTree(tree);
            toast({
                title: "File uploaded!",
                status: "success",
            });
        }
    };

    const createZipFile = async () => {
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
        formData.append("file", zipBlob, "archive.zip");
        await axios
            .post(`${import.meta.env.VITE_API_URL}/demo`, formData)
            .then((res) => {
                onClose();
                setMarkdownDocumentation(res.data.data);
                toast({
                    title: "Documentation successfully created!",
                    status: "success",
                });
            })
            .catch(() => {
                onClose();
                toast({
                    title: "Failed to create documentation!",
                    status: "error",
                });
            });
    };

    const downloadDocumentation = () => {
        const blob = new Blob([markdownDocumentation], {
            type: "text/markdown",
        });

        // Step 3: Create a download link for the Blob
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${markdownName || "readme"}.md`;

        // Append the link to the body (necessary for Firefox)
        document.body.appendChild(link);

        // Trigger the download
        link.click();

        // Clean up
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    const removeFile = () => {
        if (fileInputRef.current) {
            fileInputRef.current!.value = "";
        }
        setFileTree(null);
        setCurrentReadDirectory(null);
        setCurrentReadFile(null);
        setCurrentReadFilePath("");
        toast({
            title: "File removed!",
            status: "info",
        });
    };

    return (
        <Box
            width={{
                base: "100%",
                md: "80%",
            }}
            margin="auto"
            overflow={"scroll"}
        >
            <Heading textAlign={"center"}>Demo</Heading>
            <Card margin="10px auto">
                <Grid
                    templateColumns={{
                        base: "repeat(1,1fr)",
                        md: "repeat(2,1fr)",
                    }}
                    width={"fit-content"}
                >
                    <GridItem margin="10px">
                        <Input
                            id="file-upload"
                            ref={fileInputRef}
                            width="fit-content"
                            type="file"
                            accept=".zip"
                            multiple={true}
                            onChange={(e) => {
                                selectFile(e.target.files);
                            }}
                            display="none"
                        />
                        <FormLabel
                            color="white"
                            padding="9px"
                            borderRadius="5px"
                            background="#684FFB"
                            htmlFor="file-upload"
                            width="fit-content"
                            cursor="pointer"
                            margin="0"
                        >
                            <DownloadIcon marginRight={"10px"} />
                            Upload code (.zip only)
                        </FormLabel>
                    </GridItem>
                    <GridItem margin="10px">
                        <Button
                            leftIcon={<DeleteIcon />}
                            colorScheme="red"
                            borderRadius={5}
                            size="md"
                            onClick={removeFile}
                            margin="0"
                        >
                            Remove Codebase
                        </Button>
                    </GridItem>
                </Grid>
            </Card>
            <Grid
                gridTemplateColumns={"49% 49%"}
                justifyContent={"space-between"}
                gap={1}
            >
                <GridItem>
                    <Card height="700px" width="100%" overflow={"scroll"}>
                        {fileTree ? (
                            <Box overflow="scroll" height="600px" width="100%">
                                <FileTree
                                    node={fileTree}
                                    setReadFile={setCurrentReadFile}
                                    setReadFilePath={setCurrentReadFilePath}
                                    setReadDirectory={setCurrentReadDirectory}
                                    currentReadFilePath={currentReadFilePath}
                                    currentReadDirectory={currentReadDirectory}
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
                                        colorScheme="purple"
                                        borderRadius={5}
                                        size="md"
                                        onClick={generateDocumentation}
                                    >
                                        Write Docs
                                    </Button>
                                </GridItem>
                            </Grid>
                        </Box>
                    </Card>
                </GridItem>
                <GridItem>
                    <Card height="700px" width="100%" overflow={"scroll"}>
                        {currentReadFile ? (
                            <Box>
                                <Box background="#2809E3" color="white">
                                    <Text
                                        padding="10px"
                                        overflow={"scroll"}
                                        marginBottom={"5px"}
                                    >
                                        {currentReadFilePath || "Select a file"}
                                    </Text>
                                </Box>
                                <Box height="600px" overflow={"scroll"}>
                                    <CodeBlock
                                        text={currentReadFile?.content}
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
                    <ModalHeader>Writing in progress ...</ModalHeader>
                    <ModalBody pb={6}>
                        <Lottie animationData={writing} loop={true} />
                    </ModalBody>
                </ModalContent>
            </Modal>
            <Card margin="10px auto" padding="10px">
                <Heading textAlign={"center"}>Preview</Heading>
                <Grid
                    templateColumns={{
                        base: "repeat(1,1fr)",
                        md: "repeat(2,1fr)",
                    }}
                >
                    <GridItem margin="10px">
                        <Input
                            placeholder="Name of md file"
                            onChange={(e) => {
                                setMarkdownName(e.target.value);
                            }}
                            value={markdownName}
                        ></Input>
                    </GridItem>
                    <GridItem margin="10px">
                        <ButtonGroup>
                            <Button
                                leftIcon={<DownloadIcon />}
                                colorScheme="purple"
                                borderRadius={5}
                                size="md"
                                onClick={downloadDocumentation}
                            >
                                Download
                            </Button>
                            <Button
                                leftIcon={<DeleteIcon />}
                                colorScheme="red"
                                borderRadius={5}
                                size="md"
                                onClick={() => {
                                    setMarkdownDocumentation("");
                                }}
                            >
                                Clear
                            </Button>
                        </ButtonGroup>
                    </GridItem>
                </Grid>
                <Box margin="10px">
                    <MarkdownEditor
                        height="520px"
                        value={markdownDocumentation}
                        onChange={setMarkdownDocumentation}
                    />
                </Box>
            </Card>
        </Box>
    );
}
