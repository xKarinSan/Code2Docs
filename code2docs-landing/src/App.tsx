import React, { useState } from "react";
import { Github, FileText, ArrowRight } from "lucide-react";
import { ToastContainer, ToastContentProps, toast } from "react-toastify";
import HeroBackground from "./assets/light_grey_dots_background.jpg";
import HeroIcon from "./assets/astronaut-working-laptop-vector-flat-cartoon-character-illustration_498820-107-removebg-preview.png";

type CustomNotificationProps = ToastContentProps<{
    title: string;
    content: string;
}>;

function CustomNotification({ data, toastProps }: CustomNotificationProps) {
    const isColored = toastProps.theme === "colored";

    return (
        <div className="flex flex-col w-full">
            <h3 className={isColored ? "text-white" : "text-zinc-800"}>
                {data.title}
            </h3>
            <div className="flex items-center justify-between">
                <p className="text-sm">{data.content}</p>
            </div>
        </div>
    );
}

function App() {
    const [email, setEmail] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        await fetch(
            "https://docs.google.com/forms/d/1S6uhisVBTGOh36hanCIEx0i2_zanaJVJFT2TwKHJ3sM/formResponse",
            {
                method: "POST",
                mode: "no-cors",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ "entry.245011889": email }), // Adjust field name
            }
        ).then(() => {
            toast.success(CustomNotification, {
                data: {
                    title: "Thank You!",
                    content:
                        "We've received your feedback and will keep you updated on our progress.",
                },
            });
        });
    };

    return (
        <div className="min-h-screen bg-white">
            {/* Hero Section */}
            <div className="relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80')] bg-cover bg-center opacity-5" />
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 relative">
                    <div className="text-center">
                        <h1 className="text-5xl font-bold text-black mb-6">
                            Code2Docs
                        </h1>
                        {/* <img
                            src={HeroIcon}
                            alt="Hero Icon"
                            className="flex self-center m-auto"
                        /> */}
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
                            Transform your codebase into beautiful documentation
                            effortlessly. Seamless GitHub integration with
                            markdown support.
                        </p>
                        <div className="flex justify-center gap-4 mb-12">
                            <div className="flex items-center space-x-2 text-gray-700">
                                <Github className="w-5 h-5" />
                                <span>GitHub Integration</span>
                            </div>
                            <div className="flex items-center space-x-2 text-gray-700">
                                <FileText className="w-5 h-5" />
                                <span>Markdown Support</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Features Section */}
            <div className="bg-gray-50 py-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-2 gap-12">
                        <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-100">
                            <Github className="w-8 h-8 mb-4 text-black" />
                            <h3 className="text-xl font-semibold mb-4">
                                GitHub Integration
                            </h3>
                            <p className="text-gray-600">
                                Connect your GitHub repositories and
                                automatically generate documentation from your
                                codebase. Keep your docs in sync with your code.
                            </p>
                        </div>
                        <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-100">
                            <FileText className="w-8 h-8 mb-4 text-black" />
                            <h3 className="text-xl font-semibold mb-4">
                                Markdown Support
                            </h3>
                            <p className="text-gray-600">
                                Write documentation in Markdown format. Simple,
                                familiar, and powerful. Support for code blocks,
                                tables, and more.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Feedback Form Section */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <div className="max-w-2xl mx-auto">
                    <>
                        <div className="text-center mb-12">
                            <h2 className="text-3xl font-bold mb-4">
                                Help Shape Our Future
                            </h2>
                            <p className="text-gray-600">
                                We're building Code2Docs to solve real
                                documentation challenges. Share your thoughts
                                and be part of our journey.
                            </p>
                        </div>
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div>
                                <label
                                    htmlFor="email"
                                    className="block text-sm font-medium text-gray-700 mb-1"
                                >
                                    Email Address
                                </label>
                                <input
                                    type="email"
                                    id="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-black focus:border-transparent"
                                    placeholder="you@example.com"
                                />
                            </div>
                            <div></div>
                            <button
                                type="submit"
                                className="w-full bg-black text-white py-3 px-6 rounded-md hover:bg-gray-800 transition-colors flex items-center justify-center gap-2"
                            >
                                <span>Join the Waitlist</span>
                                <ArrowRight className="w-4 h-4" />
                            </button>
                            <ToastContainer position="top-center" />
                        </form>
                    </>
                </div>
            </div>

            {/* Footer */}
            <footer className="bg-gray-50 py-8">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center text-gray-600 text-sm">
                        © 2024 Code2Docs. All rights reserved.
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default App;
