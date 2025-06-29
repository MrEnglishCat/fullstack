
import "./globals.css";
import Link from "next/link";

export default function RootLayout({children}) {
    return (
        <html>
        <body>
        <div className="flex gap-5" style={{width:6000,}}>
            <div className="flex flex-col gap-3">
                <Link href="/charts" className=" hover:bg-blue-300">Диаграммы</Link>
                <Link href="/" className=" hover:bg-blue-400">База данных</Link>
                <Link href="/start_parser" className=" hover:bg-blue-400">Запуск парсера</Link>
            </div>
            {children}
        </div>
        </body>
        </html>
    );
}
