import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  AlertTriangle, 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Shield, 
  Zap,
  BarChart3,
  Network,
  Brain,
  Target,
  Clock,
  DollarSign
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import './App.css'

// Mock data for demonstration
const riskData = [
  { name: 'Jan', risk: 65, cost: 2.3 },
  { name: 'Feb', risk: 59, cost: 1.8 },
  { name: 'Mar', risk: 80, cost: 4.2 },
  { name: 'Apr', risk: 81, cost: 3.9 },
  { name: 'May', risk: 56, cost: 2.1 },
  { name: 'Jun', risk: 55, cost: 1.9 },
  { name: 'Jul', risk: 40, cost: 1.2 }
]

const supplyChainData = [
  { name: 'Electronics', healthy: 85, disrupted: 15 },
  { name: 'Groceries', healthy: 92, disrupted: 8 },
  { name: 'Apparel', healthy: 78, disrupted: 22 },
  { name: 'Home & Garden', healthy: 88, disrupted: 12 }
]

const disruptionTypes = [
  { name: 'Supplier Issues', value: 35, color: '#ff6b6b' },
  { name: 'Transport Delays', value: 28, color: '#4ecdc4' },
  { name: 'Weather Events', value: 20, color: '#45b7d1' },
  { name: 'Geopolitical', value: 17, color: '#96ceb4' }
]

const alerts = [
  {
    id: 1,
    type: 'critical',
    title: 'Red Sea Route Disruption',
    description: 'Major shipping delays affecting electronics supply chain. Estimated impact: $12M',
    timestamp: '2 hours ago',
    category: 'Geopolitical'
  },
  {
    id: 2,
    type: 'warning',
    title: 'Supplier Performance Anomaly',
    description: 'Supplier ABC showing 30% performance drop in last 48 hours',
    timestamp: '4 hours ago',
    category: 'Supplier'
  },
  {
    id: 3,
    type: 'info',
    title: 'Inventory Optimization Complete',
    description: 'AI recommendations implemented for Tier-1 cities. Expected savings: $2.1M',
    timestamp: '6 hours ago',
    category: 'Optimization'
  }
]

const mitigationStrategies = [
  {
    id: 1,
    title: 'Alternative Supplier Activation',
    description: 'Activate backup suppliers for critical electronics components',
    impact: 'High',
    timeframe: '24-48 hours',
    cost: '$500K',
    confidence: 92
  },
  {
    id: 2,
    title: 'Route Diversification',
    description: 'Shift 40% of shipments to Pacific route via Singapore',
    impact: 'Medium',
    timeframe: '1-2 weeks',
    cost: '$1.2M',
    confidence: 87
  },
  {
    id: 3,
    title: 'Inventory Rebalancing',
    description: 'Redistribute stock from low-risk to high-risk regions',
    impact: 'Medium',
    timeframe: '3-5 days',
    cost: '$300K',
    confidence: 95
  }
]

