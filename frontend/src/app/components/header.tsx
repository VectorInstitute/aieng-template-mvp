import Link from 'next/link'

export default function Header() {
  return (
    <header className="w-full">
      <nav className="flex justify-between items-center py-4">
        <Link href="/" className="font-bold text-xl">AI MVP</Link>
        <div className="flex items-center gap-6">
          <Link href="https://nextjs.org/docs" className="hover:underline" target="_blank">
            Next.js Docs
          </Link>
          <Link href="https://fastapi.tiangolo.com" className="hover:underline" target="_blank">
            FastAPI Docs
          </Link>
        </div>
      </nav>
    </header>
  )
}
