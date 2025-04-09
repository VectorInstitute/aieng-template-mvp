import Header from './components/header'
import ApiExample from './components/api-example'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-6">
      <Header />
      <div className="flex flex-col items-center justify-center gap-8 py-20">
        <h1 className="text-4xl font-bold text-center">Welcome to your AI Engineering MVP</h1>
        <p className="text-xl text-center max-w-2xl">
          This is a starting point for your AI-powered application. Customize this page
          or create new pages to build your MVP.
        </p>
        <ApiExample />
      </div>
    </main>
  )
}
