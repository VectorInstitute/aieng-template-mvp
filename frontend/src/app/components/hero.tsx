'use client';

import React, { memo } from 'react';

const Hero: React.FC = () => {
  return (
    <div
      className="relative py-10 md:py-15 mt-[1px]"
      style={{ background: 'linear-gradient(to right, #eb088a, #8a08eb)' }}
    >
      <div className="max-w-[1200px] mx-auto px-4">
        <div className="flex flex-col gap-4 items-center justify-center text-center">
          <h1 className="text-3xl md:text-4xl lg:text-5xl text-white font-bold">
            AI Engineering MVP Template
          </h1>
          <p className="text-sm md:text-base lg:text-lg text-white max-w-[700px]">
            A starter template for building AI-powered applications with Vector Institute branding.
          </p>
        </div>
      </div>
    </div>
  )
}

export default memo(Hero);
