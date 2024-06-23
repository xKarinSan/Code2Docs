import { Card, Heading, Input, Button, Box } from "@chakra-ui/react";
import JSZip from "jszip";
import { useState } from "react";
import { FileNode, buildFileTree } from "../helpers/FileNode";
import { FileTree } from "../components/global/FileTree";

export default function DemoPage() {
    const zip = new JSZip();
    const [fileTree, setFileTree] = useState<FileNode | null>(null);

    const selectFile = async (files: FileList | null) => {
        if (files) {
            const contents = await zip.loadAsync(files[0]);

            const extractedFiles = [];
            for (const [filename, fileData] of Object.entries(contents.files)) {
                if (!fileData.dir) {
                    const content = await fileData.async("text");
                    extractedFiles.push({ filename, content });
                }
            }
            const tree = buildFileTree(extractedFiles);
            setFileTree(tree);
        }
    };

    return (
        <Box>
            <Card margin="auto" width="60%">
                <Heading textAlign={"center"}>Upload File</Heading>
                <Input
                    border="none"
                    type="file"
                    accept=".zip"
                    multiple={true}
                    onChange={(e) => {
                        selectFile(e.target.files);
                    }}
                />
                {fileTree && <FileTree node={fileTree} />}
            </Card>
        </Box>
    );
}
