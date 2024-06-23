import { Card, Heading, Input, Button, Box } from "@chakra-ui/react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function UploadPage() {
    const navigate = useNavigate();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const selectFile = (files: FileList | null) => {
        if (files) {
            setSelectedFile(files[0]);
        }
    };
    const uploadFile = () => {
        navigate("/browse");
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
                {selectedFile?.name}
                <Button onClick={uploadFile}>Scan</Button>
            </Card>
        </Box>
    );
}
