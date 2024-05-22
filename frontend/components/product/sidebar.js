"use client";

import { Separator } from "../ui/separator";
import { FaAngleRight } from "react-icons/fa6";

export default function Sidebar() {
    return (
        <div className=" w-full h-full bg-[#f7f7f8] py-6 px-8 border-2 rounded-lg flex flex-col gap-8">
            {/* ... */}
            <div className="flex flex-col">
                <h3 className=" font-semibold text-xs md:text-sm lg:text-base xl:text-lg mb-3">
                    Sản phẩm
                </h3>
                <Separator />

                <div className="flex flex-col gap-1 mt-2">
                    <span className="flex justify-between items-center p-2 hover:cursor-pointer hover:bg-slate-200 rounded-xl">
                        <h3 className=" xl:text-sm text-xs font-medium">Đồ uống</h3>
                        <FaAngleRight />
                    </span>

                    <span className="flex justify-between items-center p-2 hover:cursor-pointer hover:bg-slate-200 rounded-xl">
                        <h3 className=" xl:text-sm text-xs font-medium">Đồ ăn</h3>
                        <FaAngleRight />
                    </span>

                    <span className="flex justify-between items-center p-2 hover:cursor-pointer hover:bg-slate-200 rounded-xl">
                        <h3 className=" xl:text-sm text-xs font-medium">Hàng hóa</h3>
                        <FaAngleRight />
                    </span>
                </div>
            </div>
        </div>
    );
}
