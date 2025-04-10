import Header from './components/header'
import Hero from './components/hero'
import { Box } from '@chakra-ui/react'

export default function Home() {
  return (
    <Box as="main" minH="100vh" display="flex" flexDirection="column">
      <Header />
      <Hero />
    </Box>
  )
}
