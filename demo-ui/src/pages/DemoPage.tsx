import {
    Card,
    Heading,
    Input,
    Box,
    Grid,
    GridItem,
    Button,
    Textarea,
} from "@chakra-ui/react";
import { ChangeEvent, MutableRefObject, ReactNode } from "react";
import JSZip from "jszip";
import { useRef, useState } from "react";
import { FileNode, buildFileTree } from "../helpers/FileNode";
import { FileTree } from "../components/global/FileTree";
import ReactMarkdown from "react-markdown";
import ChakraUIRenderer from "chakra-ui-markdown-renderer";

export default function DemoPage() {
    const fileInputRef = useRef<HTMLDivElement>(null);
    const zip = new JSZip();
    const [fileTree, setFileTree] = useState<FileNode | null>(null);
    const [currentReadFile, setCurrentReadFile] = useState<FileNode | null>(
        null
    );
    const [currentReadDirectory, setCurrentReadDirectory] =
        useState<FileNode | null>(null);
    const [markdownDocumentation, setMarkdownDocumentation] = useState("");

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

    const removeFile = () => {
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
        setFileTree(null);
        setCurrentReadFile(null);
    };

    const handleDocumentationChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
        // setMarkdownDocumentation(e.target.value);
        if (previewRef.current) {
            previewRef.current.innerHTML = sd.makeHtml(e.target.value);
        }
    };

    return (
        <Box width="80%" margin="auto">
            <Heading textAlign={"center"}>Demo</Heading>
            <Box display="flex" justifyContent={"space-evenly"}>
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
                <Button onClick={removeFile}>Remove zip file</Button>
            </Box>
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
            <Card margin="10px auto" padding="20px" height="300px">
                Selected Directory:
                {currentReadDirectory ? currentReadDirectory.name : ""}
                <Grid templateColumns="repeat(2, 1fr)" gap={1}>
                    <GridItem>
                        <Textarea
                            spellCheck={false}
                            onChange={(e) => {
                                setMarkdownDocumentation(e.target.value);
                            }}
                        ></Textarea>
                    </GridItem>
                    <GridItem flex={1}>
                        <Heading>Preview</Heading>
                        <ReactMarkdown components={ChakraUIRenderer()}>
                            {markdownDocumentation}
                        </ReactMarkdown>
                    </GridItem>
                </Grid>
            </Card>
        </Box>
    );
}
