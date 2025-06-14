'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Card, Title } from '@tremor/react'

export default function Navigation() {
  const pathname = usePathname()

  const navItems = [
    { name: 'Dashboard', path: '/' },
    { name: 'Performance', path: '/performance' },
    { name: 'Optimization', path: '/optimization' },
    { name: 'Alerts', path: '/alerts' },
    { name: 'Settings', path: '/settings' }
  ]

  return (
    <Card className="mb-6">
      <div className="flex items-center justify-between">
        <Title>SloeLux Performance Bot</Title>
        <nav className="flex space-x-4">
          {navItems.map((item) => (
            <Link
              key={item.path}
              href={item.path}
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                pathname === item.path
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </div>
    </Card>
  )
} 