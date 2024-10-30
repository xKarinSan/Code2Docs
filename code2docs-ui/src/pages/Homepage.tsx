import { Heading, Box, Card, SimpleGrid, Image } from "@chakra-ui/react";
import { useUserStore } from "../store/userStore";
import { Link } from "react-router-dom";

import codebaseMenuIcon from "../assets/codebasemenuicon.png";
import documentationMenuIcon from "../assets/documentationmenuicon.png";
import profileMenuIcon from "../assets/profilemenuicon.png";
import logoutMenuIcon from "../assets/logoutmenuicon.png";

function Homepage() {
    const githubUsername = useUserStore((state: any) => state.githubUsername);

    return (
        <Box>
            <Heading>
                Welcome {githubUsername}, what would you like today?
            </Heading>
            <SimpleGrid
                columns={{
                    base: 1,
                    md: 2,
                    xl: 4,
                    "2xl": 4.5,
                }}
            >
                <Link to="/codebases" target="_window">
                    <Card padding={5} margin={5} width={250}>
                        <Image src={codebaseMenuIcon} />
                        Manage Codebases
                    </Card>
                </Link>
                <Link to="/documentations" target="_window">
                    <Card padding={5} margin={5} width={250}>
                        <Image src={documentationMenuIcon} />
                        Manage Documentations
                    </Card>
                </Link>
                <Link to="/profile" target="_window">
                    <Card padding={5} margin={5} width={250}>
                        <Image src={profileMenuIcon} />
                        Manage Profile
                    </Card>
                </Link>
                <Link to="/logout">
                    <Card padding={5} margin={5} width={250}>
                        <Image src={logoutMenuIcon} />
                        Logout
                    </Card>
                </Link>
            </SimpleGrid>
        </Box>
    );
}
export default Homepage;
