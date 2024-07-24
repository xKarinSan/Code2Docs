import {
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
        setCurrentReadFile(null);
        setCurrentReadFilePath("");
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
                >
                    <GridItem margin="10px">
                        <Input
                            ref={fileInputRef}
                            width="fit-content"
                            border="none"
                            type="file"
                            accept=".zip"
                            multiple={true}
                            onChange={(e) => {
                                selectFile(e.target.files);
                            }}
                            alignContent={"center"}
                        />
                    </GridItem>
                    <GridItem
                        margin="10px"
                        display={"flex"}
                        justifyContent={{
                            base: "start",
                            md: "center",
                        }}
                    >
                        <Button onClick={removeFile}>Remove zip file</Button>
                    </GridItem>
                </Grid>
            </Card>
            <Grid
                gridTemplateColumns={"49% 49%"}
                justifyContent={"space-between"}
                gap={1}
            >
                <GridItem>
                    <Card
                        overflow="scroll"
                        height="500px"
                        width="100%"
                        padding="10px"
                    >
                        {fileTree && (
                            <FileTree
                                node={fileTree}
                                setReadFile={setCurrentReadFile}
                                setReadFilePath={setCurrentReadFilePath}
                                setReadDirectory={setCurrentReadDirectory}
                            />
                        )}
                    </Card>
                </GridItem>
                <GridItem>
                    <Card overflow="scroll" height="500px" width="100%">
                        <Text padding="10px">
                            {currentReadFilePath || "Select a file"}
                        </Text>
                        <CodeBlock
                            text={currentReadFile?.content}
                            showLineNumbers={true}
                        />
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
            <Card margin="10px auto" padding="5px" display={"grid"}>
                <Grid
                    templateColumns={{
                        base: "repeat(1,1fr)",
                        md: "repeat(2,1fr)",
                    }}
                    gap={5}
                >
                    <GridItem margin="10px" alignSelf={"center"}>
                        Selected Folder:
                        {currentReadDirectory ? currentReadDirectory.name : ""}
                    </GridItem>
                    <GridItem margin="10px">
                        <Button onClick={generateDocumentation}>
                            Write Docs
                        </Button>
                    </GridItem>
                </Grid>
            </Card>
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
                        <Button
                            colorScheme="purple"
                            borderRadius={5}
                            size="md"
                            onClick={downloadDocumentation}
                        >
                            Download
                        </Button>
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
