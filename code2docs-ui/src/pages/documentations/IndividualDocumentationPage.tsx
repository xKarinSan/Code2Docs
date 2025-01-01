import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getDocsetURL } from "../../global/constants";
import { useUserStore } from "../../store/userStore";
import { Button, Heading, Box } from "@chakra-ui/react";
import MarkdownEditor from "@uiw/react-markdown-editor";

interface Doc {
    doc_id: number;
    docset_id: number;
    doc_name: string;
    contents: string;
}

function IndividualDocumentationPage() {
    const documentSetInfo = useParams();
    const githubInstallationId = useUserStore(
        (state: any) => state.githubInstallationId
    );
    const [selectedDoc, setSelectedDoc] = useState<Doc>();
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
                    setDocsList(res.data);
                    return res.data;
                });
        } catch (e) {}
    };
    return (
        <div>
            <Heading>Individual documentation</Heading>
            <Box display={"grid"}>
                {docsList.map((documentation: Doc) => {
                    const { doc_name } = documentation;
                    return (
                        <Button
                            onClick={() => {
                                setSelectedDoc(documentation);
                            }}
                        >
                            {doc_name}
                        </Button>
                    );
                })}
            </Box>
            <MarkdownEditor
                height="520px"
                value={selectedDoc?.contents}
                // onChange={setSelectedDoc}
            />{" "}
        </div>
    );
}

export default IndividualDocumentationPage;
