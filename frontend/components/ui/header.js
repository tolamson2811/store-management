import Image from "next/image";
import Link from "next/link";

export default function Header() {
    return (
        <header className=" top-0 left-0 right-0 fixed h-20 bg-slate-700">
            <nav className="flex items-center justify-between gap-8 h-full px-8">
                <div>
                    <Link href={'/'}>
                        <Image
                            src="https://cdn2.iconfinder.com/data/icons/facebook-ui-colored/48/JD-15-512.png"
                            width={100}
                            height={100}
                            alt="store logo"
                        />
                    </Link>
                </div>

                

                <div className="flex items-center gap-8">
                    <Link href={"/category"} className="text-white">
                        Order
                    </Link>
                    <Link href={"/contact"} className="text-white">
                        Transaction
                    </Link>
                    <Link href={"/account"} className=" text-white">Account</Link>
                </div>
            </nav>
        </header>
    );
}
