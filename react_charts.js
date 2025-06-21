// components/Charts/PerformanceChart.js - Performance Metrics Chart
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';

const PerformanceChart = ({ data, type = 'line' }) => {
  if (!data || data.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
        No performance data available
      </div>
    );
  }

  const formatTooltip = (value, name) => {
    if (name === 'efficiency_score' || name === 'task_completion_rate' || name === 'citizen_satisfaction') {
      return [`${value.toFixed(1)}%`, name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())];
    }
    if (name === 'budget_utilization') {
      return [`$${value.toLocaleString()}`, 'Budget Utilization'];
    }
    return [value, name];
  };

  if (type === 'area') {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip formatter={formatTooltip} />
          <Legend />
          <Area
            type="monotone"
            dataKey="efficiency_score"
            stackId="1"
            stroke="#1890ff"
            fill="#1890ff"
            fillOpacity={0.6}
          />
          <Area
            type="monotone"
            dataKey="task_completion_rate"
            stackId="1"
            stroke="#52c41a"
            fill="#52c41a"
            fillOpacity={0.6}
          />
        </AreaChart>
      </ResponsiveContainer>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip formatter={formatTooltip} />
        <Legend />
        <Line
          type="monotone"
          dataKey="efficiency_score"
          stroke="#1890ff"
          strokeWidth={2}
          dot={{ r: 4 }}
        />
        <Line
          type="monotone"
          dataKey="task_completion_rate"
          stroke="#52c41a"
          strokeWidth={2}
          dot={{ r: 4 }}
        />
        <Line
          type="monotone"
          dataKey="citizen_satisfaction"
          stroke="#fa541c"
          strokeWidth={2}
          dot={{ r: 4 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

// components/Charts/ResourceChart.js - Resource Allocation Chart
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const ResourceChart = ({ data, type = 'bar' }) => {
  if (!data || data.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
        No resource data available
      </div>
    );
  }

  const COLORS = ['#1890ff', '#52c41a', '#fa541c', '#722ed1', '#faad14'];

  const formatTooltip = (value, name) => {
    if (name.includes('budget') || name.includes('equipment')) {
      return [`$${value.toLocaleString()}`, name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())];
    }
    if (name.includes('staff')) {
      return [`${value} staff`, name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())];
    }
    return [value, name];
  };

  if (type === 'pie') {
    return (
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip formatter={formatTooltip} />
        <Legend />
        <Bar dataKey="budget_allocation" fill="#1890ff" />
        <Bar dataKey="staff_allocation" fill="#52c41a" />
        <Bar dataKey="equipment_allocation" fill="#fa541c" />
      </BarChart>
    </ResponsiveContainer>
  );
};

// components/Charts/PredictiveChart.js - AI Predictions Chart
import React from 'react';
import Plot from 'react-plotly.js';

const PredictiveChart = ({ data }) => {
  if (!data || !data.predictions || data.predictions.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
        No prediction data available
      </div>
    );
  }

  const { predictions } = data;
  const dates = predictions.map(p => p.date);
  
  // Budget prediction trace
  const budgetTrace = {
    x: dates,
    y: predictions.map(p => p.budget_allocation),
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Budget Allocation',
    line: { color: '#1890ff', width: 3 },
    marker: { size: 8 }
  };

  // Staff prediction trace
  const staffTrace = {
    x: dates,
    y: predictions.map(p => p.staff_allocation),
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Staff Allocation',
    line: { color: '#52c41a', width: 3 },
    marker: { size: 8 },
    yaxis: 'y2'
  };

  // Equipment prediction trace
  const equipmentTrace = {
    x: dates,
    y: predictions.map(p => p.equipment_allocation),
    type: 'scatter',
    mode: 'lines+markers',
    name: 'Equipment Budget',
    line: { color: '#fa541c', width: 3 },
    marker: { size: 8 }
  };

  const layout = {
    title: `Resource Predictions - ${data.department}`,
    xaxis: {
      title: 'Time Period',
      type: 'date'
    },
    yaxis: {
      title: 'Budget ($)',
      side: 'left'
    },
    yaxis2: {
      title: 'Staff Count',
      side: 'right',
      overlaying: 'y'
    },
    legend: {
      x: 0,
      y: 1.1,
      orientation: 'h'
    },
    margin: { t: 60, r: 60, b: 60, l: 60 },
    height: 400
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
  };

  return (
    <div>
      <Plot
        data={[budgetTrace, equipmentTrace, staffTrace]}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
      />
      <div style={{ marginTop: 16, padding: 16, backgroundColor: '#f5f5f5', borderRadius: 6 }}>
        <p><strong>Model:</strong> {data.model_type}</p>
        <p><strong>Confidence:</strong> {(data.confidence * 100).toFixed(1)}%</p>
        <p><strong>Prediction Range:</strong> {predictions.length} months ahead</p>
      </div>
    </div>
  );
};

// components/Charts/TaskDistributionChart.js - Task Distribution Visualization
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const TaskDistributionChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
        No task distribution data available
      </div>
    );
  }

  const COLORS = {
    'Pending': '#faad14',
    'In Progress': '#1890ff',
    'Completed': '#52c41a',
    'Canceled': '#f5222d'
  };

  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={renderCustomizedLabel}
          outerRadius={100}
          fill="#8884d8"
          dataKey="count"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.status]} />
          ))}
        </Pie>
        <Tooltip formatter={(value) => [`${value} tasks`, 'Count']} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

// components/Charts/DepartmentComparisonChart.js - Department Performance Comparison
import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend } from 'recharts';

const DepartmentComparisonChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
        No comparison data available
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="metric" />
        <PolarRadiusAxis angle={90} domain={[0, 100]} />
        <Radar
          name="Current Performance"
          dataKey="current"
          stroke="#1890ff"
          fill="#1890ff"
          fillOpacity={0.3}
          strokeWidth={2}
        />
        <Radar
          name="Target Performance"
          dataKey="target"
          stroke="#52c41a"
          fill="#52c41a"
          fillOpacity={0.2}
          strokeWidth={2}
        />
        <Legend />
      </RadarChart>
    </ResponsiveContainer>
  );
};

// components/Charts/GeospatialChart.js - Map-based Data Visualization
import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const GeospatialChart = ({ data, center = [40.7128, -74.0060], zoom = 10 }) => {
  if (!data || data.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
        No geospatial data available
      </div>
    );
  }

  const getColorByValue = (value, max) => {
    const intensity = value / max;
    if (intensity > 0.8) return '#f5222d';
    if (intensity > 0.6) return '#fa541c';
    if (intensity > 0.4) return '#faad14';
    if (intensity > 0.2) return '#52c41a';
    return '#1890ff';
  };

  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <div style={{ height: '400px', width: '100%' }}>
      <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {data.map((point, index) => (
          <React.Fragment key={index}>
            <Marker position={[point.lat, point.lng]}>
              <Popup>
                <div>
                  <h4>{point.name}</h4>
                  <p>Value: {point.value}</p>
                  <p>Department: {point.department}</p>
                </div>
              </Popup>
            </Marker>
            <Circle
              center={[point.lat, point.lng]}
              radius={point.value * 10}
              color={getColorByValue(point.value, maxValue)}
              fillColor={getColorByValue(point.value, maxValue)}
              fillOpacity={0.5}
            />
          </React.Fragment>
        ))}
      </MapContainer>
    </div>
  );
};

export { 
  PerformanceChart, 
  ResourceChart, 
  PredictiveChart, 
  TaskDistributionChart, 
  DepartmentComparisonChart, 
  GeospatialChart 
};