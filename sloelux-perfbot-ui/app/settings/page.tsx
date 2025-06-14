'use client'

import React from 'react'
import { Card, Title, Text, Button, TextInput, Select, SelectItem, Switch } from '@tremor/react'
import { useState } from 'react'

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    theme: 'light',
    notifications: {
      email: true,
      slack: true,
      webhook: false
    },
    monitoring: {
      interval: '5m',
      retention: '30d'
    },
    thresholds: {
      lcp: 2.5,
      tbt: 300,
      inp: 200
    }
  })

  const handleSave = () => {
    // TODO: Implement settings save
    console.log('Saving settings:', settings)
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Title>Settings</Title>
        <Button onClick={handleSave}>Save Changes</Button>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <Card>
          <Title>Appearance</Title>
          <div className="mt-4 space-y-4">
            <div>
              <Text>Theme</Text>
              <Select
                value={settings.theme}
                onValueChange={(value) => setSettings({ ...settings, theme: value })}
                className="mt-2"
              >
                <SelectItem value="light">Light</SelectItem>
                <SelectItem value="dark">Dark</SelectItem>
                <SelectItem value="system">System</SelectItem>
              </Select>
            </div>
          </div>
        </Card>

        <Card>
          <Title>Notifications</Title>
          <div className="mt-4 space-y-4">
            <div className="flex items-center justify-between">
              <Text>Email Notifications</Text>
              <Switch
                checked={settings.notifications.email}
                onChange={(checked) => setSettings({
                  ...settings,
                  notifications: { ...settings.notifications, email: checked }
                })}
              />
            </div>
            <div className="flex items-center justify-between">
              <Text>Slack Notifications</Text>
              <Switch
                checked={settings.notifications.slack}
                onChange={(checked) => setSettings({
                  ...settings,
                  notifications: { ...settings.notifications, slack: checked }
                })}
              />
            </div>
            <div className="flex items-center justify-between">
              <Text>Webhook Notifications</Text>
              <Switch
                checked={settings.notifications.webhook}
                onChange={(checked) => setSettings({
                  ...settings,
                  notifications: { ...settings.notifications, webhook: checked }
                })}
              />
            </div>
          </div>
        </Card>

        <Card>
          <Title>Monitoring</Title>
          <div className="mt-4 space-y-4">
            <div>
              <Text>Check Interval</Text>
              <Select
                value={settings.monitoring.interval}
                onValueChange={(value) => setSettings({
                  ...settings,
                  monitoring: { ...settings.monitoring, interval: value }
                })}
                className="mt-2"
              >
                <SelectItem value="1m">1 minute</SelectItem>
                <SelectItem value="5m">5 minutes</SelectItem>
                <SelectItem value="15m">15 minutes</SelectItem>
                <SelectItem value="30m">30 minutes</SelectItem>
                <SelectItem value="1h">1 hour</SelectItem>
              </Select>
            </div>
            <div>
              <Text>Data Retention</Text>
              <Select
                value={settings.monitoring.retention}
                onValueChange={(value) => setSettings({
                  ...settings,
                  monitoring: { ...settings.monitoring, retention: value }
                })}
                className="mt-2"
              >
                <SelectItem value="7d">7 days</SelectItem>
                <SelectItem value="14d">14 days</SelectItem>
                <SelectItem value="30d">30 days</SelectItem>
                <SelectItem value="90d">90 days</SelectItem>
              </Select>
            </div>
          </div>
        </Card>

        <Card>
          <Title>Performance Thresholds</Title>
          <div className="mt-4 space-y-4">
            <div>
              <Text>Largest Contentful Paint (LCP)</Text>
              <TextInput
                type="number"
                value={settings.thresholds.lcp.toString()}
                onChange={(e) => setSettings({
                  ...settings,
                  thresholds: { ...settings.thresholds, lcp: parseFloat(e.target.value) }
                })}
                className="mt-2"
                placeholder="2.5"
              />
            </div>
            <div>
              <Text>Total Blocking Time (TBT)</Text>
              <TextInput
                type="number"
                value={settings.thresholds.tbt.toString()}
                onChange={(e) => setSettings({
                  ...settings,
                  thresholds: { ...settings.thresholds, tbt: parseFloat(e.target.value) }
                })}
                className="mt-2"
                placeholder="300"
              />
            </div>
            <div>
              <Text>Interaction to Next Paint (INP)</Text>
              <TextInput
                type="number"
                value={settings.thresholds.inp.toString()}
                onChange={(e) => setSettings({
                  ...settings,
                  thresholds: { ...settings.thresholds, inp: parseFloat(e.target.value) }
                })}
                className="mt-2"
                placeholder="200"
              />
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
} 