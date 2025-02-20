import axios from "axios";
import { useEffect, useState } from "react";
import { useParams, NavLink } from "react-router-dom";
import { getDocsetURL } from "../../global/constants";
import { useUserStore } from "../../store/userStore";
import {
    Breadcrumb,
    BreadcrumbLink,
    BreadcrumbItem,
    Heading,
    Box,
    Card,
} from "@chakra-ui/react";
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
    const [selectedDoc, setSelectedDoc] = useState<Doc | null>();
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

    const selectDocumentation = (currentDoc: Doc) => {
        setSelectedDoc(
            selectedDoc?.doc_id != currentDoc.doc_id ? currentDoc : null
        );
    };
    return (
        <Box>
            <Breadcrumb>
                <BreadcrumbItem>
                    <NavLink to="/home">
                        <BreadcrumbLink>Home</BreadcrumbLink>
                    </NavLink>
                </BreadcrumbItem>
                <BreadcrumbItem>
                    <NavLink to="/documentations">
                        <BreadcrumbLink>Documentations</BreadcrumbLink>
                    </NavLink>
                </BreadcrumbItem>
                <BreadcrumbItem>
                    <BreadcrumbLink>
                        {selectedDocSet?.docset_name}
                    </BreadcrumbLink>
                </BreadcrumbItem>
            </Breadcrumb>
            <Heading margin={5}>
                Documentations for {selectedDocSet?.docset_name}
            </Heading>
            <Box display={"flex"} margin={2}>
                <Box height={"80vh"} width={"30%"} overflow={"scroll"}>
                    {docsList.map((documentation: Doc) => {
                        const { doc_name, doc_id } = documentation;
                        return (
                            <Card
                                background={
                                    selectedDoc?.doc_id == doc_id
                                        ? "black"
                                        : "white"
                                }
                                textColor={
                                    selectedDoc?.doc_id == doc_id
                                        ? "white"
                                        : "black"
                                }
                                margin={2}
                                padding={3}
                                whiteSpace={"nowrap"}
                                overflow={"scroll"}
                                textAlign={"left"}
                                _hover={{ cursor: "pointer" }}
                                onClick={() => {
                                    selectDocumentation(documentation);
                                }}
                            >
                                {doc_name}
                            </Card>
                        );
                    })}
                </Box>
                <Box
                    overflow={"scroll"}
                    width={"60%"}
                    height={"80vh"}
                    padding={2}
                >
                    <MarkdownEditor
                        minHeight="60vh"
                        value={selectedDoc?.contents}
                    />
                </Box>
            </Box>
        </Box>
    );
}

export default IndividualDocumentationPage;
