import Sidebar from "@/components/product/sidebar"
import { Separator } from "@/components/ui/separator"

export default function Home() {
    return (
        <main className=" grid grid-cols-4 min-h-screen items-center justify-between pt-32 pb-16 px-16 gap-12">
            <Sidebar/>

            <div className=" col-span-3 w-full bg-green-200 h-full py-6 pl-8">
                products list 
            </div>

            
        </main>
    )
}