'use client';

import React, { memo } from 'react';
import { Box, Container, Heading, Text, VStack, useBreakpointValue } from '@chakra-ui/react'

const Hero: React.FC = () => {
  const headingSize = useBreakpointValue({ base: "xl", md: "2xl", lg: "3xl" });
  const textSize = useBreakpointValue({ base: "sm", md: "md", lg: "lg" });

  return (
    <Box
      bgGradient="linear(to-r, brand.pink, brand.purple)"
      position="relative"
      py={{ base: "40px", md: "60px" }}
      mt="1px" // Add a tiny margin to ensure no gap with header
    >
      <Container maxW="1200px">
        <VStack
          spacing={4}
          alignItems="center"
          justifyContent="center"
          textAlign="center"
        >
          <Heading as="h1" size={headingSize} color="white" fontWeight="bold">
            AI Engineering MVP Template
          </Heading>
          <Text fontSize={textSize} color="white" maxW="700px">
            A starter template for building AI-powered applications with Vector Institute branding.
          </Text>
        </VStack>
      </Container>
    </Box>
  )
}

export default memo(Hero);
