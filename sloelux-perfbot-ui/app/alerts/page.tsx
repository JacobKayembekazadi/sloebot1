'use client'

import React from 'react'
import { Card, Title, Text, Button, Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Badge, Select, SelectItem } from '@tremor/react'
import { useState } from 'react'

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([
    {
      id: 1,
      type: 'Performance Degradation',
      severity: 'high',
      message: 'LCP increased by 200ms',
      timestamp: '2024-02-14 10:30',
      status: 'active'
    },
    {
      id: 2,
      type: 'Resource Warning',
      severity: 'medium',
      message: 'Large images detected',
      timestamp: '2024-02-14 10:35',
      status: 'resolved'
    }
  ])

  const [filter, setFilter] = useState('all')

  const filteredAlerts = alerts.filter(alert => {
    if (filter === 'all') return true
    if (filter === 'active') return alert.status === 'active'
    if (filter === 'resolved') return alert.status === 'resolved'
    return true
  })

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Title>Alerts</Title>
        <div className="flex space-x-4">
          <Select
            value={filter}
            onValueChange={setFilter}
            className="w-40"
          >
            <SelectItem value="all">All Alerts</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="resolved">Resolved</SelectItem>
          </Select>
          <Button>Configure Alerts</Button>
        </div>
      </div>

      <Card>
        <Table>
          <TableHead>
            <TableRow>
              <TableHeaderCell>Type</TableHeaderCell>
              <TableHeaderCell>Severity</TableHeaderCell>
              <TableHeaderCell>Message</TableHeaderCell>
              <TableHeaderCell>Timestamp</TableHeaderCell>
              <TableHeaderCell>Status</TableHeaderCell>
              <TableHeaderCell>Actions</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredAlerts.map((alert) => (
              <TableRow key={alert.id}>
                <TableCell>{alert.type}</TableCell>
                <TableCell>
                  <Badge
                    color={
                      alert.severity === 'high'
                        ? 'red'
                        : alert.severity === 'medium'
                        ? 'yellow'
                        : 'blue'
                    }
                  >
                    {alert.severity}
                  </Badge>
                </TableCell>
                <TableCell>{alert.message}</TableCell>
                <TableCell>{alert.timestamp}</TableCell>
                <TableCell>
                  <Badge
                    color={alert.status === 'active' ? 'red' : 'green'}
                  >
                    {alert.status}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Button
                    size="xs"
                    variant="secondary"
                    onClick={() => {
                      // Handle alert action
                    }}
                  >
                    {alert.status === 'active' ? 'Resolve' : 'View Details'}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <Title>Alert Statistics</Title>
          <div className="mt-4">
            <Text>Active Alerts: 3</Text>
            <Text>Resolved Today: 5</Text>
            <Text>Average Resolution Time: 45m</Text>
          </div>
        </Card>

        <Card>
          <Title>Alert Rules</Title>
          <div className="mt-4 space-y-2">
            <Text>LCP {'>'} 2.5s</Text>
            <Text>TBT {'>'} 300ms</Text>
            <Text>INP {'>'} 200ms</Text>
          </div>
        </Card>

        <Card>
          <Title>Notification Channels</Title>
          <div className="mt-4 space-y-2">
            <Text>Slack: #performance-alerts</Text>
            <Text>Email: alerts@example.com</Text>
            <Text>Webhook: Enabled</Text>
          </div>
        </Card>
      </div>
    </div>
  )
} 