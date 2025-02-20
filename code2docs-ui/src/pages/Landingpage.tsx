import {
    AspectRatio,
    SimpleGrid,
    Box,
    Button,
    Card,
    Text,
    Heading,
    Image,
    Input,
    Textarea,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

// ========== assets ==========
// hero section
import LightGreyDots from "../assets/landing/light_grey_dots_background.jpg";
import AstronaultHero from "../assets/landing/astronaut-working-laptop-vector-flat-cartoon-character-illustration_498820-107-removebg-preview.png";

// highlights section
import DocumentGen from "../assets/landing/conceptual-illustration-document-management-organization_1263357-34825-ezgif.com-avif-to-png-converter-removebg-preview.png";
import GithubLogo from "../assets/landing/ghlogo.png";
import Documents from "../assets/landing/archives-icon_1134104-20114-ezgif.com-avif-to-png-converter-removebg-preview.png";
import Gears from "../assets/landing/gears-with-hearts_25030-68420-ezgif.com-avif-to-png-converter-removebg-preview.png";

// demo section
import DemoVideo from "../assets/landing/code2docs jan demo.mp4";

type HighlightCardItems = {
    title: string;
    imageSrc: string;
    desc: string;
};

type StepCardItems = {
    title: string;
    subtitle: string;
    desc: string;
};

function HighlightCard({ title, imageSrc, desc }: HighlightCardItems) {
    return (
        <Card background={"black"} border={"1px #535353 solid"} padding="15px">
            <Image
                src={imageSrc}
                aspectRatio={1}
                height={200}
                width={200}
                margin={"5px auto"}
            />
            <Text fontSize={"18px"} color={"white"} fontWeight={"bold"}>
                {title}
            </Text>
            <Text fontSize={"15px"} color={"white"}>
                {desc}
            </Text>
        </Card>
    );
}

function StepCard({ title, subtitle, desc }: StepCardItems) {
    return (
        <Card border={"1px #9F9F9F solid"} padding="15px">
            <Heading fontSize={24} margin={"5px auto"}>
                {title}
            </Heading>
            <Text fontSize={"18px"} fontWeight={"bold"} margin={"5px auto"}>
                {subtitle}
            </Text>
            <Text fontSize={"15px"} margin={"5px auto"}>
                {desc}
            </Text>
        </Card>
    );
}

const HighlightCardContents: HighlightCardItems[] = [
    {
        title: "Easy Document Generation",
        imageSrc: DocumentGen,
        desc: "Automate the creation of comprehensive code documentation for your codebase.",
    },
    {
        title: "GitHub Integration",
        imageSrc: GithubLogo,
        desc: "This works for Github repositories too!",
    },
    {
        title: "Easy Document Management",
        imageSrc: Documents,
        desc: "Feel free to retrieve and customise your documentations anytime, anywhere!",
    },
    {
        title: "Productivity Boost",
        imageSrc: Gears,
        desc: "Build and ship your product, allow Code2Docs to document your code!",
    },
];

const stepCardContents: StepCardItems[] = [
    {
        title: "Step 1",
        subtitle: "Choose your codebase",
        desc: "in zip format or from your Github repositories",
    },
    {
        title: "Step 2",
        subtitle: "Pick your code",
        desc: "that you want to document!",
    },
    {
        title: "Step 3",
        subtitle: "Document your code",
        desc: "with Code2Docs and its magic!",
    },
    {
        title: "Step 4",
        subtitle: "Preview & Download",
        desc: "after you are satisfied",
    },
];
export default function Landingpage() {
    const navigate = useNavigate();
    const goToLogin = () => {
        navigate("/login");
    };
    return (
        <>
            <Box
                id="home"
                backgroundImage={`url(${LightGreyDots})`}
                backgroundSize="cover"
                bgRepeat={"repeat-y"}
                display={"grid"}
                padding="30px"
            >
                <Heading textAlign={"center"} fontSize={"48px"} margin="30px">
                    Code2Docs
                </Heading>
                <Text marginTop="10" textAlign={"center"} fontSize={"28px"}>
                    Automate your code documentation with{" "}
                    <b>AI-Powered Precision.</b>
                </Text>
                <Image margin={"5px auto"} src={AstronaultHero} />
                <Button
                    background="black"
                    color={"white"}
                    margin={{ md: "5px auto" }}
                    padding={{
                        md: "30px",
                    }}
                    width={{ md: "fit-content" }}
                    onClick={() => {
                        goToLogin();
                    }}
                >
                    Try Now!
                </Button>
            </Box>
            <Box id="highlights" padding="30px" background={"black"}>
                <Heading
                    margin={5}
                    textAlign={"left"}
                    fontSize={"48px"}
                    color="white"
                >
                    Highlights
                </Heading>
                <SimpleGrid
                    columns={{
                        base: 1,
                        md: 2,
                        xl: 4,
                        "2xl": 4.5,
                    }}
                    gap={5}
                    margin={10}
                >
                    {HighlightCardContents.map(
                        (contents: HighlightCardItems) => {
                            const { imageSrc, title, desc } = contents;
                            return (
                                <HighlightCard
                                    title={title}
                                    imageSrc={imageSrc}
                                    desc={desc}
                                />
                            );
                        }
                    )}
                </SimpleGrid>
            </Box>
            <Box id="howwework" padding="30px" background={"white"}>
                <Heading margin={5} textAlign={"left"} fontSize={"48px"}>
                    How Code2Docs Work
                </Heading>
                <SimpleGrid
                    columns={{
                        base: 1,
                        md: 2,
                        xl: 4,
                        "2xl": 4.5,
                    }}
                    gap={5}
                    margin={10}
                >
                    {stepCardContents.map((contents: StepCardItems) => {
                        const { subtitle, title, desc } = contents;
                        return (
                            <StepCard
                                title={title}
                                subtitle={subtitle}
                                desc={desc}
                            />
                        );
                    })}
                </SimpleGrid>
            </Box>
            <Box id="demo" padding="30px" background={"white"}>
                <Heading margin={5} textAlign={"left"} fontSize={"48px"}>
                    Demo
                </Heading>
                <Card border={"1px #9F9F9F solid"} padding={5} margin={30}>
                    <AspectRatio ratio={2} padding={15}>
                        <iframe
                            width={"80%"}
                            title="demo"
                            src={DemoVideo}
                            allowFullScreen
                        />
                    </AspectRatio>
                </Card>
            </Box>
            <Box id="contactus" padding="30" background={"black"}>
                <footer>
                    <Heading
                        margin={5}
                        textAlign={"left"}
                        fontSize={"48px"}
                        color="white"
                    >
                        {" "}
                        Contact Us
                    </Heading>
                    <Box></Box>
                    <Text color={"white"} fontSize={22} marginX={5}>
                        Feel free to drop us a message here and we will get back
                        to you soon!
                    </Text>
                    <Box
                        margin={5}
                        display={"grid"}
                        width={{
                            md: "40vw",
                            lg: "35vw",
                        }}
                    >
                        <Text color="white" marginY={2}>
                            Name:
                        </Text>
                        <Input marginY={2} color={"white"}></Input>

                        <Text color="white" marginY={2}>
                            Email:
                        </Text>
                        <Input marginY={2} color={"white"}></Input>

                        <Text color="white" marginY={2}>
                            Message:
                        </Text>
                        <Textarea marginY={2} color={"white"}></Textarea>
                        <Button
                            background="white"
                            padding={{
                                md: "30px",
                            }}
                            marginTop={4}
                            width={{ md: "fit-content" }}                            
                        >
                            Send Message
                        </Button>
                    </Box>
                    <Text color="white" fontSize={14} marginX={5}>
                        ©2025 Code2Docs. All rights reserved.
                    </Text>
                </footer>
            </Box>
        </>
    );
}
