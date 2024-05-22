import Header from "@/components/ui/header";
import Footer from "@/components/ui/footer";

export default function MainLayout({ children }) {
    return (
        <>
            <Header />
            {children}
            <Footer/>
        </>
    );
}