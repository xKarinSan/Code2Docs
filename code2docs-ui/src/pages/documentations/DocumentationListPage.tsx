import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getDocsetURL } from "../../global/constants";
import { useUserStore } from "../../store/userStore";
import {
    Heading,
    Card,
    TableContainer,
    Table,
    Thead,
    Tbody,
    Tr,
    Td,
    Th,
    Link,
} from "@chakra-ui/react";
import axios from "axios";

interface DocSet {
    docset_id: number;
    docset_name: string;
    date_generated: Date;
}

function DocumentationListPage() {
    const navigate = useNavigate();
    const githubInstallationId = useUserStore(
        (state: any) => state.githubInstallationId
    );

    const [docSetList, setDocSetList] = useState<DocSet[]>([]);

    const loadDocumentationContents = async () => {
        try {
            await axios
                .get(`${getDocsetURL}set/u/${githubInstallationId}`)
                .then((res) => {
                    console.log("res", res.data);
                    // const { docs, doc_set: docSet } = res.data;
                    setDocSetList(res.data);
                });
        } catch (e) {}
    };

    const goToDocset = (docset_id: number) => {
        navigate(`/documentations/${docset_id}`);
    };
    useEffect(() => {
        loadDocumentationContents();
    }, []);
    return (
        <div>
            <Heading>Documentation History</Heading>
            <Card margin={5}>
                <TableContainer>
                    <Table variant="simple">
                        <Thead>
                            <Th>Doc ID</Th>
                            <Th>Doc Name</Th>
                            <Th>Created Date</Th>
                            <Th>Codebase Link</Th>
                        </Thead>
                        <Tbody>
                            {docSetList.map((docset: DocSet) => {
                                const {
                                    docset_id: docsetId,
                                    docset_name: docsetName,
                                    date_generated: dateCreated,
                                } = docset;
                                return (
                                    <Tr>
                                        <Td>{docsetId}</Td>
                                        <Td>{docsetName}</Td>
                                        <Td>{dateCreated.toString()}</Td>
                                        <Td>
                                            <Link
                                                onClick={() => {
                                                    goToDocset(docsetId);
                                                }}
                                            >
                                                Go to documentations
                                            </Link>
                                        </Td>
                                    </Tr>
                                );
                            })}
                        </Tbody>
                    </Table>
                </TableContainer>
            </Card>
        </div>
    );
}

export default DocumentationListPage;
