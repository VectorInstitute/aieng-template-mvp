'use client';

import React, { memo } from 'react';
import { Box, Flex, Container, Image, useBreakpointValue } from '@chakra-ui/react'
import NextLink from 'next/link'

const Header: React.FC = () => {
  const logoSize = useBreakpointValue({ base: "80px", md: "100px" })

  return (
    <Box as="header" position="relative" top={0} left={0} right={0} zIndex={10} bg="white" borderBottom="1px" borderColor="gray.200">
      <Container maxW="1200px">
        <Flex justify="flex-start" align="center" py={2}>
          <Box
            width={logoSize}
            height="30px"
            position="relative"
            cursor="pointer"
          >
            <NextLink href="/" passHref>
              <Image
                src="/images/vector-logo.png"
                alt="Vector Institute"
                objectFit="contain"
                width="100%"
                height="100%"
                fallbackSrc="https://via.placeholder.com/150x40?text=Vector+Institute"
              />
            </NextLink>
          </Box>
        </Flex>
      </Container>
    </Box>
  )
}

export default memo(Header);
