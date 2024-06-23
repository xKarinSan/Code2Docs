import {
    Card,
    Heading,
    Input,
    Box,
    Grid,
    GridItem,
    Button,
} from "@chakra-ui/react";
import JSZip from "jszip";
import { useRef, useState } from "react";
import { FileNode, buildFileTree } from "../helpers/FileNode";
import { FileTree } from "../components/global/FileTree";

export default function DemoPage() {
    const fileInputRef = useRef();
    const zip = new JSZip();
    const [fileTree, setFileTree] = useState<FileNode | null>(null);
    const [currentReadFile, setCurrentReadFile] = useState<FileNode | null>(
        null
    );

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

    return (
        <Box>
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
        </Box>
    );
}
