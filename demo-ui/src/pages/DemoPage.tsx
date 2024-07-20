import {
    Card,
    Heading,
    Input,
    Box,
    Grid,
    GridItem,
    Button,
    Textarea,
    Spacer,
    Flex,
} from "@chakra-ui/react";
import JSZip from "jszip";
import { useRef, useState } from "react";
import { FileNode, buildFileTree } from "../helpers/FileNode";
import { FileTree } from "../components/global/FileTree";
import axios from "axios";

export default function DemoPage() {
    const zip = new JSZip();

    const fileInputRef = useRef<HTMLInputElement | null>(null);
    const [fileTree, setFileTree] = useState<FileNode | null>(null);
    const [currentReadFile, setCurrentReadFile] = useState<FileNode | null>(
        null
    );
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

    const traverseNode = (
        currNode: FileNode | null,
        currentChildrenArr: FileNode[]
    ) => {
        if (currNode?.children) {
            currNode.children.forEach((child: FileNode) => {
                currentChildrenArr.push(child);
                traverseNode(child, currentChildrenArr);
            });
        }
        return currentChildrenArr;
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
        const zipBlob = await createZipFile();
        const formData = new FormData();
        formData.append("file", zipBlob);
        await axios
            .post(`${import.meta.env.VITE_API_URL}/demo`, formData)
            .then((res) => {
                setMarkdownDocumentation(res.data.data);
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
    };

    return (
        <Box width="80%" margin="auto">
            <Heading textAlign={"center"}>Demo</Heading>
            <Card margin="10px auto">
                <Grid templateColumns="repeat(2, 1fr)">
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
                        />
                    </GridItem>
                    <GridItem margin="10px">
                        <Button onClick={removeFile}>Remove zip file</Button>
                    </GridItem>
                </Grid>
            </Card>
            <Grid templateColumns="repeat(4, 1fr)" gap={1}>
                <GridItem colSpan={1}>
                    <Card overflow={"scroll"} padding="10px" height="500px">
                        {fileTree && (
                            <FileTree
                                node={fileTree}
                                setReadFile={setCurrentReadFile}
                                setReadDirectory={setCurrentReadDirectory}
                            />
                        )}
                    </Card>
                </GridItem>
                <GridItem colSpan={3}>
                    <Card
                        padding="20px"
                        overflow="scroll"
                        height="500px"
                        whiteSpace="pre"
                    >
                        {currentReadFile?.content}
                    </Card>
                </GridItem>
            </Grid>
            <Card margin="10px auto" padding="10px" display={"grid"}>
                <Grid templateColumns="repeat(3, 1fr)" gap={5}>
                    <GridItem margin="10px">
                        Selected Folder:
                        {currentReadDirectory ? currentReadDirectory.name : ""}
                    </GridItem>
                    <GridItem margin="10px" colSpan={2}>
                        <Flex gap={5}>
                            <Button onClick={generateDocumentation}>
                                Write Documentation
                            </Button>
                            <Input
                                width="30%"
                                placeholder="Name of md file"
                                onChange={(e) => {
                                    setMarkdownName(e.target.value);
                                }}
                                value={markdownName}
                            ></Input>
                            <Button
                                colorScheme="purple"
                                borderRadius={5}
                                size="md"
                                width="200px"
                                onClick={downloadDocumentation}
                            >
                                Download
                            </Button>
                        </Flex>
                    </GridItem>
                </Grid>
            </Card>
            {/* <Card margin="10px auto" padding="10px" display={"grid"}>
                <Flex gap={5}>
                    <Spacer />
                    <Input
                        width="30%"
                        placeholder="Name of md file"
                        onChange={(e) => {
                            setMarkdownName(e.target.value);
                        }}
                        value={markdownName}
                    ></Input>
                    <Button
                        colorScheme="purple"
                        borderRadius={5}
                        size="md"
                        width="200px"
                        onClick={downloadDocumentation}
                    >
                        Download
                    </Button>
                </Flex>
            </Card> */}
            <Card margin="10px auto" padding="20px" height="600px">
                <Grid templateColumns="repeat(2, 1fr)" gap={5} height={"100%"}>
                    <GridItem>
                        <Box>
                            <Heading>Edit Preview</Heading>
                            <Textarea
                                spellCheck={false}
                                value={markdownDocumentation}
                                onChange={(e) => {
                                    setMarkdownDocumentation(e.target.value);
                                }}
                                height={500}
                                resize={"none"}
                            ></Textarea>
                        </Box>
                    </GridItem>
                    <GridItem flex={1}>
                        <Box>
                            <Heading>Preview</Heading>
                            {/* <ReactMarkdown components={ChakraUIRenderer()}> */}
                            <Box maxHeight="500px" overflow={"scroll"}>
                                {markdownDocumentation}
                            </Box>

                            {/* </ReactMarkdown> */}
                        </Box>
                    </GridItem>
                </Grid>
            </Card>
        </Box>
    );
}
