import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Slider } from '@/components/ui/slider.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { AlertTriangle, TrendingUp, DollarSign, Clock, CheckCircle, XCircle } from 'lucide-react'
import './App.css'

const API_BASE = 'http://localhost:5000/api/supply-chain'

function App() {
  const [disruptionTypes, setDisruptionTypes] = useState({})
  const [interventions, setInterventions] = useState({})
  const [selectedDisruption, setSelectedDisruption] = useState('')
  const [severity, setSeverity] = useState([0.5])
  const [duration, setDuration] = useState([10])
  const [selectedInterventions, setSelectedInterventions] = useState([])
  const [disruptionResults, setDisruptionResults] = useState(null)
  const [interventionResults, setInterventionResults] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Load initial data
    fetchDisruptionTypes()
    fetchInterventions()
  }, [])

  const fetchDisruptionTypes = async () => {
    try {
      const response = await fetch(`${API_BASE}/disruption-types`)
      const data = await response.json()
      setDisruptionTypes(data)
    } catch (error) {
      console.error('Error fetching disruption types:', error)
    }
  }

  const fetchInterventions = async () => {
    try {
      const response = await fetch(`${API_BASE}/interventions`)
      const data = await response.json()
      setInterventions(data)
    } catch (error) {
      console.error('Error fetching interventions:', error)
    }
  }

  const simulateDisruption = async () => {
    if (!selectedDisruption) return

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/simulate-disruption`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          disruption_type: selectedDisruption,
          severity: severity[0],
          duration: duration[0]
        })
      })
      const data = await response.json()
      setDisruptionResults(data)
      setInterventionResults(null) // Reset intervention results
    } catch (error) {
      console.error('Error simulating disruption:', error)
    } finally {
      setLoading(false)
    }
  }

  const simulateIntervention = async () => {
    if (!disruptionResults || selectedInterventions.length === 0) return

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/simulate-intervention`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          disruption: disruptionResults.disruption,
          interventions: selectedInterventions
        })
      })
      const data = await response.json()
      setInterventionResults(data)
    } catch (error) {
      console.error('Error simulating intervention:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleIntervention = (interventionId) => {
    setSelectedInterventions(prev => 
      prev.includes(interventionId) 
        ? prev.filter(id => id !== interventionId)
        : [...prev, interventionId]
    )
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount)
  }

  const getStockoutColor = (probability) => {
    if (probability < 0.2) return '#22c55e' // green
    if (probability < 0.5) return '#eab308' // yellow
    return '#ef4444' // red
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Supply Chain Co-pilot</h1>
          <p className="text-lg text-gray-600">AI-Driven Disruption Simulator for Walmart India</p>
        </div>

        {/* Disruption Configuration */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-500" />
              Configure Disruption Scenario
            </CardTitle>
            <CardDescription>
              Define the disruption parameters to simulate its impact on your supply chain
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="text-sm font-medium mb-2 block">Disruption Type</label>
                <Select value={selectedDisruption} onValueChange={setSelectedDisruption}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select disruption type" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(disruptionTypes).map(([key, value]) => (
                      <SelectItem key={key} value={key}>
                        {value.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Severity: {Math.round(severity[0] * 100)}%
                </label>
                <Slider
                  value={severity}
                  onValueChange={setSeverity}
                  max={1}
                  min={0.1}
                  step={0.1}
                  className="mt-2"
                />
              </div>
              
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Duration: {duration[0]} days
                </label>
                <Slider
                  value={duration}
                  onValueChange={setDuration}
                  max={30}
                  min={1}
                  step={1}
                  className="mt-2"
                />
              </div>
            </div>
            
            <Button 
              onClick={simulateDisruption} 
              disabled={!selectedDisruption || loading}
              className="w-full md:w-auto"
            >
              {loading ? 'Simulating...' : 'Simulate Disruption Impact'}
            </Button>
          </CardContent>
        </Card>

        {/* Disruption Results */}
        {disruptionResults && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Impact Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Disruption Impact Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                    <div className="flex items-center gap-2">
                      <DollarSign className="h-5 w-5 text-red-600" />
                      <span className="font-medium">Revenue at Risk</span>
                    </div>
                    <span className="text-lg font-bold text-red-600">
                      {formatCurrency(disruptionResults.impact.total_revenue_at_risk)}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-orange-50 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600">
                        {disruptionResults.impact.affected_skus}
                      </div>
                      <div className="text-sm text-gray-600">Affected SKUs</div>
                    </div>
                    <div className="text-center p-3 bg-red-50 rounded-lg">
                      <div className="text-2xl font-bold text-red-600">
                        {disruptionResults.impact.high_risk_skus}
                      </div>
                      <div className="text-sm text-gray-600">High Risk SKUs</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Stockout Risk Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Stockout Risk by Category</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={Object.entries(
                        disruptionResults.sku_impacts.reduce((acc, sku) => {
                          acc[sku.category] = (acc[sku.category] || 0) + sku.stockout_probability
                          return acc
                        }, {})
                      ).map(([category, risk], index) => ({
                        name: category,
                        value: Math.round(risk * 100),
                        fill: COLORS[index % COLORS.length]
                      }))}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    />
                    <Tooltip formatter={(value) => [`${value}%`, 'Risk Level']} />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Intervention Selection */}
        {disruptionResults && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-blue-500" />
                Select Intervention Strategies
              </CardTitle>
              <CardDescription>
                Choose one or more intervention strategies to mitigate the disruption impact
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {Object.entries(interventions).map(([key, intervention]) => (
                  <div
                    key={key}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      selectedInterventions.includes(key)
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => toggleIntervention(key)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium">{intervention.name}</h3>
                      {selectedInterventions.includes(key) ? (
                        <CheckCircle className="h-5 w-5 text-blue-500" />
                      ) : (
                        <XCircle className="h-5 w-5 text-gray-300" />
                      )}
                    </div>
                    <div className="text-sm text-gray-600 space-y-1">
                      <div>Cost per unit: {formatCurrency(intervention.cost_per_unit)}</div>
                      <div>Recovery rate: {Math.round(intervention.recovery_rate * 100)}%</div>
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {intervention.implementation_days} days to implement
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <Button 
                onClick={simulateIntervention}
                disabled={selectedInterventions.length === 0 || loading}
                className="w-full md:w-auto"
              >
                {loading ? 'Analyzing...' : 'Analyze Intervention Impact'}
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Intervention Results */}
        {interventionResults && (
          <div className="space-y-6">
            {/* ROI Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Intervention Analysis Results</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">
                      {formatCurrency(interventionResults.intervention_summary.total_cost)}
                    </div>
                    <div className="text-sm text-gray-600">Total Cost</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">
                      {formatCurrency(interventionResults.intervention_summary.total_revenue_saved)}
                    </div>
                    <div className="text-sm text-gray-600">Revenue Saved</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">
                      {formatCurrency(interventionResults.intervention_summary.net_benefit)}
                    </div>
                    <div className="text-sm text-gray-600">Net Benefit</div>
                  </div>
                  <div className="text-center p-4 bg-orange-50 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600">
                      {interventionResults.intervention_summary.overall_roi}%
                    </div>
                    <div className="text-sm text-gray-600">Overall ROI</div>
                  </div>
                </div>

                {/* Recommendation */}
                <Alert className={interventionResults.recommendation.recommended ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}>
                  <AlertTriangle className={`h-4 w-4 ${interventionResults.recommendation.recommended ? 'text-green-600' : 'text-red-600'}`} />
                  <AlertDescription className={interventionResults.recommendation.recommended ? 'text-green-800' : 'text-red-800'}>
                    <strong>Recommendation:</strong> {interventionResults.recommendation.recommended ? 'Proceed' : 'Reconsider'} with selected interventions.
                    Confidence level: <Badge variant="outline">{interventionResults.recommendation.confidence}</Badge>
                  </AlertDescription>
                </Alert>
              </CardContent>
            </Card>

            {/* Intervention Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle>Intervention Strategy Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={interventionResults.interventions}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="intervention_name" 
                      angle={-45}
                      textAnchor="end"
                      height={100}
                    />
                    <YAxis />
                    <Tooltip 
                      formatter={(value, name) => [
                        name === 'roi' ? `${value}%` : formatCurrency(value),
                        name === 'roi' ? 'ROI' : name === 'cost' ? 'Cost' : 'Revenue Saved'
                      ]}
                    />
                    <Bar dataKey="cost" fill="#ef4444" name="cost" />
                    <Bar dataKey="revenue_saved" fill="#22c55e" name="revenue_saved" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

