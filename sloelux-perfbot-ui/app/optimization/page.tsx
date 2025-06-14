'use client'

import { Card, Title, Text, Button, Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Badge } from '@tremor/react'
import { useState } from 'react'

export default function OptimizationPage() {
  const [optimizations, setOptimizations] = useState([
    {
      id: 1,
      type: 'Image Optimization',
      status: 'completed',
      impact: '+5 points',
      timestamp: '2024-02-14 10:30',
      details: 'Compressed 15 images'
    },
    {
      id: 2,
      type: 'CSS Minification',
      status: 'in-progress',
      impact: 'Pending',
      timestamp: '2024-02-14 10:35',
      details: 'Processing CSS files'
    }
  ])

  const startOptimization = async (type: string) => {
    try {
      const response = await fetch('http://localhost:8000/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type }),
      })
      const data = await response.json()
      // Update optimizations list
      setOptimizations([...optimizations, data])
    } catch (error) {
      console.error('Error starting optimization:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <Title>Quick Optimizations</Title>
          <div className="mt-4 space-y-4">
            <Button onClick={() => startOptimization('images')}>
              Optimize Images
            </Button>
            <Button onClick={() => startOptimization('css')}>
              Minify CSS
            </Button>
            <Button onClick={() => startOptimization('js')}>
              Minify JavaScript
            </Button>
          </div>
        </Card>

        <Card>
          <Title>Optimization Status</Title>
          <div className="mt-4">
            <Text>Current Score: 92</Text>
            <Text>Last Optimization: 10:30 AM</Text>
            <Text>Next Scheduled: 11:30 AM</Text>
          </div>
        </Card>

        <Card>
          <Title>Resource Usage</Title>
          <div className="mt-4">
            <Text>Images: 45%</Text>
            <Text>Scripts: 30%</Text>
            <Text>Styles: 15%</Text>
            <Text>Other: 10%</Text>
          </div>
        </Card>
      </div>

      <Card>
        <Title>Optimization History</Title>
        <Table className="mt-4">
          <TableHead>
            <TableRow>
              <TableHeaderCell>Type</TableHeaderCell>
              <TableHeaderCell>Status</TableHeaderCell>
              <TableHeaderCell>Impact</TableHeaderCell>
              <TableHeaderCell>Timestamp</TableHeaderCell>
              <TableHeaderCell>Details</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {optimizations.map((optimization) => (
              <TableRow key={optimization.id}>
                <TableCell>{optimization.type}</TableCell>
                <TableCell>
                  <Badge
                    color={
                      optimization.status === 'completed'
                        ? 'green'
                        : optimization.status === 'in-progress'
                        ? 'yellow'
                        : 'red'
                    }
                  >
                    {optimization.status}
                  </Badge>
                </TableCell>
                <TableCell>{optimization.impact}</TableCell>
                <TableCell>{optimization.timestamp}</TableCell>
                <TableCell>{optimization.details}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  )
} 