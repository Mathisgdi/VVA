import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

export default function Home() {
    return (
        <div className='flex h-screen justify-center items-center'>
            <Select>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Date"/>
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="2024">2024</SelectItem>
                    <SelectItem value="2025">2025</SelectItem>
                </SelectContent>
            </Select>
        </div>
    );
}
