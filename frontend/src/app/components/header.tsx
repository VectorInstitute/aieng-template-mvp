'use client';

import React, { memo } from 'react';
import NextLink from 'next/link'
import Image from 'next/image'

const Header: React.FC = () => {
  return (
    <header className="relative top-0 left-0 right-0 z-10 bg-white border-b border-gray-200">
      <div className="max-w-[1200px] mx-auto px-4">
        <div className="flex justify-start items-center py-2">
          <div className="w-20 md:w-[100px] h-[30px] relative cursor-pointer">
            <NextLink href="/">
              <Image
                src="/images/vector-logo.png"
                alt="Vector Institute"
                fill
                style={{ objectFit: 'contain' }}
              />
            </NextLink>
          </div>
        </div>
      </div>
    </header>
  )
}

export default memo(Header);
