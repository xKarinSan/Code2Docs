import { useUserStore } from "../../store/userStore";
import {
    Box,
    Button,
    Card,
    FormLabel,
    Heading,
    Image,
    Input,
    InputGroup,
} from "@chakra-ui/react";
import { Link } from "react-router-dom";
function UserAccountPage() {
    const githubProfilePictureUrl = useUserStore(
        (state: any) => state.githubProfilePictureUrl
    );
    const githubDisplayName = useUserStore(
        (state: any) => state.githubDisplayName
    );
    const githubUsername = useUserStore((state: any) => state.githubUsername);
    return (
        <Box>
            <Card
                padding={5}
                marginX={20}
                marginY={5}
                maxWidth={"700px"}
                margin={"auto"}
            >
                <Heading alignContent={"center"} margin={"auto"}>
                    User Profile
                </Heading>
                <Image
                    margin={"10px auto"}
                    src={githubProfilePictureUrl ?? ""}
                    borderRadius={50}
                    width={100}
                    height={100}
                />
                <InputGroup padding={5} alignItems={"center"}>
                    <FormLabel>Username:</FormLabel>
                    <Input
                        value={githubUsername ?? ""}
                        disabled={true}
                        background={"white"}
                        border={"1px black solid"}
                    />
                </InputGroup>
                <Link to="/logout">
                    <Button
                        margin={"auto"}
                        alignSelf={"start"}
                        left={0}
                        background="black"
                        color="white"
                        borderRadius={5}
                    >
                        Logout
                    </Button>
                </Link>
            </Card>
        </Box>
    );
}

export default UserAccountPage;