function App() {
  const [selectedTab, setSelectedTab] = useState('overview')
  const [riskScore, setRiskScore] = useState(73)
  const [isSimulating, setIsSimulating] = useState(false)

  const runSimulation = () => {
    setIsSimulating(true)
    setTimeout(() => {
      setRiskScore(Math.floor(Math.random() * 30) + 40)
      setIsSimulating(false)
    }, 3000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white dark:bg-slate-800 shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">ResilienceNet</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">AI-Driven Supply Chain Resilience Platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-green-600 border-green-600">
                <Activity className="w-3 h-3 mr-1" />
                System Active
              </Badge>
              <Button onClick={runSimulation} disabled={isSimulating} className="bg-gradient-to-r from-blue-600 to-purple-600">
                {isSimulating ? (
                  <>
                    <Zap className="w-4 h-4 mr-2 animate-spin" />
                    Simulating...
                  </>
                ) : (
                  <>
                    <Brain className="w-4 h-4 mr-2" />
                    Run AI Simulation
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-red-500 to-red-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Risk Score</CardTitle>
              <AlertTriangle className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{riskScore}%</div>
              <p className="text-xs opacity-80">
                {riskScore > 70 ? '+12% from last week' : '-8% from last week'}
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Cost Savings</CardTitle>
              <DollarSign className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">$8.2M</div>
              <p className="text-xs opacity-80">+23% from last month</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Alerts</CardTitle>
              <Activity className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs opacity-80">2 critical, 1 warning</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Response Time</CardTitle>
              <Clock className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">2.3h</div>
              <p className="text-xs opacity-80">-45% improvement</p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs value={selectedTab} onValueChange={setSelectedTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="alerts">Alerts</TabsTrigger>
            <TabsTrigger value="mitigation">Mitigation</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Risk Trend Chart */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2" />
                    Risk & Cost Trends
                  </CardTitle>
                  <CardDescription>
                    Supply chain risk score and associated costs over time
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={riskData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis yAxisId="left" />
                      <YAxis yAxisId="right" orientation="right" />
                      <Tooltip />
                      <Legend />
                      <Line yAxisId="left" type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2} name="Risk Score %" />
                      <Line yAxisId="right" type="monotone" dataKey="cost" stroke="#3b82f6" strokeWidth={2} name="Cost Impact ($M)" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Supply Chain Health */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BarChart3 className="w-5 h-5 mr-2" />
                    Supply Chain Health
                  </CardTitle>
                  <CardDescription>
                    Health status across different product categories
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={supplyChainData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="healthy" stackId="a" fill="#10b981" name="Healthy %" />
                      <Bar dataKey="disrupted" stackId="a" fill="#ef4444" name="Disrupted %" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Disruption Types */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Network className="w-5 h-5 mr-2" />
                  Disruption Analysis
                </CardTitle>
                <CardDescription>
                  Distribution of disruption types affecting the supply chain
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={disruptionTypes}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {disruptionTypes.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="space-y-4">
                    {disruptionTypes.map((type, index) => (
                      <div key={index} className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div 
                            className="w-4 h-4 rounded-full" 
                            style={{ backgroundColor: type.color }}
                          ></div>
                          <span className="text-sm font-medium">{type.name}</span>
                        </div>
                        <span className="text-sm text-gray-500">{type.value}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Predictive Analytics</CardTitle>
                  <CardDescription>AI-powered forecasting and risk assessment</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Stockout Risk (Next 7 days)</span>
                      <span>23%</span>
                    </div>
                    <Progress value={23} className="h-2" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Cost Spike Probability</span>
                      <span>67%</span>
                    </div>
                    <Progress value={67} className="h-2" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Supplier Reliability</span>
                      <span>89%</span>
                    </div>
                    <Progress value={89} className="h-2" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Route Optimization</span>
                      <span>94%</span>
                    </div>
                    <Progress value={94} className="h-2" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>AI Model Performance</CardTitle>
                  <CardDescription>Real-time model accuracy and confidence metrics</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">94.2%</div>
                      <div className="text-sm text-gray-500">Prediction Accuracy</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">87.5%</div>
                      <div className="text-sm text-gray-500">Model Confidence</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600">2.3s</div>
                      <div className="text-sm text-gray-500">Response Time</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">99.8%</div>
                      <div className="text-sm text-gray-500">System Uptime</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="alerts" className="space-y-6">
            <div className="space-y-4">
              {alerts.map((alert) => (
                <Alert key={alert.id} className={`${
                  alert.type === 'critical' ? 'border-red-500 bg-red-50 dark:bg-red-950' :
                  alert.type === 'warning' ? 'border-yellow-500 bg-yellow-50 dark:bg-yellow-950' :
                  'border-blue-500 bg-blue-50 dark:bg-blue-950'
                }`}>
                  <AlertTriangle className={`h-4 w-4 ${
                    alert.type === 'critical' ? 'text-red-600' :
                    alert.type === 'warning' ? 'text-yellow-600' :
                    'text-blue-600'
                  }`} />
                  <AlertTitle className="flex items-center justify-between">
                    <span>{alert.title}</span>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="text-xs">
                        {alert.category}
                      </Badge>
                      <span className="text-xs text-gray-500">{alert.timestamp}</span>
                    </div>
                  </AlertTitle>
                  <AlertDescription>
                    {alert.description}
                  </AlertDescription>
                </Alert>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="mitigation" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-1 gap-6">
              {mitigationStrategies.map((strategy) => (
                <Card key={strategy.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center">
                        <Target className="w-5 h-5 mr-2" />
                        {strategy.title}
                      </CardTitle>
                      <Badge variant={
                        strategy.impact === 'High' ? 'destructive' :
                        strategy.impact === 'Medium' ? 'default' : 'secondary'
                      }>
                        {strategy.impact} Impact
                      </Badge>
                    </div>
                    <CardDescription>{strategy.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div>
                        <div className="text-sm font-medium text-gray-500">Timeframe</div>
                        <div className="text-lg font-semibold">{strategy.timeframe}</div>
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-500">Estimated Cost</div>
                        <div className="text-lg font-semibold">{strategy.cost}</div>
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-500">Confidence</div>
                        <div className="flex items-center space-x-2">
                          <div className="text-lg font-semibold">{strategy.confidence}%</div>
                          <Progress value={strategy.confidence} className="h-2 flex-1" />
                        </div>
                      </div>
                      <div className="flex items-end">
                        <Button className="w-full bg-gradient-to-r from-green-600 to-green-700">
                          Implement Strategy
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

export default App

