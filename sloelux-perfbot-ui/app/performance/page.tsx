'use client'

import { Card, Title, Text, AreaChart, BarChart, DonutChart } from '@tremor/react'
import { useState, useEffect } from 'react'

export default function PerformancePage() {
  const [metrics, setMetrics] = useState({
    performance: [],
    lcp: [],
    tbt: [],
    inp: []
  })

  useEffect(() => {
    // Fetch metrics from API
    const fetchMetrics = async () => {
      try {
        const response = await fetch('http://localhost:8000/metrics')
        const data = await response.json()
        setMetrics(data)
      } catch (error) {
        console.error('Error fetching metrics:', error)
      }
    }

    fetchMetrics()
    const interval = setInterval(fetchMetrics, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <Title>Performance Score</Title>
          <DonutChart
            className="mt-6"
            data={[
              { name: 'Score', value: 92 },
              { name: 'Remaining', value: 8 }
            ]}
            category="value"
            index="name"
            colors={['blue', 'gray']}
            valueFormatter={(value) => `${value}%`}
          />
        </Card>

        <Card>
          <Title>Largest Contentful Paint</Title>
          <AreaChart
            className="mt-6"
            data={metrics.lcp}
            index="timestamp"
            categories={['value']}
            colors={['blue']}
            valueFormatter={(value) => `${value}s`}
          />
        </Card>

        <Card>
          <Title>Total Blocking Time</Title>
          <AreaChart
            className="mt-6"
            data={metrics.tbt}
            index="timestamp"
            categories={['value']}
            colors={['red']}
            valueFormatter={(value) => `${value}ms`}
          />
        </Card>

        <Card>
          <Title>Interaction to Next Paint</Title>
          <AreaChart
            className="mt-6"
            data={metrics.inp}
            index="timestamp"
            categories={['value']}
            colors={['green']}
            valueFormatter={(value) => `${value}ms`}
          />
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <Title>Performance Trends</Title>
          <BarChart
            className="mt-6"
            data={metrics.performance}
            index="date"
            categories={['score']}
            colors={['blue']}
            valueFormatter={(value) => `${value}%`}
          />
        </Card>

        <Card>
          <Title>Resource Usage</Title>
          <BarChart
            className="mt-6"
            data={[
              { name: 'Images', value: 45 },
              { name: 'Scripts', value: 30 },
              { name: 'Styles', value: 15 },
              { name: 'Other', value: 10 }
            ]}
            index="name"
            categories={['value']}
            colors={['blue']}
            valueFormatter={(value) => `${value}%`}
          />
        </Card>
      </div>
    </div>
  )
} 