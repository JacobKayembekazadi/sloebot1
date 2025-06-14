'use client'

import React from 'react'
import { Card, Title, Text, Metric, AreaChart, BarChart, DonutChart } from '@tremor/react'

export default function DashboardPage() {
  const performanceData = [
    { date: '2024-02-14 00:00', lcp: 2.1, tbt: 250, inp: 180 },
    { date: '2024-02-14 01:00', lcp: 2.3, tbt: 280, inp: 190 },
    { date: '2024-02-14 02:00', lcp: 2.0, tbt: 240, inp: 170 },
    { date: '2024-02-14 03:00', lcp: 2.2, tbt: 260, inp: 185 },
    { date: '2024-02-14 04:00', lcp: 2.4, tbt: 290, inp: 195 }
  ]

  const resourceData = [
    { name: 'Images', value: 45 },
    { name: 'JavaScript', value: 25 },
    { name: 'CSS', value: 15 },
    { name: 'Fonts', value: 10 },
    { name: 'Other', value: 5 }
  ]

  const optimizationData = [
    { name: 'Image Optimization', value: 85 },
    { name: 'Code Minification', value: 92 },
    { name: 'Caching', value: 78 },
    { name: 'Lazy Loading', value: 88 }
  ]

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <Text>Performance Score</Text>
          <Metric>92</Metric>
        </Card>
        <Card>
          <Text>Largest Contentful Paint</Text>
          <Metric>2.2s</Metric>
        </Card>
        <Card>
          <Text>Total Blocking Time</Text>
          <Metric>260ms</Metric>
        </Card>
        <Card>
          <Text>Interaction to Next Paint</Text>
          <Metric>185ms</Metric>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <Title>Performance Trends</Title>
          <AreaChart
            className="mt-4 h-72"
            data={performanceData}
            index="date"
            categories={['lcp', 'tbt', 'inp']}
            colors={['blue', 'green', 'orange']}
            valueFormatter={(number) => `${number}ms`}
          />
        </Card>

        <Card>
          <Title>Resource Distribution</Title>
          <DonutChart
            className="mt-4 h-72"
            data={resourceData}
            category="value"
            index="name"
            valueFormatter={(number) => `${number}%`}
            colors={['blue', 'cyan', 'indigo', 'violet', 'fuchsia']}
          />
        </Card>
      </div>

      <Card>
        <Title>Optimization Progress</Title>
        <BarChart
          className="mt-4 h-72"
          data={optimizationData}
          index="name"
          categories={['value']}
          colors={['blue']}
          valueFormatter={(number) => `${number}%`}
        />
      </Card>
    </div>
  )
} 