import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getDocsetURL } from "../../global/constants";
import { useUserStore } from "../../store/userStore";
import { Button, Heading, Box, Card } from "@chakra-ui/react";
import MarkdownEditor from "@uiw/react-markdown-editor";

interface Doc {
    doc_id: number;
    docset_id: number;
    doc_name: string;
    contents: string;
}

interface DocSet {
    docset_id: number;
    docset_name: string;
    date_generated: Date;
}

function IndividualDocumentationPage() {
    const documentSetInfo = useParams();
    const githubInstallationId = useUserStore(
        (state: any) => state.githubInstallationId
    );
    const [selectedDoc, setSelectedDoc] = useState<Doc>();
    const [selectedDocSet, setSelectedDocSet] = useState<DocSet>();
    const [docsList, setDocsList] = useState([]);

    useEffect(() => {
        loadDocumentationContents();
    }, []);

    const loadDocumentationContents = async () => {
        try {
            const { docset_id } = documentSetInfo;
            await axios
                .get(`${getDocsetURL}s/${docset_id}/u/${githubInstallationId}`)
                .then((res) => {
                    console.log("res", res.data);
                    const { docs, doc_set: docSet } = res.data;
                    setDocsList(docs);
                    setSelectedDocSet(docSet);
                });
        } catch (e) {}
    };
    return (
        <Box>
            <Heading margin={5}>{selectedDocSet?.docset_name}</Heading>
            <Box display={"flex"}>
                <Box height={"auto"}>
                    {docsList.map((documentation: Doc) => {
                        const { doc_name } = documentation;
                        return (
                            <Card margin={2}>
                                <Button
                                    background={"white"}
                                    onClick={() => {
                                        setSelectedDoc(documentation);
                                    }}
                                >
                                    {doc_name}
                                </Button>
                            </Card>
                        );
                    })}
                </Box>
                <MarkdownEditor
                    width={"auto"}
                    height="520px"
                    value={selectedDoc?.contents}
                />
            </Box>
        </Box>
    );
}

export default IndividualDocumentationPage;
